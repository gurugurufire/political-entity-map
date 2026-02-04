---
description: GitHubへのコミット＆プッシュを安全に実行する標準手順
---

# 🚀 Git Push ワークフロー

このワークフローは、変更をGitHubリポジトリに安全にプッシュするための標準手順です。

## 実行プロセス

### 1. `tech-standard`スキルのロード
- `view_file .agent/skills/tech-standard/SKILL.md` を実行し、コミットメッセージの規格やブランチ運用ルールを確認します。

### 2. 状態確認とステージング
// turbo
```powershell
git status
```
- 意図しないファイル（秘密鍵、巨大ファイルなど）が含まれていないか確認します。
- 問題なければ `git add .` を実行します。

### 3. コミット (Standardized)
- `tech-standard` の規格に従ったコミットメッセージを作成します。
  - 例: `feat(scope): 簡潔な説明`
```powershell
git commit -m "feat(workflow): update session workflows for better automation"
```

### 4. プッシュ
```powershell
git push origin main
```

### 5. 完了報告
- プッシュが完了したことを報告します。
