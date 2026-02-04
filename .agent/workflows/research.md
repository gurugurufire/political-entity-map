---
description: 新しい技術やアーキテクチャの調査・研究を行う際の標準手順
---

# 🔬 Research & Architecture Workflow

新しいハックや技術検証を始める際は、以下の手順で「研究ドキュメント」を整備してください。

## 実行プロセス

### 1. 調査スキルの準備
以下のスキルをロードします（Local: `.agent/skills/` に無ければ Global: `$home/...` を参照）。
- `article-extractor` (Web記事抽出)
- `youtube-transcript` (動画リサーチ)
- `scrap-manager` (情報整理)
- `view_file` 等を使って `SKILL.md` を読み込んでください。

### 2. リサーチ実行 & スクラップ作成
- `article-extractor` や `youtube-transcript` を使用して情報を収集します。
- `scrap-manager` を使用して、集めた情報を `.agent/docs/scraps/` に保存・インデックス化します。

### 3. アーキテクチャの可視化
- `tech-standard` スキル (`view_file .agent/skills/tech-standard/SKILL.md`) のMermaid記法に従い、構造を図示します。

### 4. 検証プランの策定
- `.agent/plans/` に検証手順を作成します（`planning` ワークフローへの接続も可）。

### 5. 成果の格上げ
- 検証が成功したら、`agent-ops` を使って `AgentHistory.md` に記録し、知見を永続化します。
