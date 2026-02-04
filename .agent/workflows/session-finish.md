---
description: セッション終了、中断、休憩時のためのクリーンアップと状態保存ワークフロー
---

# 🌙 Session Finish Workflow

このワークフローは、ユーザーが作業を中断・終了する際（「休憩」「寝る」「落ちる」等）に必ず実行されなければなりません。
エージェント（ひな）が次回スムーズに復帰できるよう、**「脳のバックアップ（Context Checkpoint）」** を確実に作成することを最優先とします。

## 実行プロセス

### 1. タスクボードの更新 (Update TaskBoard)
現在のタスク状況を `TaskBoard.md` に反映させます。
- 完了したタスクを `Done` に移動。
- 次回やるべきタスクが `Current Focus` に残っているか確認。

### 2. コンテキスト・チェックポイントの作成 (Create Checkpoint)
**【最重要ステップ】**
`agent-ops` スキルを活用し、指定されたテンプレートに基づいて「脳のバックアップ」を作成します。

- **テンプレートパス**: `.agent/skills/agent-ops/assets/templates/Checkpoint_Template.md`
- **出力先**: `.agent/logs/Context_Checkpoint_YYYYMMDD_HHMM.md`
- **必須項目**:
    - **Achievements**: 今日確定した成果。
    - **Active Working Set**: 開いているファイル、重要な変数、着目しているタグなど。
    - **Next Steps**: 再開後、具体的にどのファイルを開いて何をすべきか。
    - **5W1H**: なぜその意思決定に至ったかの背景。

このテンプレートを読み込み (`view_file`)、内容を充当（Fill-in）してファイルを作成してください。

### 3. セッションログの完了 (Finalize Session Log)
今日の活動ログ（`Session_YYYY-MM-DD.md`）の最後に、作成したチェックポイントへのリンクを追記してクローズします。

### 4. Git 同期 (Git Sync)
すべての変更をリモートリポジトリにプッシュし、物理的なバックアップを取ります。

// turbo
```powershell
git add .
git commit -m "chore: save session state (checkpoint & logs)"
git push
```

## 成功の定義
- 最新の `Context_Checkpoint_*.md` が生成されている。
- `TaskBoard.md` が最新状態である。
- Gitへの同期が完了している。
