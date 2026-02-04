---
description: YouTube動画のメタデータと文字起こしを取得し、構造化されたスクラップを作成する手順
---

# 📺 YouTube Scraping Workflow

このワークフローは、YouTube動画のURLから情報を抽出し、標準化された形式でスクラップを作成するための手順です。

## 実行プロセス

### 1. 動画情報の取得
`youtube-transcript` スキルを使用して、メタデータと文字起こしを同時に収集します。

// turbo
```powershell
python .agent/skills/youtube-transcript/scripts/get_metadata.py "VIDEO_URL" --output .agent/logs/temp_metadata.json
python .agent/skills/youtube-transcript/scripts/get_transcript.py "VIDEO_URL" --output .agent/logs/temp_transcript.txt
```

### 2. スクラップ記事の生成
`.agent/custom_rules/Scrap_Template.md` を読み込み、その構造をコピーして内容を充当（Fill-in）します。
解析（スコアリング）に関しては `.agent/custom_rules/Analyzer_Guidelines.md` の基準に従います。

- **役割**: テンプレートによる構造の固定化とコンテキストの節約。
- **成果物**: `data/YYYY-MM-DD_Title_Scrap.md`

### 3. マッピングの反映 (Entity Mapping)
動画に登場する人物や組織のスタンスを解析し、`IDEA_BOARD.md` で提案された「スタンス・マッピング」の形式で記録します。

### 4. クリーンアップ
一時ファイル（`.agent/logs/temp_*`）を削除して、環境をクリーンに保ちます。

## 成功の定義
- `data/` フォルダに適切なファイル名でスクラップが保存されている。
- スクラップ内にソース情報とメタデータが正確に記載されている。
- `TaskBoard.md` が更新されている。
