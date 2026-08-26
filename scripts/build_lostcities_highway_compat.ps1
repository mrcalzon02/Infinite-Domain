$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$project = Join-Path $root 'packdev\lostcities-highway-compat'
$source = Join-Path $project 'src\main\java'
$resources = Join-Path $project 'src\main\resources'
$build = Join-Path $project 'build'
$classes = Join-Path $build 'classes'
$staging = Join-Path $build 'staging'
$dependencies = Join-Path $build 'dependencies'
$mods = Join-Path $root 'mods'
$output = Join-Path $mods 'infinite-domain-lostcities-highway-compat-1.0.0.jar'

$minecraftRoot = 'C:\Users\Admin\curseforge\minecraft\Install\libraries'
$minecraft = Join-Path $minecraftRoot 'net\minecraft\client\1.21.1-20240808.144430\client-1.21.1-20240808.144430-srg.jar'
$loader = Join-Path $minecraftRoot 'net\neoforged\fancymodloader\loader\4.0.43\loader-4.0.43.jar'
$eventBus = Join-Path $minecraftRoot 'net\neoforged\bus\8.0.5\bus-8.0.5.jar'
$brigadier = Join-Path $minecraftRoot 'com\mojang\brigadier\1.3.10\brigadier-1.3.10.jar'
$dataFixer = Join-Path $minecraftRoot 'com\mojang\datafixerupper\8.0.16\datafixerupper-8.0.16.jar'
$distMarker = Join-Path $minecraftRoot 'net\neoforged\mergetool\2.0.7\mergetool-2.0.7-api.jar'
$neoForge = Join-Path $minecraftRoot 'net\neoforged\neoforge\21.1.248\neoforge-21.1.248-universal.jar'
$mixin = Join-Path $minecraftRoot 'net\fabricmc\sponge-mixin\0.15.2+mixin.0.8.7\sponge-mixin-0.15.2+mixin.0.8.7.jar'
$lostCities = Get-ChildItem -LiteralPath $mods -Filter 'lostcities-*.jar' | Select-Object -First 1 -ExpandProperty FullName
$javac = 'C:\Program Files\Pylo\MCreator\jdk\bin\javac.exe'
$jar = 'C:\Program Files\Pylo\MCreator\jdk\bin\jar.exe'

foreach ($required in @($minecraft, $loader, $eventBus, $brigadier, $dataFixer, $distMarker, $neoForge, $mixin, $lostCities, $javac, $jar)) {
    if (-not (Test-Path -LiteralPath $required)) {
        throw "Missing build dependency: $required"
    }
}

if (Test-Path -LiteralPath $build) {
    Remove-Item -LiteralPath $build -Recurse -Force
}
New-Item -ItemType Directory -Path $classes, $staging, $dependencies -Force | Out-Null

$localClasspath = @()
foreach ($dependency in @($minecraft, $loader, $eventBus, $brigadier, $dataFixer, $distMarker, $neoForge, $mixin, $lostCities)) {
    $localCopy = Join-Path $dependencies ([System.IO.Path]::GetFileName($dependency))
    Copy-Item -LiteralPath $dependency -Destination $localCopy -Force
    $localClasspath += $localCopy
}

$sources = Get-ChildItem -LiteralPath $source -Recurse -Filter '*.java' | Select-Object -ExpandProperty FullName
$classpath = $localClasspath -join ';'
& $javac --release 21 -proc:none -classpath $classpath -d $classes $sources
if ($LASTEXITCODE -ne 0) { throw "javac failed with exit code $LASTEXITCODE" }

Copy-Item -Path (Join-Path $classes '*') -Destination $staging -Recurse -Force
Copy-Item -Path (Join-Path $resources '*') -Destination $staging -Recurse -Force

foreach ($oldPatch in Get-ChildItem -LiteralPath $mods -Filter 'infinite-domain-lostcities-highway-compat-*.jar') {
    Remove-Item -LiteralPath $oldPatch.FullName -Force
}
Push-Location $staging
try {
    & $jar --create --file $output .
    if ($LASTEXITCODE -ne 0) { throw "jar failed with exit code $LASTEXITCODE" }
} finally {
    Pop-Location
}

Write-Output "Built $output"
