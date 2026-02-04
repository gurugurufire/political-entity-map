# 📋 解析ワークフロースキーム (全体像)

現在のプロジェクトにおける、動画取得からマッピングまでの情報の流れを整理したスキーム図です。

```mermaid
graph TD
    subgraph "1. データ収集 (情報取得)"
        URL["YouTube URL"] --> Script["youtube-transcript スキル"]
        Script --> Meta["メタデータ (JSON)"]
        Script --> Trans["文字起こし (Text)"]
    end

    subgraph "2. 構造化スクラップ (Hinaによる解析)"
        Meta & Trans --> Analysis{"解析ガイドライン<br>に基づくスコアリング"}
        Analysis --> Scrap["スクラップ記事 (data/*.md)"]
        
        subgraph "スクラップの内容"
            Scrap --> Title["人間用ヘッダー<br>(🗞️ Scrap形式)"]
            Scrap --> Network["ネットワークマップ<br>(Mermaid図解)"]
            Scrap --> JSON["分析用メタデータ<br>(JSONブロック)"]
        end
    end

    subgraph "3. システム連携 (マッピング・可視化)"
        JSON --> Tool["mapping_tool.py<br>(データ統合エンジン)"]
        Tool --> Final["POLITICAL_MAP.md<br>(政治地図ダッシュボード)"]
        
        subgraph "可視化アウトプット"
            Final --> Chart1["勢力・感情分析チャート"]
            Final --> Chart2["発信者バイアス分析チャート"]
        end
    end

    %% スタイル設定
    style URL fill:#f9f,stroke:#333
    style Scrap fill:#bbf,stroke:#333
    style Final fill:#bfb,stroke:#333
```

## 🚀 各ステップの役割

1.  **Data Ingestion**: 原材料の収集。YouTubeのメタデータと文字起こしを自動で抜き出します。
2.  **Structured Scraping**: ぬいさんと相談して決めた「標準フォーマット」への整形。ここでAIが感情値やバイアス値をスコアリングします。
3.  **System Integration**: 独立したスクラップ記事を統合。Pythonスクリプトが全ファイルを読み込み、平均値を算出して全体の「地図」を自動更新します。
