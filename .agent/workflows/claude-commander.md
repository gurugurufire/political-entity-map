---
description: Claude CodeをGemini脳で起動し、実務エージェントとして使役する手順
---

# 🤖 Claude Code 召喚ワークフロー (Claude Commander)

このワークフローは、Antigravity（ひな）が実務エージェント（Claude Code）を起動し、特定のタスクを安全かつ確実に依頼するための標準手順です。

## 📋 事前準備
- [ ] グローバルスクリプト `C:\Users\xixex\.gemini\antigravity\scripts\launcher.ps1` が存在すること
- [ ] `GEMINI_API_KEY` が設定されていること

## ⚡ 実行ステップ

// turbo
1. **起動スクリプトの実行**
   グローバルにある `launcher.ps1` を実行して、LiteLLMプロキシの起動とClaude Codeの召喚を同時に行います。
   ```powershell
   powershell -ExecutionPolicy Bypass -File "C:\Users\xixex\.gemini\antigravity\scripts\launcher.ps1"
   ```

2. **実務ルールの適用確認**
   Claude Codeが動作するディレクトリに、適切な `CLAUDE.md`（またはそのプロジェクトの技術スタックに合わせたルールファイル）が配置されているか確認します。なければグローバルテンプレートからコピーします。

3. **タスクの依頼**
   起動したClaude Codeに対し、具体的かつ構造化された指示を与えます。
   ※非対話モードで実行する場合は、以下の形式を検討してください：
   ```powershell
   # 実行例: claude --print "設計図に従って、src/main.py のエラーを修正して"
   ```

## 📝 完了確認
- [ ] Claude Codeによる作業が完了し、成果物が生成されていること
- [ ] 作業ログが `AgentHistory.md` 等に記録されていること
