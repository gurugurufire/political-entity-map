---
name: project-caretaker
description: プロジェクトの整理整頓、ログのアーカイブ、目次生成を行うスキル。「お掃除」専門。
---

# 🧹 Project Caretaker (お片付けスキル)

## 概要
プロジェクトフォルダ内の散乱したファイルを整理し、ドキュメントの目次を生成することで、開発環境を常に清潔に保ちます。
※タスクボードの整理は `task-manager` に移管しました。

## 使用方法 (Usage)

### 1. 📂 ファイル整理 (`/clean-room`)
ルートディレクトリにある散らかったファイルを、ルールに従って適切なフォルダへ移動します。
**手順:**
1. **Dry Run**: まず移動対象を確認します。
   ```powershell
   python .agent/skills/project-caretaker/scripts/organizer.py --dry-run
   ```
2. **Execution**: 内容を確認後、実際に移動します。
   ```powershell
   python .agent/skills/project-caretaker/scripts/organizer.py
   ```

### 2. 📑 目次更新 (`/update-index`)
`docs/` フォルダなどの内容をスキャンし、各フォルダに `README.md` (目次) を生成・更新します。
これにより、どこに何があるかが一目でわかるようになります。
**手順:**
1. **Execution**:
   ```powershell
   python .agent/skills/project-caretaker/scripts/index_generator.py
   ```

## 設定 (Configuration)
`resources/mapping_rules.json` でファイルの移動ルールを定義します。

## 注意事項
- ファイル削除は行いません（移動のみ）。
- `.git` や重要なシークレットファイルは触りません。
