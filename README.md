# 高山市暮らし応援商品券 加盟店検索サイト

飛騨高山市が発行する「暮らし応援商品券」の加盟店を、スマートフォンからかんたんに検索できるWebサイトです。

## 機能

- **地域・業種・フリーワード**で加盟店を絞り込み検索
- **さるぼぼコイン対応**のお店を一覧表示
- スマートフォン対応（レスポンシブデザイン）
- 毎日自動でデータを最新化

## ファイル構成

```
takayama-shohinken/
├── index.html                  # 検索サイト本体
├── data/
│   └── stores.json             # 加盟店データ（自動更新）
├── scripts/
│   └── update_data.py          # データ更新スクリプト
├── .github/
│   └── workflows/
│       └── update.yml          # 自動更新ワークフロー
└── README.md                   # このファイル
```

## 使い方

### ローカルで動かす場合

ファイルをダブルクリックするだけでは動作しません（セキュリティ制限のため）。
以下のいずれかの方法で起動してください。

**方法①：Python の簡易サーバーを使う**

```bash
cd takayama-shohinken
python -m http.server 8000
```

ブラウザで `http://localhost:8000` を開く。

**方法②：VS Code の Live Server 拡張機能を使う**

VS Code で `index.html` を開き、右クリック →「Open with Live Server」

### データを手動で更新する

```bash
pip install requests
python scripts/update_data.py
```

### GitHub Pages で公開する場合

1. このリポジトリを GitHub に push
2. GitHub のリポジトリ設定 → Pages → Source を「main ブランチのルート」に設定
3. 自動でページが公開されます

## データについて

| 項目 | 内容 |
|------|------|
| データ出典 | [高山市公式ウェブサイト](https://www.city.takayama.lg.jp/) 加盟店一覧CSV |
| 更新タイミング | 毎日 17:00（日本時間）に自動取得 |
| 文字コード | Shift-JIS（自動でUTF-8に変換） |

掲載情報の正確性については高山市公式サイトをご確認ください。

## 自動更新の仕組み

GitHub Actions を使い、毎日 UTC 08:00（JST 17:00）に以下を実行します。

1. 高山市公式サイトからCSVを取得
2. Shift-JIS → UTF-8 に変換して `data/stores.json` を生成
3. 変更があれば自動コミット・プッシュ

---

© 高山市暮らし応援商品券加盟店検索サイト
データ出典：高山市公式ウェブサイト
