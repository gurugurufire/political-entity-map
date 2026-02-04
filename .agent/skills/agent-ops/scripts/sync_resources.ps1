<#
.SYNOPSIS
    Local projects resources and Global resources synchronization script.
    Adopts the newer version of files by default.

.DESCRIPTION
    Syncs:
    1. Rules: .agent/custom_rules/GEMINI_Global_Rules_v3_Lite.md <-> $home/.gemini/GEMINI.md
    2. Skills: .agent/skills/ <-> $home/.gemini/antigravity/global_skills/
    3. Workflows: .agent/workflows/ <-> $home/.gemini/antigravity/global_workflows/

.PARAMETER DryRun
    If specified, shows what would be copied without actually copying.
#>

param(
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

# --- Configuration ---
$HomeDir = [System.Environment]::GetFolderPath("UserProfile")
$LocalRule = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot "../../../custom_rules/GEMINI_Global_Rules_v3_Lite.md"))
$GlobalRule = [System.IO.Path]::GetFullPath((Join-Path $HomeDir ".gemini/GEMINI.md"))

$LocalSkills = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot "../../../skills"))
$GlobalSkills = [System.IO.Path]::GetFullPath((Join-Path $HomeDir ".gemini/antigravity/global_skills"))

$LocalWorkflows = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot "../../../workflows"))
$GlobalWorkflows = [System.IO.Path]::GetFullPath((Join-Path $HomeDir ".gemini/antigravity/global_workflows"))

# --- Functions ---

function Sync-File ($src, $dest) {
    if (-not (Test-Path $src)) { return }
    if (-not (Test-Path $dest)) {
        Write-Host "New file found: $src -> $dest" -ForegroundColor Cyan
        if (-not $DryRun) {
            $parent = Split-Path $dest
            if (-not (Test-Path $parent)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
            Copy-Item $src $dest -Force
        }
        return
    }

    $srcTime = (Get-Item $src).LastWriteTime
    $destTime = (Get-Item $dest).LastWriteTime

    if ($srcTime -gt $destTime) {
        Write-Host "Updating newer: $src ($srcTime) -> $dest ($destTime)" -ForegroundColor Yellow
        if (-not $DryRun) { Copy-Item $src $dest -Force }
    }
}

function Sync-Folder ($srcDir, $destDir) {
    if (-not (Test-Path $srcDir)) { return }
    Write-Host "Scanning $srcDir -> $destDir" -ForegroundColor Gray
    
    $files = Get-ChildItem $srcDir -Recurse -File
    foreach ($file in $files) {
        $relPath = $file.FullName.Replace($srcDir, "").TrimStart("\").TrimStart("/")
        $destFile = Join-Path $destDir $relPath
        Sync-File $file.FullName $destFile
    }
}

# --- Execution ---

Write-Host "=== Resource Sync Start ===" -ForegroundColor Green
if ($DryRun) { Write-Host "[DRY RUN MODE] No files will be modified." -ForegroundColor Magenta }

# 1. Rule Sync (Bidirectional)
Sync-File $LocalRule $GlobalRule
Sync-File $GlobalRule $LocalRule

# 2. Skills Sync (Bidirectional)
Sync-Folder $LocalSkills $GlobalSkills
Sync-Folder $GlobalSkills $LocalSkills

# 3. Workflows Sync (Bidirectional)
Sync-Folder $LocalWorkflows $GlobalWorkflows
Sync-Folder $GlobalWorkflows $LocalWorkflows

Write-Host "=== Resource Sync Finished ===" -ForegroundColor Green
