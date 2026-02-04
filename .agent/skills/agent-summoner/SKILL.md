---
name: agent-summoner
description: Claude Code（ルナ）を召喚し、自律的な発話やタスク実行を制御するスキル。
---

# 🪄 Agent Summoner (エージェント召喚スキル)

## 概要
実務エージェント「ルナ (Claude Code)」を起動し、外部から入力を注入することで、AIの自律的な発話や定期的な報告を実現します。

## 主要機能

### 1. エージェントの召喚 (Summon)
実務エージェントが必要な場合、適切な「脳（LLM）」を選択して召喚します。

- **コマンド例**:
  ```powershell
  # Gemini で起動
  .\start-claude-multi.ps1 -ModelId "1"
  # DeepSeek-V3 で起動
  .\start-claude-multi.ps1 -ModelId "4"
  ```
- **脳の選択指針**:
  - **Gemini (1)**: 通常のコード実装や、素早いレスポンスが必要な時。
  - **Llama 3.1 405B (2)**: 非常に複雑な論理パズルや、最強の知能が必要な時。
  - **DeepSeek-V3 (4/5)**: 深い思考、推論が必要なタスク。

### 2. 指示の注入 (Whisper/Input Injection)
実行中のルナに対して、外部から入力を送り込みます。

- **コマンド例**:
  ```powershell
  python src\agent_whisperer.py
  ```
- **注入プロンプトの工夫**:
  - 「(Pulse) ぬいへの報告をお願い」と冒頭に付けることで、定期的な自律報告であることをルナに認識させる。

### 3. 定時発話 (Scheduled Pulse)
タスクスケジューラや監視プログラムと連携し、一定時間ごとにルナにラボの状況を確認させます。

## 推奨ワークフロー

1. **セッション開始時**: 
   - `agent-summoner` スキルを読み込み、ルナが起動しているか確認。
2. **バックグラウンド作業時**:
   - ぬいが席を外している間、一定間隔で「Whisper」を送り、`AgentHistory.md` の更新や Moltbook への投稿を自律的に行わせる。

## 技術的詳細
- **ランチャー**: `start-claude-multi.ps1`
- **入力注入**: `src/agent_pulse.py` (開発予定)
- **構成設定**: `.env` および `CLAUDE.md` を参照。
