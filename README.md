# USB Power Controller

GitHub ActionsからMQTTを経由してローカルPCのUSBポートの電源を制御するシンプルなシステムです。

## 概要

1. GitHubでPRがapprovalされると、GitHub ActionsがMQTTメッセージをpublishします
2. ローカルPCで動作するPythonスクリプトがMQTTメッセージをsubscribeします
3. メッセージを受信すると、指定されたUSBポートの電源をONにします

## セットアップ

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. uhubctlのインストール（USB制御用）

Ubuntu/Debian:
```bash
sudo apt-get install uhubctl
```

macOS:
```bash
brew install uhubctl
```

### 3. USBハブの確認

```bash
# USBハブの一覧を確認
uhubctl

# 特定のポートの状態を確認
uhubctl -p 1 -l 1-1
```

### 4. 設定の変更

`usb_power_controller.py`内の設定を環境に合わせて変更してください（87-99行目）：

```python
config = {
    "mqtt": {
        "broker": "your-mqtt-broker.com",  # MQTTブローカーのアドレス
        "port": 1883,
        "topic": "usb/power/control"       # MQTTトピック名
    },
    "usb": {
        "hub_device": "1-1",  # USBハブのデバイス番号
        "port_number": "1"    # 制御したいUSBポート番号
    }
}
```

### 5. GitHub Actionsの設定

GitHubリポジトリで以下のシークレット環境変数を設定してください：

- `MQTT_BROKER`: MQTTブローカーのアドレス

## 使用方法

### ローカルPCでの実行

```bash
python usb_power_controller.py
```

実行すると、MQTTメッセージの待機状態になります。

### GitHub Actionsのテスト

1. GitHubリポジトリにPRを作成
2. PRをapprovalする
3. GitHub Actionsが実行され、MQTTメッセージが送信される
4. ローカルPCのUSBポートがONになる

## 設定のカスタマイズ

### USBハブとポート番号の確認方法

```bash
# USBハブの詳細情報を確認
lsusb -t

# uhubctlでポート状態を確認
uhubctl -p 1 -l 1-1
```

### MQTTブローカーの変更

無料のMQTTブローカー例：
- `test.mosquitto.org` (テスト用)
- `broker.hivemq.com` (テスト用)

本番環境では独自のMQTTブローカーを使用することを推奨します。

## トラブルシューティング

### USBポート制御が動作しない場合

1. `uhubctl`コマンドが正しくインストールされているか確認
2. USBハブがper-port power switchingに対応しているか確認
3. 権限が必要な場合は`sudo`で実行

### MQTT接続エラー

1. MQTTブローカーのアドレスとポートが正しいか確認
2. ネットワーク接続を確認
3. ファイアウォールの設定を確認

## ファイル構成

```
.
├── .github/
│   └── workflows/
│       └── mqtt-publish.yml      # GitHub Actions設定
├── usb_power_controller.py       # メインスクリプト（設定も含む）
├── requirements.txt              # Python依存関係
└── README.md                     # このファイル
```