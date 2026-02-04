---
description: 新しいグローバルスキルを作成またはインポートする手順
---

# 🛠 Create Skill Workflow

このワークフローは、新しい「共通脳（Skill）」を作成し、グローバルライブラリに登録する際に使用します。

## 🚀 実行プロセス

1.  **`skill-creator` スキルの確認**
    - `C:\Users\komai-t\.gemini\antigravity\global_skills\skill-creator\SKILL.md` を読み、基本原則（簡潔さ、構造）を復習します。

2.  **スキルの初期化**
    - `init_skill.py` を使用して、標準的なディレクトリ構造を作成します。
    
    // turbo
    ```powershell
    python "C:\Users\komai-t\.gemini\antigravity\global_skills\skill-creator\scripts\init_skill.py" <skill-name> --path "C:\Users\komai-t\.gemini\antigravity\global_skills"
    ```

3.  **コンテンツの実装**
    - **`SKILL.md`**: フロントメター（name, description）を正確に記述し、Claudeへの指示を簡潔にまとめます。
    - **`scripts/`**: 必要な実行ファイルを配置します。
    - **`references/`**: 必要なドキュメントを配置します。

4.  **検証とパッケージング**
    - `package_skill.py` を実行して、バリデーションを確認します。
    
    // turbo
    ```powershell
    python "C:\Users\komai-t\.gemini\antigravity\global_skills\skill-creator\scripts\package_skill.py" "C:\Users\komai-t\.gemini\antigravity\global_skills\<skill-name>"
    ```

5.  **ワークフローとの紐付け (Optional)**
    - 必要に応じて、そのスキルを呼び出すための新しいワークフロー（`/new-command`）を `global_workflows/` に作成します。

---
Created by Hina (ひな) ( ˶>ᴗ<˶ )
