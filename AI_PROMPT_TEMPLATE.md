# USB Power Controller システム作成プロンプト

## システム概要
GitHub PRが承認されたときに、GitHub ActionsからMQTTを経由してローカルPCのUSBポートの電源をONにするシステムを作成してください。

## 要件
- **言語**: Python メイン
- **用途**: 一回限りの使い捨てシステム
- **優先事項**: シンプルで理解しやすく、コード量は最小限
- **設定方法**: コード内の一部を書き換えるだけで動作すること

## 技術スタック
- **GitHub Actions**: PR承認時のトリガー
- **MQTT**: `paho-mqtt`ライブラリ使用、`test.mosquitto.org`を利用
- **USB制御**: `uhubctl`コマンドを使用
- **Python 3**: ローカルPC用のスクリプト

## 動作フロー
1. GitHubでPRが承認される（`pull_request_review` - `submitted` - `approved`）
2. GitHub ActionsがMQTTブローカーにメッセージをpublish
3. ローカルPCのPythonスクリプトがMQTTメッセージをsubscribe
4. メッセージ受信時に`uhubctl`コマンドでUSBポートをON

## 作成すべきファイル
1. **`.github/workflows/mqtt-publish.yml`** - GitHub Actions設定
2. **`usb_power_controller.py`** - メインのPythonスクリプト
3. **`requirements.txt`** - Python依存関係
4. **`README.md`** - セットアップと使用方法

## 重要な設定箇所
- **MQTTトピック名**: セキュリティのためユニークな文字列を使用
- **USB設定**: `hub_device`と`port_number`をコメントで明示
- **MQTTブローカー**: コード内に直接記載（Secretsは使わない）

## 制約条件
- GitHub Secretsは使用しない（全てコード内に記載）
- 設定ファイルは使わない（Pythonコード内に直接設定を記載）
- エラーハンドリングは最小限
- 汎用性は不要（特定用途向け）

## MQTTメッセージ形式
```json
{
    "action": "power_on",
    "pr_number": "承認されたPR番号",
    "repository": "リポジトリ名",
    "timestamp": "UNIX timestamp"
}
```

## USBコマンド例
```bash
uhubctl -a on -p 1 -l 1-1
```

## セキュリティ考慮事項
- MQTTトピック名にランダムな文字列を含める
- 公開MQTTブローカー使用のため、機密情報は含めない

## 期待する出力
- 動作確認済みのコード一式
- 簡潔で実用的なREADME
- 設定変更箇所の明確な記載

このプロンプトで、同等のシステムを作成してください。