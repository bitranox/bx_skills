# psync-skills.ps1 - Sync skill directories from this repo to <cwd>/.claude/skills/

$ErrorActionPreference = 'Stop'

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$CallDir = (Get-Location).Path
$TargetDir = Join-Path $CallDir '.claude\skills'

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
