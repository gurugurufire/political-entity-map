---
name: kintone-manager
description: kintoneのアプリ設定、フィールド定義、およびアプリアクションを一括取得し、解析・図解（Mermaid）の補助を行うためのスキルです。kintone環境の最新化や差分調査を行う際に使用します。
---

# 🛠 kintone-manager

このスキルは、kintone APIを利用してアプリの構造を抽出し、要件定義書やシステム俯瞰図の最新化を強力にサポートします。

## 🎯 主な機能

1.  **設定一括抽出**: アプリIDを指定し、フィールド定義（JSON）、レイアウト（JSON）、アプリアクション設定を取得します。
2.  **構造の平坦化**: `src/desktop.js` のロジックに基づき、複雑なレイアウトとフィールド定義をマージして人間が読みやすい形式（CSV/JSON）に変換します。
3.  **関連性の抽出**: ルックアップ、関連レコード、アプリアクションから「アプリ間の繋がり」を自動的に抽出します。

## 🚀 実行ガイド

### 1. 認証情報の準備
以下のいずれかの方法で環境変数を設定してください。
- `KINTONE_BASE_URL`: `https://(subdomain).cybozu.com`
- `KINTONE_USERNAME` / `KINTONE_PASSWORD`
- もしくは `KINTONE_API_TOKEN` (アプリ単位)

### 2. スクリプトの実行
付属のスクリプトを使用して情報を抽出します。

```powershell
# 特定のアプリの設定を抽出
python scripts/kintone_fetch_config.py --app <AppID> --output ./output

# アプリ間の繋がりを抽出
python scripts/kintone_analyze_links.py --apps <AppID1,AppID2,...>
```

## 🧠 専門知識 (Domain Knowledge)

- **アプリの繋がり種別**:
    - **ルックアップ (Lookup)**: フィールド設定の `lookup` オブジェクトを参照。
    - **関連レコード (Related Records)**: フィールド設定の `referenceTable` を参照。
    - **アプリアクション (App Action)**: `/k/v1/app/actions.json` APIを使用して取得。

## 📋 運用ルール
- 取得した生データ（JSON）は必ず `99_アーカイブ` や `Logs` に残し、再現性を確保すること。
- 機密情報（パスワード等）が含まれないよう、出力結果のフィルタリングには細心の注意を払うこと。
