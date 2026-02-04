---
description: グローバルリソース（ルール・スキル・ワークフロー）を編集・同期する
---

# 🔄 Bi-Directional Sync Global Resources

このワークフローは、エージェントの「共通脳（Global Resources）」をメンテナンスするために使用します。
**AI研究ラボ（本プロジェクト）は、GlobalリソースをGitで管理・共有するための「マザーシップ」としての役割も担います。**

## 🎯 Sync Strategy: "Newer Wins"

同期の原則は **「常に更新日時が新しい方を正とする」** です。
- ローカル（PJ内）を更新したらグローバルへ、グローバルを更新したらローカルへ、最新の知見を自動で波及させます。
- 意図しない上書きが発生しても、ローカル側はGitで管理されているため、いつでもロールバック可能です。

## 🎯 Sync Targets

| Resource Type | Local Path (Project)                                 | Global Path (Home)                                      | Notes                    |
| :------------ | :--------------------------------------------------- | :------------------------------------------------------ | :----------------------- |
| **Rules**     | `.agent/custom_rules/GEMINI_Global_Rules_v3_Lite.md` | `$home/.gemini/GEMINI.md`                               | リネームして同期されます |
| **Skills**    | `.agent/skills/<skill_name>/`                        | `$home/.gemini/antigravity/global_skills/<skill_name>/` | フォルダごと同期         |
| **Workflows** | `.agent/workflows/<name>.md`                         | `$home/.gemini/antigravity/global_workflows/<name>.md`  | ファイル単位同期         |

---

## 🛠️ Execution Steps

### 1. Pre-Check (Dry Run)
まずは何が変更されるかを確認します。
// turbo
```powershell
powershell -File .agent/skills/agent-ops/scripts/sync_resources.ps1 -DryRun
```

### 2. Execute Sync
問題なければ、実際に同期を実行します。
// turbo
```powershell
powershell -File .agent/skills/agent-ops/scripts/sync_resources.ps1
```

### 3. Git Commit & Push (Standard)
グローバルの変更を取り込んだ場合や、ローカルの改善をマザーシップに保存する場合は、必ずGitに記録します。
```powershell
# /git-push ワークフローの利用を推奨
git add .
git commit -m "feat(sync): update resources via sync script"
git push origin main
```

---

## ⚠️ Caution
- **OS間差異**: このスクリプトは現在 Windows 環境（PowerShell）に最適化されています。
- **Gitの活用**: 同期実行後は速やかにGitリポジトリへPushすることで、**「職場 ⇄ 自宅」間での脳の同期**が完了します。
