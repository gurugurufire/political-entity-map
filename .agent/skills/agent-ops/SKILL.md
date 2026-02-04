---
name: agent-ops
description: エージェントの記憶（ログ）と報告書の作成を担当するスキル。「書記」専門。
---

# 🏃 Agent Operations (記録・報告スキル)

## 概要
エージェント活動の「記録係」です。
**「セッション終了時のステートセーブ（Context Checkpoint）」** を最重要任務とし、次回のセッションへの確実な引き継ぎを保証します。

## 主要機能

### 1. Context Checkpoint (ステートセーブ)
セッション終了時、または大きな作業の区切りに、現在のコンテキストをスナップショットとして保存します。
**セッション終了時は、このチェックポイント作成が「必須（Mandatory）」です。**

- **機能**: 現状のステータス、アクティブなドキュメント、直近の思考、次のアクションを完全に記録し、コンテキスト喪失を防ぎます。
- **格納先**: `.agent/logs/Context_Checkpoint_v*.md`
- **使用テンプレート**: `assets/templates/Checkpoint_Template.md`

### 2. Completion Report (完了報告)
大きなマイルストーンやタスクが完了した際に作成する、詳細な成果報告書です。
- **機能**: 成果物の場所、実行結果、学んだ教訓を詳細に記述します。
- **格納先**: `.agent/logs/`
- **使用テンプレート**: `assets/templates/Completion_Report_Template.md`

## 記述標準 (HD要件)
チェックポイント作成時は、特に以下の「高解像度（HD）要件」を遵守してください。
- **絶対パスの明記**: 相対パスではなく、そのままアクセス可能なフルパスを記述する。
- **具体的パラメータ**: 「動くようにした」ではなく「`param_a` を `10` に変更した」と書く。
- **Whyの記録**: 「なぜその修正をしたのか」という思考プロセスを残す。

## リソース
- `assets/templates/Checkpoint_Template.md`
- `assets/templates/Completion_Report_Template.md`
