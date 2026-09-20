# YouTube CLI wrapper — PowerShell (.ps1)
# Interactive by default; non-interactive with --non-interactive
# Example interactive: .\youtube-downloader.ps1
# Example non-interactive: .\youtube-downloader.ps1 -url "https://youtube.com/watch?v=xxx"

param(
    [switch]$NonInteractive,
    [string]$Url = $null
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $scriptDir

if ($NonInteractive -and $Url) {
    Write-Host "Running in non-interactive mode with URL: $Url"
    python main_noplaylist.py $Url
} elseif ($Url) {
    # URL provided without explicit --non-interactive flag (treat as non-interactive)
    Write-Host "URL provided: $Url"
    python main_noplaylist.py $Url
} else {
    Write-Host "Running in interactive mode (default)."
    Write-Host "Enter a video URL (or use -NonInteractive -Url '...')"
    $userUrl = Read-Host "URL"
    if ([string]::IsNullOrWhiteSpace($userUrl)) {
        Write-Host "No URL entered. Exiting."
        exit 1
    }
    python main_noplaylist.py $userUrl
}
