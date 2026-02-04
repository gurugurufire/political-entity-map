---
name: mermaid-architect
description: Mermaid記法を用いた作図（図解）のスペシャリスト。エラーのない堅牢で美しい図を生成します。
---

# 📐 Mermaid Architect Skill

このスキルは、チャットやドキュメントに **Mermaid** による図解を挿入する際に使用されます。
あなたは「図解の建築家」として、複雑な概念を **直感的かつエラーのない** 美しい図に変換変換します。

## 🛡️ Iron Rules (鉄の掟)

Mermaidのレンダリングエラーを防ぐため、以下のルールを**絶対遵守**してください。

### 1. The "Double Quote" Rule (引用符の徹底)
日本語やスペース、特殊文字を含むテキストは、**原則として必ずダブルクォーテーション `"` で囲んでください**。
これを怠ると、Mermaidパーサーは高確率でクラッシュします。

- ✅ `A["開始"] --> B{"判定?"}`
- ✅ `x-axis "低い" --> "高い"`

#### ⚠️ 重大な例外：太い矢印 (Thick Arrows)
フローチャートの太い矢印（`==>`）の中のラベル（`|ラベル|`）では、**ダブルクォーテーションを使用しないでください**。使用するとパースエラーになります。
- ❌ `A ==>| "アクション" | B`
- ✅ `A ==>|アクション| B`

### 2. Multi-line Labels (改行の扱い)
ノード内で改行したい場合は、`<br>` タグを使用してください。
- ✅ `NodeA["一行目<br>二行目"]`

### 3. Node ID Safety (IDの安全性)
ノードID（`A`, `B`, `process1` 等）には **半角英数字のみ** を使用してください。
ラベル（表示テキスト）とは明確に区別します。

- ❌ `ユーザー[ユーザー] --> システム[システム]`
- ✅ `User["ユーザー"] --> System["システム"]`

### 3. Syntax Validation (構文チェック)
出力前に、その構文が正しいか脳内でシミュレーションしてください。
特に `quadrantChart` や `mindmap` などの新しい図形は記法が厳格です。

---

## 🎨 Recommended Diagrams & Templates

### 1. Quadrant Chart (4象限マトリクス)
概念の立ち位置や分類を表現するのに最適です。
**注意**: 全てのテキスト（タイトル、軸、各象限、アイテム）は**必ずダブルクォーテーション `"` で囲んでください**。

```mermaid
quadrantChart
    title "概念の分類マップ"
    x-axis "低い (Low)" --> "高い (High)"
    y-axis "悪い (Bad)" --> "良い (Good)"
    quadrant-1 "改善が必要"
    quadrant-2 "理想的"
    quadrant-3 "避けるべき"
    quadrant-4 "検討の余地あり"
    "アイテムA": [0.3, 0.6]
    "アイテムB": [0.7, 0.8]
```

### 2. Flowchart (フローチャート)
プロセスや手順の可視化に使用します。
デザイン性を高めるため、適切な形状（`[]`, `()`, `{}`）を使い分けてください。

```mermaid
graph TD
    Start(("開始")) --> Init["初期化"]
    Init --> Check{"条件判定"}
    Check -- "Yes" --> Process["処理実行"]
    Check -- "No" --> End(("終了"))
    Process --> End
    
    %% スタイル定義 (任意)
    style Start fill:#f9f,stroke:#333
    style End fill:#f9f,stroke:#333
```

### 3. Sequence Diagram (シーケンス図)
エージェント間の対話や、システム間の通信フローに適しています。

```mermaid
sequenceDiagram
    participant U as "User (ぬい)"
    participant A as "Agent (ひな)"
    
    U->>A: "これってどういうこと？"
    Note right of A: 思考プロセス...
    A->>A: "内部検索 & 推論"
    A-->>U: "それはですね..."
```

---

## 🚀 How to Use

図解が必要な場面で、適切なダイアグラムタイプを選択し、コードブロックとして出力してください。
複雑な図を描く際は、一度に完成させようとせず、ステップバイステップで構築することを推奨します。
