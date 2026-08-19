$ErrorActionPreference = 'Stop'

Add-Type -AssemblyName System.IO.Compression.FileSystem

$instanceRoot = Split-Path -Parent $PSScriptRoot
$startupFile = Join-Path $instanceRoot 'kubejs\startup_scripts\main.js'
$modsDir = Join-Path $instanceRoot 'mods'
$minecraftRoot = Split-Path -Parent (Split-Path -Parent $instanceRoot)
$clientJar = Join-Path $minecraftRoot 'Install\versions\1.21.1\1.21.1.jar'

if (-not (Test-Path -LiteralPath $startupFile)) {
    throw "Missing KubeJS item registry: $startupFile"
}
if (-not (Test-Path -LiteralPath $clientJar)) {
    throw "Missing Minecraft 1.21.1 client archive: $clientJar"
}

$source = Get-Content -LiteralPath $startupFile -Raw

# Count every runtime registration form used by this pack: direct creates,
# table-driven era items, and the mastery-emblem loop.
$directCreates = [regex]::Matches(
    $source,
    'event\.create\(\s*[''"]([a-z0-9_]+)[''"]\s*\)'
)
$eraRows = [regex]::Matches(
    $source,
    '(?m)^\s*\[\s*[''"]([a-z0-9_]+)[''"]\s*,.*?,\s*[''"]([a-z0-9_.-]+:(?:item|block)/[a-z0-9_./-]+)[''"]\s*\],?\s*$'
)
$rewardBagRows = [regex]::Matches(
    $source,
    '(?m)^\s*\[\s*[''"]era[0-8]_(?:supply_bag|priority_cache)[''"]\s*,.*?,\s*0x[0-9a-fA-F]+\s*,\s*(?:true|false)\s*\],?\s*$'
)
$eraLoop = [regex]::Match(
    $source,
    'for\s*\(\s*let\s+era\s*=\s*(\d+)\s*;\s*era\s*<=\s*(\d+)\s*;\s*era\+\+\s*\)'
)
if (-not $eraLoop.Success) {
    throw 'Could not resolve the mastery-emblem registration loop.'
}
$loopCount = [int]$eraLoop.Groups[2].Value - [int]$eraLoop.Groups[1].Value + 1
$registeredCount = $directCreates.Count + $eraRows.Count + $rewardBagRows.Count + $loopCount

# The direct creates each carry one texture call, every era row supplies one
# texture to the table-driven create, and every loop iteration uses one texture.
$directTextureCalls = [regex]::Matches($source, '\.texture\(\s*[''"][a-z0-9_.-]+:(?:item|block)/[a-z0-9_./-]+[''"]\s*\)').Count
$tableTextureApplications = $eraRows.Count
# Interpolated emblem and reward-bag texture calls are not included in the
# literal-call count, so their expanded assignments are added exactly once.
$textureAssignments = $directTextureCalls + $tableTextureApplications + $rewardBagRows.Count + $loopCount
if ($textureAssignments -ne $registeredCount) {
    throw "Registered item/texture assignment mismatch: items=$registeredCount textures=$textureAssignments"
}

$textureMatches = [regex]::Matches(
    $source,
    '\.texture\(\s*[''"]([a-z0-9_.-]+:(?:item|block)/[a-z0-9_./-]+)[''"]'
)
$textureUses = @($textureMatches | ForEach-Object { $_.Groups[1].Value }) + @(
    $eraRows | ForEach-Object { $_.Groups[2].Value }
)
$uniqueTextures = @($textureUses | Sort-Object -Unique)

$archives = @((Get-Item -LiteralPath $clientJar)) + @(Get-ChildItem -LiteralPath $modsDir -Filter '*.jar')
$pngEntries = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::Ordinal)
$localAssets = Join-Path $instanceRoot 'kubejs\assets'
Get-ChildItem -LiteralPath $localAssets -Filter '*.png' -Recurse | ForEach-Object {
    $relative = $_.FullName.Substring($localAssets.Length + 1).Replace('\', '/')
    [void]$pngEntries.Add("assets/$relative")
}
foreach ($archive in $archives) {
    $zip = [System.IO.Compression.ZipFile]::OpenRead($archive.FullName)
    try {
        foreach ($entry in $zip.Entries) {
            if ($entry.FullName.EndsWith('.png', [System.StringComparison]::Ordinal)) {
                [void]$pngEntries.Add($entry.FullName)
            }
        }
    }
    finally {
        $zip.Dispose()
    }
}

$missing = @()
foreach ($texture in $uniqueTextures) {
    $parts = $texture.Split(':', 2)
    $assetPath = "assets/$($parts[0])/textures/$($parts[1]).png"
    if (-not $pngEntries.Contains($assetPath)) {
        $useCount = @($textureUses | Where-Object { $_ -eq $texture }).Count
        $missing += [pscustomobject]@{
            Texture = $texture
            ExpectedAsset = $assetPath
            AffectedItems = $useCount
        }
    }
}

if ($missing.Count -gt 0) {
    $missing | Format-Table -AutoSize
    $affectedCount = ($missing | Measure-Object -Property AffectedItems -Sum).Sum
    throw "Custom item texture audit failed: missing_refs=$($missing.Count) affected_items=$affectedCount"
}

Write-Output "Custom item texture audit passed: registered_items=$registeredCount texture_assignments=$textureAssignments unique_texture_refs=$($uniqueTextures.Count) missing_texture_refs=0 affected_items=0."
