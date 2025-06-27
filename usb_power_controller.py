#!/usr/bin/env python3
"""
USB Power Controller - MQTTトリガーでUSBポートの電源をON/OFFする
"""

import json
import time
import subprocess
import paho.mqtt.client as mqtt
from typing import Dict, Any

class USBPowerController:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.mqtt_client = mqtt.Client()
        self.setup_mqtt()

    def setup_mqtt(self):
        """MQTT接続の設定"""
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        
        # MQTT接続
        broker = self.config['mqtt']['broker']
        port = self.config['mqtt']['port']
        
        print(f"MQTTブローカーに接続中: {broker}:{port}")
        self.mqtt_client.connect(broker, port, 60)

    def on_connect(self, client, userdata, flags, rc):
        """MQTT接続時のコールバック"""
        if rc == 0:
            print("MQTTブローカーに接続しました")
            topic = self.config['mqtt']['topic']
            client.subscribe(topic)
            print(f"トピックを購読中: {topic}")
        else:
            print(f"MQTT接続エラー: {rc}")

    def on_message(self, client, userdata, msg):
        """MQTTメッセージ受信時のコールバック"""
        try:
            message = json.loads(msg.payload.decode())
            print(f"MQTTメッセージ受信: {message}")
            
            if message.get('action') == 'power_on':
                self.power_on_usb_port()
                
        except json.JSONDecodeError:
            print("無効なJSONメッセージを受信しました")
        except Exception as e:
            print(f"メッセージ処理エラー: {e}")

    def power_on_usb_port(self):
        """USBポートの電源をONにする"""
        usb_port = self.config['usb']['port_number']
        hub_device = self.config['usb']['hub_device']
        
        print(f"USBポート {usb_port} の電源をONにします (ハブ: {hub_device})")
        
        try:
            # uhubctlを使用してUSBポートの電源をON
            # 実際のコマンドは使用するUSBハブによって異なります
            cmd = f"uhubctl -a on -p {usb_port} -l {hub_device}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"USBポート {usb_port} の電源をONにしました")
                print(f"出力: {result.stdout}")
            else:
                print(f"USBポート制御エラー: {result.stderr}")
                
        except Exception as e:
            print(f"USB電源制御エラー: {e}")

    def run(self):
        """メインループを開始"""
        print("USB Power Controller を開始しています...")
        print("MQTTメッセージを待機中... (Ctrl+Cで終了)")
        
        try:
            self.mqtt_client.loop_forever()
        except KeyboardInterrupt:
            print("\nプログラムを終了します")
            self.mqtt_client.disconnect()

def main():
    # 設定読み込み
    config = {
        "mqtt": {
            "broker": "test.mosquitto.org",  # 実際のMQTTブローカーに変更
            "port": 1883,
            "topic": "usb/power/control"
        },
        "usb": {
            "hub_device": "1-1",  # 実際のUSBハブデバイスに変更
            "port_number": "1"    # 制御したいUSBポート番号に変更
        }
    }
    
    # コントローラー開始
    controller = USBPowerController(config)
    controller.run()

if __name__ == "__main__":
    main()