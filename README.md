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
├── AI_PROMPT_TEMPLATE.md         # AI作成用プロンプト
└── README.md                     # このファイル
```

## AI作成用プロンプトテンプレート

このシステムを他のAIサービス（ChatGPT、Claude、Gemini等）で再現したい場合は、以下のプロンプトを使用してください：

---

### USB Power Controller システム作成プロンプト

**システム概要**
GitHub PRが承認されたときに、GitHub ActionsからMQTTを経由してローカルPCのUSBポートの電源をONにするシステムを作成してください。

**要件**
- **言語**: Python メイン
- **用途**: 一回限りの使い捨てシステム
- **優先事項**: シンプルで理解しやすく、コード量は最小限
- **設定方法**: コード内の一部を書き換えるだけで動作すること

**技術スタック**
- **GitHub Actions**: PR承認時のトリガー
- **MQTT**: `paho-mqtt`ライブラリ使用、`test.mosquitto.org`を利用
- **USB制御**: `uhubctl`コマンドを使用
- **Python 3**: ローカルPC用のスクリプト

**動作フロー**
1. GitHubでPRが承認される（`pull_request_review` - `submitted` - `approved`）
2. GitHub ActionsがMQTTブローカーにメッセージをpublish
3. ローカルPCのPythonスクリプトがMQTTメッセージをsubscribe
4. メッセージ受信時に`uhubctl`コマンドでUSBポートをON

**作成すべきファイル**
1. **`.github/workflows/mqtt-publish.yml`** - GitHub Actions設定
2. **`usb_power_controller.py`** - メインのPythonスクリプト
3. **`requirements.txt`** - Python依存関係
4. **`README.md`** - セットアップと使用方法

**重要な設定箇所**
- **MQTTトピック名**: セキュリティのためユニークな文字列を使用
- **USB設定**: `hub_device`と`port_number`をコメントで明示
- **MQTTブローカー**: コード内に直接記載（Secretsは使わない）

**制約条件**
- GitHub Secretsは使用しない（全てコード内に記載）
- 設定ファイルは使わない（Pythonコード内に直接設定を記載）
- エラーハンドリングは最小限
- 汎用性は不要（特定用途向け）

**MQTTメッセージ形式**
```json
{
    "action": "power_on",
    "pr_number": "承認されたPR番号",
    "repository": "リポジトリ名",
    "timestamp": "UNIX timestamp"
}
```

**USBコマンド例**
```bash
uhubctl -a on -p 1 -l 1-1
```

**セキュリティ考慮事項**
- MQTTトピック名にランダムな文字列を含める
- 公開MQTTブローカー使用のため、機密情報は含めない

**期待する出力**
- 動作確認済みのコード一式
- 簡潔で実用的なREADME
- 設定変更箇所の明確な記載

このプロンプトで、同等のシステムを作成してください。

---

詳細なプロンプトテンプレートは `AI_PROMPT_TEMPLATE.md` ファイルも参照してください。