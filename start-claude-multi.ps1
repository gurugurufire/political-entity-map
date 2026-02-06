param (
    [string]$ModelId
)

# AI Research Lab: Multi-Brain Launcher (NIM Enhanced)

# --- Settings: Load Environment Variables ---
# プロジェクトルートの .env を優先的に読み込む
$ENV_PATH = Join-Path (Get-Location) ".env"
if (Test-Path $ENV_PATH) {
    Write-Host "Loading environment from $ENV_PATH" -ForegroundColor Gray
    Get-Content $ENV_PATH | ForEach-Object {
        if ($_ -match '^([^#][^=]+)=(.*)$') {
            $name = $matches[1].Trim()
            $value = $matches[2].Trim().Trim('"').Trim("'")
            [System.Environment]::SetEnvironmentVariable($name, $value, "Process")
        }
    }
}

$MODELS = @{
    "1" = "gemini/gemini-2.0-flash";      
    "2" = "nvidia_nim/meta/llama-3.1-405b-instruct";
    "3" = "nvidia_nim/meta/llama-3.1-70b-instruct";
    "4" = "nvidia_nim/deepseek-ai/deepseek-v3.1-terminus";
    "5" = "nvidia_nim/deepseek-ai/deepseek-v3.2";
}

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "   AI Research Lab: Brain Selector" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

if (-not $ModelId) {
    Write-Host "Choose your Brain (LLM):"
    Write-Host "1: Gemini 2.0 Flash      (Fast/Stable)" -ForegroundColor White
    Write-Host "2: Llama 3.1 405B (NIM)  (God Mode)" -ForegroundColor Magenta
    Write-Host "3: Llama 3.1 70B  (NIM)  (Balanced)" -ForegroundColor Yellow
    Write-Host "4: DeepSeek-V3.1 (NIM)   (Terminus - Reasoning)" -ForegroundColor Cyan
    Write-Host "5: DeepSeek-V3.2 (NIM)   (Latest Reasoning)" -ForegroundColor Blue
    Write-Host "=========================================" -ForegroundColor Cyan

    $choice = Read-Host "Select (1-5)"
}
else {
    $choice = $ModelId
}

$MODEL_NAME = $MODELS[$choice]

if (-not $MODEL_NAME) {
    Write-Host "Invalid selection. Exiting..." -ForegroundColor Red
    exit
}

Write-Host "Selected Mode: $MODEL_NAME" -ForegroundColor Green

# NVIDIA NIM の場合は API キーを LiteLLM 用に設定
if ($MODEL_NAME -like "nvidia_nim/*") {
    if (-not $env:NVIDIA_API_KEY) {
        Write-Host "❌ Error: NVIDIA_API_KEY is not set in .env" -ForegroundColor Red
        exit
    }
    # LiteLLM が NVIDIA NIM に接続するために必要な変数を設定
    $env:OPENAI_API_KEY = $env:NVIDIA_API_KEY
    $env:OPENAI_API_BASE = "https://integrate.api.nvidia.com/v1"
}

Write-Host "Launching LiteLLM Proxy..." -ForegroundColor Yellow

# 1. Kill old processes
Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*litellm*" } | Stop-Process -Force

# 2. Start LiteLLM Proxy
# NVIDIA NIM の場合、LiteLLM は OpenAI 互換 API として動作させる
Start-Process powershell -ArgumentList "-NoExit", "-Command", "litellm --model $MODEL_NAME --drop_params" -WindowStyle Normal

# 3. Wait for proxy to start
Start-Sleep -Seconds 5

# 4. Set Env for Claude Code
$env:ANTHROPIC_BASE_URL = "http://localhost:4000"
$env:ANTHROPIC_API_KEY = "sk-placeholder"
$env:CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC = "1"

# 5. Summon Claude
Write-Host "Summoning Claude Code with $MODEL_NAME brain..." -ForegroundColor Green
claude

Write-Host "Session ended." -ForegroundColor Gray
