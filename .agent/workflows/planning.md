---
description: 新しいタスクの計画策定とタスクボード更新の自動化
---

// turbo-all
このワークフローは、新しい機能開発やバグ修正の依頼を受けた際に、計画書の作成とタスクボードの更新を自動的に行います。

### 実行プロセス

1. **`task-manager`スキルをロード**
   - `task-manager` スキルをロードします（Local: `.agent/skills/` 優先、無ければ Global: `$home/...`）。
   - `SKILL.md` を読み、タスク管理の作法を確認します。

2. **計画書の作成 (Design Phase)**
   - `task-manager` のテンプレートを使用し、`.agent/plans/` フォルダに `[タスク名]_Plan_YYYYMMDD.md` を作成します。
   - `design-docs` スキルも参照し、設計品質を高めます。

3. **タスクボードの更新**
   - `task-manager` の機能を使って、`TaskBoard.md` に新しいタスクを追加・リンクします。
   - 優先順位（Priority）を適切に設定します。

4. **完了報告**
   - 計画が整ったことを報告し、実装フェーズへ移行するか確認します。