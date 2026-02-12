# sync-skills.ps1 - Sync skill directories from this repo to ~/.claude/skills/

$ErrorActionPreference = 'Stop'

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$TargetDir = Join-Path $env:USERPROFILE '.claude\skills'

Write-Host "Syncing skills from: $ScriptDir"
Write-Host "Target: $TargetDir"

# Git pull if inside a repo
Push-Location $ScriptDir
try {
    $null = git rev-parse --is-inside-work-tree 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host 'Pulling latest changes...'
        git pull
    }
} finally {
    Pop-Location
}

# If the script already lives in the target, just pull and exit
if ($ScriptDir -eq $TargetDir) {
    Write-Host "Script is running from $TargetDir - pull complete, nothing to sync."
    exit 0
}

# Create target if needed
if (-not (Test-Path $TargetDir)) {
    New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
}

# Iterate over directories in the script's location, skipping hidden ones
Get-ChildItem -Path $ScriptDir -Directory |
    Where-Object { -not $_.Name.StartsWith('.') } |
    ForEach-Object {
        $name = $_.Name
        $dest = Join-Path $TargetDir $name

        Write-Host "Syncing: $name"
        if (Test-Path $dest) {
            Remove-Item -Path $dest -Recurse -Force
        }
        Copy-Item -Path $_.FullName -Destination $dest -Recurse
    }

Write-Host "Done. Synced skills to $TargetDir"
