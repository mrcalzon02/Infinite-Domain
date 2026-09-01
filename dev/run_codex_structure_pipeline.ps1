param(
    [string]$RepoRoot = ".",

    # 0 = no artificial run-count limit; stop only on completion, repeated failure, or Ctrl+C.
    [int]$MaxRuns = 0,

    [int]$RetryLimit = 3,

    # Optional extra arguments supported by your installed Codex CLI.
    # Example: -CodexArgs @("--sandbox","workspace-write")
    [string[]]$CodexArgs = @()
)

$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path $RepoRoot).Path
$PromptFile = Join-Path $RepoRoot "CODEX_STRUCTURE_PIPELINE.md"
$CodexDir = Join-Path $RepoRoot ".codex"
$StateFile = Join-Path $CodexDir "structure_pipeline_state.md"
$CompleteFile = Join-Path $CodexDir "structure_pipeline_complete"
$LogDir = Join-Path $CodexDir "structure_pipeline_logs"

if (-not (Get-Command codex -ErrorAction SilentlyContinue)) {
    throw "Codex CLI was not found on PATH."
}

if (-not (Test-Path $PromptFile)) {
    throw "Missing CODEX_STRUCTURE_PIPELINE.md in the repository root."
}

New-Item -ItemType Directory -Force -Path $CodexDir | Out-Null
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

if (-not (Test-Path $StateFile)) {
@"
# Codex Structure Pipeline State

Status: INITIALIZED
Current stage: A — existing structural audit
Last completed unit: none recorded by wrapper
Next action: inspect repository audit state and resume first unfinished unit

This file is persistent progress state for CODEX_STRUCTURE_PIPELINE.md.
Codex must update it after meaningful verified batches.
"@ | Set-Content -Path $StateFile -Encoding UTF8
}

$run = 0
$consecutiveFailures = 0

Push-Location $RepoRoot
try {
    while ($true) {
        if (Test-Path $CompleteFile) {
            Write-Host "Codex structure pipeline reports COMPLETE." -ForegroundColor Green
            Write-Host "Sentinel: $CompleteFile"
            break
        }

        if ($MaxRuns -gt 0 -and $run -ge $MaxRuns) {
            Write-Warning "Reached MaxRuns=$MaxRuns without a completion sentinel."
            Write-Host "Progress is preserved in $StateFile. Re-run the same command to continue."
            exit 2
        }

        $run++
        $timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
        $logFile = Join-Path $LogDir ("run-{0:D4}-{1}.jsonl" -f $run, $timestamp)

        Write-Host ""
        Write-Host "=== Codex structural pipeline run $run ===" -ForegroundColor Cyan
        Write-Host "Repository: $RepoRoot"
        Write-Host "State:      $StateFile"
        Write-Host "Log:        $logFile"

        $instruction = @"
Execute the long-running repository objective in CODEX_STRUCTURE_PIPELINE.md.

Read CODEX_STRUCTURE_PIPELINE.md and .codex/structure_pipeline_state.md first.
Locate and honor the repository's established structural-audit process and existing checkpoints.
Resume the next unfinished unit; do not restart completed audits or completed phases.
Perform real implementation/repair/validation work, not merely planning.
Finish Stage A completely before advancing to Stage B.
When Stage A's gate is satisfied, immediately continue Stage B.
Update .codex/structure_pipeline_state.md after meaningful verified progress.
Only create .codex/structure_pipeline_complete when every completion gate in CODEX_STRUCTURE_PIPELINE.md is genuinely satisfied.
If blocked, record the blocker and continue all independent unblocked work.
Work only on main. Never create a side branch.
"@

        $allArgs = @("exec", "--json") + $CodexArgs + @($instruction)

        & codex @allArgs 2>&1 | Tee-Object -FilePath $logFile
        $exitCode = $LASTEXITCODE

        if ($exitCode -eq 0) {
            $consecutiveFailures = 0
        } else {
            $consecutiveFailures++
            Write-Warning "codex exec exited with code $exitCode ($consecutiveFailures/$RetryLimit consecutive failures)."

            if ($consecutiveFailures -ge $RetryLimit) {
                Write-Error "Stopping after $RetryLimit consecutive Codex failures. Fix the underlying problem and rerun; state is preserved."
                exit $exitCode
            }

            Start-Sleep -Seconds ([Math]::Min(30, 5 * $consecutiveFailures))
        }

        if (Test-Path $CompleteFile) {
            Write-Host "Codex created the completion sentinel." -ForegroundColor Green
            break
        }

        Start-Sleep -Seconds 2
    }
}
finally {
    Pop-Location
}
