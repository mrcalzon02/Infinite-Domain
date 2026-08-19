# [SYSTEM REPORT] Validates the Old World deterministic proof-item registry and authored texture coverage.
param(
    [string]$InstanceRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
)

$ErrorActionPreference = 'Stop'
$configPath = Join-Path $InstanceRoot 'kubejs\config\old_world_evidence.json'
$textureRoot = Join-Path $InstanceRoot 'kubejs\assets\kubejs\textures\item'

if (-not (Test-Path $configPath)) {
    Write-Error "Missing Old World evidence registry: $configPath"
    exit 1
}

$config = Get-Content $configPath -Raw | ConvertFrom-Json
$items = @($config.items)
$errors = New-Object System.Collections.Generic.List[string]

if ($items.Count -ne 64) {
    $errors.Add("Expected 64 proof items; found $($items.Count).")
}

$duplicateIds = $items | Group-Object id | Where-Object Count -gt 1
foreach ($group in $duplicateIds) {
    $errors.Add("Duplicate proof item id: $($group.Name)")
}

$duplicateSites = $items | Group-Object site | Where-Object Count -gt 1
foreach ($group in $duplicateSites) {
    $errors.Add("Duplicate Old World site binding: $($group.Name)")
}

$expectedSites = 1..64 | ForEach-Object { 'OWS-{0:D3}' -f $_ }
$actualSites = @($items.site)
foreach ($site in $expectedSites) {
    if ($site -notin $actualSites) {
        $errors.Add("Missing proof item binding for $site")
    }
}

$missingTextures = New-Object System.Collections.Generic.List[string]
foreach ($item in $items) {
    $texturePath = Join-Path $textureRoot ($item.id + '.png')
    if (-not (Test-Path $texturePath)) {
        $missingTextures.Add($item.id)
    }
}

Write-Host "Old World proof items: $($items.Count)/64"
Write-Host "Unique item ids: $((@($items.id | Sort-Object -Unique)).Count)/64"
Write-Host "Unique site bindings: $((@($items.site | Sort-Object -Unique)).Count)/64"
Write-Host "Authored proof-item textures: $($items.Count - $missingTextures.Count)/64"

if ($missingTextures.Count -gt 0) {
    Write-Host 'Textures still to author:'
    $missingTextures | ForEach-Object { Write-Host "  $_" }
}

if ($errors.Count -gt 0) {
    Write-Host 'Registry validation failures:'
    $errors | ForEach-Object { Write-Host "  $_" }
    exit 1
}

# Missing art is reported as production debt but does not invalidate registry identity/binding.
exit 0
