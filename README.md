# クラカジ (Kurakaji)
> 暮らしをスマートにする小型家電・雑貨家電カタログメディア

商標を使用せず、7文字の洗練されたネーミング「**クラカジ**」（暮らし＋家電/家事）を採用した、小型家電・雑貨家電特化型アフィリエイトWebサイトです。

## 特徴
- **即時API連携**: 楽天API経由でリアルタイム検索・商品取得が可能なVercel Serverless Function (`/api/items`) を標準装備。
- **モバイル＆PC両対応の洗練されたUI/UX**: スマートフォン、タブレット、PCいずれからも直感的に探せるレスポンシブデザイン。
- **厳選された導線**: 余計な装飾やノイズを排し、購入コンバージョン（CTA）を高める導線設計。
- **SEO & OGP最適化**: 構造化マークアップ、OGP設定済み。

## 構成
- `index.html`: セマンティックかつ軽量なHTML5構造
- `src/style.css`: 高級感と清潔感のあるクリーンなCSS
- `src/main.js`: リアルタイム検索・カテゴリー切替・並び順ソート・APIフォールバック制御
- `src/data.js`: 初期高速表示およびオフライン用マスターデータ
- `api/items.js`: 楽天API連携用 Vercel Serverless Function
- `vercel.json`: Vercel デプロイ構成

## Vercelデプロイ時の環境変数設定
Vercelダッシュボードの「Settings」>「Environment Variables」に以下を設定してください：
- `RAKUTEN_APP_ID`: 楽天API Application ID
- `RAKUTEN_ACCESS_KEY`: 楽天API Access Key
- `RAKUTEN_AFFILIATE_ID`: 楽天アフィリエイトID（任意）

## GitHub Actions（自動更新）
`.github/workflows/auto_post.yml` が配置されており、必要に応じて定期実行アクションを設定可能です。
