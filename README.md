# 🗞️ Political Scrap & Mapping Project (政治ネタ収集基地)

YouTube上の政治・時事ニュース動画を収集・解析し、情報の偏りや勢力図を可視化するプロジェクトです。
情報の濁流から「誰が何を語り、どのようなポジションにいるのか」を客観的にマッピングすることを目的としています。

## 🎯 目的 (Goals)
1. **情報の構造化**: 動画の内容をスクレイピングし、Markdown形式のレポート（Scrap）として保存。
2. **勢力図の可視化**: 収集したデータ（Sentiment, Stance）を元に、Mermaidを用いて勢力図（Political Map）を自動生成。
3. **情報バイアスの分析**: 発信者の立ち位置（Source Bias）を分析し、情報の偏りを可視化。

## 🛠️ システム構成 (Tech Stack)
- **Core**: Python
- **Format**: Markdown + Mermaid + JSON Metadata
- **Tools**:
    - `yt-dlp`: 動画メタデータ・字幕取得
    - `mapping_tool.py`: スクレイピングデータの集計・可視化スクリプト
    - `data/`: スクラップデータの格納庫

## 🚀 使い方 (Usage)

### 1. スクレイピング
YouTube動画からスクラップを作成します。（現在は自動化スクリプトを開発中）
`data/` ディレクトリに所定のフォーマット（Markdown + JSON Metadata）でファイルを作成してください。

### 2. マッピング生成
以下のコマンドを実行すると、`data/` 内の全ファイルを解析し、最新の `POLITICAL_MAP.md` を生成します。
```bash
python src/mapping_tool.py
```

## 🤝 貢献 (Contribution)
- 新しいニュースソースの追加、解析精度の向上、可視化ツールの改善など、歓迎します！
- Pull Request を送る際は、必ず解析対象の動画URLと根拠を明記してください。

## 📜 License
MIT License
