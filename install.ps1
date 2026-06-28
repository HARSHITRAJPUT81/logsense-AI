# LogSense AI - Windows PowerShell Installer
Write-Host ""
Write-Host "  ====================================" -ForegroundColor Cyan
Write-Host "   LogSense AI - Windows Installer" -ForegroundColor Cyan
Write-Host "  ====================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
try {
    python --version | Out-Null
    Write-Host "  Python found!" -ForegroundColor Green
} catch {
    Write-Host "  Python not found. Downloading..." -ForegroundColor Yellow
    $url = "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe"
    Invoke-WebRequest -Uri $url -OutFile "python_installer.exe"
    Start-Process python_installer.exe -Args "/quiet InstallAllUsers=1 PrependPath=1" -Wait
    Remove-Item python_installer.exe
    Write-Host "  Python installed!" -ForegroundColor Green
}

# Check Git
try {
    git --version | Out-Null
    Write-Host "  Git found!" -ForegroundColor Green
} catch {
    Write-Host "  Git not found. Downloading..." -ForegroundColor Yellow
    $url = "https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe"
    Invoke-WebRequest -Uri $url -OutFile "git_installer.exe"
    Start-Process git_installer.exe -Args "/VERYSILENT /NORESTART" -Wait
    Remove-Item git_installer.exe
    Write-Host "  Git installed!" -ForegroundColor Green
}

# Clone repo
if (-Not (Test-Path "logsense")) {
    Write-Host "  Downloading LogSense AI..." -ForegroundColor Yellow
    git clone https://github.com/HARSHITRAJPUT81/logsense.git
}

Set-Location logsense

# Setup venv
Write-Host "  Setting up Python environment..." -ForegroundColor Yellow
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt -q
pip install -e . -q
Write-Host "  Libraries installed!" -ForegroundColor Green

# API Key
Write-Host ""
Write-Host "  You need a FREE Groq API key" -ForegroundColor Cyan
Write-Host "  1. Go to: https://console.groq.com" -ForegroundColor White
Write-Host "  2. Sign up free with Google" -ForegroundColor White
Write-Host "  3. Click API Keys - Create API Key" -ForegroundColor White
Write-Host "  4. Copy key starting with gsk_..." -ForegroundColor White
Write-Host ""
$GROQ_KEY = Read-Host "  Paste your Groq API key"

# Create .env
"GROQ_API_KEY=$GROQ_KEY" | Out-File .env -Encoding utf8
"LOGSENSE_MODEL=claude-sonnet-4-6" | Out-File .env -Append -Encoding utf8
"LOGSENSE_DB=$env:USERPROFILE\.logsense\history.db" | Out-File .env -Append -Encoding utf8

# Add to PATH
$currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
$newPath = "$currentPath;$(Get-Location)\venv\Scripts"
[Environment]::SetEnvironmentVariable("PATH", $newPath, "User")

Write-Host ""
Write-Host "  ====================================" -ForegroundColor Green
Write-Host "   LogSense AI installed successfully!" -ForegroundColor Green
Write-Host "  ====================================" -ForegroundColor Green
Write-Host ""
Write-Host "  Commands to use:" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Analyze Windows System logs:" -ForegroundColor White
Write-Host "  logsense analyze `"$env:SystemRoot\System32\winevt\Logs\System.evtx`"" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Analyze Application logs:" -ForegroundColor White
Write-Host "  logsense analyze `"$env:SystemRoot\System32\winevt\Logs\Application.evtx`"" -ForegroundColor Yellow
Write-Host ""
Write-Host "  See history:" -ForegroundColor White
Write-Host "  logsense report" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Restart PowerShell before using logsense!" -ForegroundColor Red
Write-Host ""