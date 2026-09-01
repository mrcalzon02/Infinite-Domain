param(
    [string]$Destination = '',
    [string]$JavaPath = ''
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$instance = Split-Path -Parent $PSScriptRoot
$neoForgeVersion = '21.1.248'
$installerSha256 = '68eeab77059ba53df1812f1afa5bf530ab2566a3cdcd5f924aa6e71be42e410c'
$cacheRoot = [IO.Path]::GetFullPath((Join-Path $instance 'benchmark_runs\.launcher-cache'))
if (-not $Destination) {
    $Destination = Join-Path $cacheRoot "neoforge-$neoForgeVersion-server"
}
$Destination = [IO.Path]::GetFullPath($Destination)
if (-not $JavaPath) {
    $JavaPath = 'C:\Users\Admin\curseforge\minecraft\Install\java\Jre_21\bin\java.exe'
}
if (-not (Test-Path -LiteralPath $JavaPath -PathType Leaf)) {
    throw "Java 21 runtime is missing: $JavaPath"
}

$installer = Join-Path $cacheRoot "neoforge-$neoForgeVersion-installer.jar"
$installerUri = "https://maven.neoforged.net/releases/net/neoforged/neoforge/$neoForgeVersion/neoforge-$neoForgeVersion-installer.jar"
New-Item -ItemType Directory -Path $cacheRoot -Force | Out-Null
if (-not (Test-Path -LiteralPath $installer -PathType Leaf)) {
    Write-Host "Downloading the official NeoForge $neoForgeVersion installer ..."
    Invoke-WebRequest -Uri $installerUri -OutFile $installer
}
$actualHash = (Get-FileHash -LiteralPath $installer -Algorithm SHA256).Hash.ToLowerInvariant()
if ($actualHash -ne $installerSha256) {
    throw "NeoForge installer SHA-256 mismatch. Expected $installerSha256, found $actualHash at $installer"
}

New-Item -ItemType Directory -Path $Destination -Force | Out-Null
Push-Location $Destination
try {
    & $JavaPath -jar $installer --installServer
    if ($LASTEXITCODE -ne 0) {
        throw "NeoForge server installer exited with code $LASTEXITCODE"
    }
} finally {
    Pop-Location
}

$argumentFile = Join-Path $Destination "libraries\net\neoforged\neoforge\$neoForgeVersion\win_args.txt"
$serverJar = Join-Path $Destination "libraries\net\neoforged\neoforge\$neoForgeVersion\neoforge-$neoForgeVersion-server.jar"
if (-not (Test-Path -LiteralPath $argumentFile -PathType Leaf) -or -not (Test-Path -LiteralPath $serverJar -PathType Leaf)) {
    throw "NeoForge reported success but the dedicated-server runtime is incomplete at $Destination"
}

Write-Host "NeoForge $neoForgeVersion dedicated-server runtime is ready: $Destination"
Write-Host 'Validate it with: .\scripts\run_worldgen_benchmark.ps1 -ValidateLauncher'
