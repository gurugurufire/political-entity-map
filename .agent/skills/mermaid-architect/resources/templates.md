# 📐 Mermaid Templates & Snippets

コピー＆ペーストして使える実用的な図解テンプレート集です。
**全ての日本語テキストは必ず `"` で囲んでください。**

## 1. Gantt Chart (プロジェクト進行)
タスクのスケジュール管理に使用します。

```mermaid
gantt
    title "プロジェクト進行表"
    dateFormat  YYYY-MM-DD
    section "調査フェーズ"
    "要件定義"       :done,    des1, 2026-02-01, 2026-02-03
    "技術選定"       :active,  des2, 2026-02-04, 3d
    section "実装フェーズ"
    "プロトタイプ"   :         des3, after des2, 5d
    "テスト"         :         des4, after des3, 2d
```

## 2. Git Graph (ブランチ戦略)
Gitのコミット履歴やブランチ運用を可視化します。
ラベル（コミットメッセージ等）は引用符で囲むのが安全です。

```mermaid
gitGraph
    commit id: "Initial"
    branch "feature/login"
    checkout "feature/login"
    commit id: "Add Auth"
    commit id: "Fix Bug"
    checkout main
    merge "feature/login"
    commit id: "Release v1.0"
```

## 3. Class Diagram (クラス設計)
オブジェクト指向設計の可視化に使用します。
型やメソッド名に日本語を使う場合は特に注意してください。

```mermaid
classDiagram
    class Agent {
        +String name
        +String role
        +think()
        +execute("Task")
    }
    class User {
        +String name
        +request("Order")
    }
    User "1" --> "*" Agent : "命令する"
```

## 4. Mindmap (マインドマップ)
アイデアの発散や構造化に使用します。
**注意**: `mindmap` は構文が独特で、スペースやインデントに敏感です。

```mermaid
mindmap
  root(("AI Research Lab"))
    "研究テーマ"
      "Transformer"
        "Attention"
        "Embedding"
      "Agent"
        "Orchestration"
        "Memory"
    "開発環境"
      "Local LLM"
      "Docker"
```

## 5. ER Diagram (データベース設計)
エンティティ間の関係を定義します。

```mermaid
erDiagram
    USER ||--o{ POST : "書く"
    USER {
        string name "ユーザー名"
        string email "メール"
    }
    POST {
        string title "タイトル"
        string content "本文"
    }
```

## 6. Quadrant Chart (4象限マトリクス)
**必須: 全ての文字列を `"` で囲むこと**
引用符で囲めば、日本語も問題なく表示されます。

```mermaid
quadrantChart
    title "システム分析"
    x-axis "コスト低" --> "コスト高"
    y-axis "価値低" --> "価値高"
    quadrant-1 "無駄"
    quadrant-2 "高コスパ"
    quadrant-3 "安物買い"
    quadrant-4 "戦略的投資"
    "プランA": [0.3, 0.8]
    "プランB": [0.75, 0.6]
```
