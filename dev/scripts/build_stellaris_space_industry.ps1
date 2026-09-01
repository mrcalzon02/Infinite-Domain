$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$project = Join-Path $root 'packdev\stellaris-space-industry'
$source = Join-Path $project 'src\main\java'
$resources = Join-Path $project 'src\main\resources'
$build = Join-Path $project 'build'
$classes = Join-Path $build 'classes'
$staging = Join-Path $build 'staging'
$dependencies = Join-Path $build 'dependencies'
$mods = Join-Path $root 'mods'
$output = Join-Path $mods 'infinite-domain-stellaris-industry-1.0.0.jar'

& 'C:\Users\Admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' (Join-Path $root 'scripts\generate_stellaris_space_industry.py')
if ($LASTEXITCODE -ne 0) { throw "Space-industry resource generation failed" }
& 'C:\Users\Admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' (Join-Path $root 'scripts\generate_alien_structures.py')
if ($LASTEXITCODE -ne 0) { throw "Alien-structure generation failed" }

$minecraftRoot = 'C:\Users\Admin\curseforge\minecraft\Install\libraries'
$dependencyPaths = @(
    (Join-Path $minecraftRoot 'net\minecraft\client\1.21.1-20240808.144430\client-1.21.1-20240808.144430-srg.jar'),
    (Join-Path $minecraftRoot 'net\neoforged\fancymodloader\loader\4.0.43\loader-4.0.43.jar'),
    (Join-Path $minecraftRoot 'net\neoforged\bus\8.0.5\bus-8.0.5.jar'),
    (Join-Path $minecraftRoot 'com\mojang\brigadier\1.3.10\brigadier-1.3.10.jar'),
    (Join-Path $minecraftRoot 'com\mojang\datafixerupper\8.0.16\datafixerupper-8.0.16.jar'),
    (Join-Path $minecraftRoot 'net\neoforged\neoforge\21.1.248\neoforge-21.1.248-universal.jar'),
    (Join-Path $minecraftRoot 'net\fabricmc\sponge-mixin\0.15.2+mixin.0.8.7\sponge-mixin-0.15.2+mixin.0.8.7.jar'),
    (Join-Path $mods 'architectury-13.0.11-neoforge.jar'),
    (Join-Path $mods 'potentials-neoforge-1.21-0.7.1.jar'),
    (Join-Path $mods 'stellaris-1.21-neoforge-1.4.25.jar')
)
$javac = 'C:\Program Files\Common Files\Oracle\Java\javapath\javac.exe'
$jar = 'C:\Program Files\Pylo\MCreator\jdk\bin\jar.exe'
foreach ($required in @($dependencyPaths + $javac + $jar)) {
    if (-not (Test-Path -LiteralPath $required)) { throw "Missing build dependency: $required" }
}

if (Test-Path -LiteralPath $build) { Remove-Item -LiteralPath $build -Recurse -Force }
New-Item -ItemType Directory -Path $classes, $staging, $dependencies -Force | Out-Null
$classpath = @()
foreach ($dependency in $dependencyPaths) {
    $copy = Join-Path $dependencies ([IO.Path]::GetFileName($dependency))
    Copy-Item -LiteralPath $dependency -Destination $copy -Force
    $classpath += $copy
}
$sources = Get-ChildItem -LiteralPath $source -Recurse -Filter '*.java' | Select-Object -ExpandProperty FullName
& $javac --release 21 -proc:none -classpath ($classpath -join ';') -d $classes $sources
if ($LASTEXITCODE -ne 0) { throw "javac failed with exit code $LASTEXITCODE" }
Copy-Item -Path (Join-Path $classes '*') -Destination $staging -Recurse -Force
Copy-Item -Path (Join-Path $resources '*') -Destination $staging -Recurse -Force
foreach ($old in Get-ChildItem -LiteralPath $mods -Filter 'infinite-domain-stellaris-industry-*.jar') { Remove-Item -LiteralPath $old.FullName -Force }
Push-Location $staging
try { & $jar --create --file $output .; if ($LASTEXITCODE -ne 0) { throw "jar failed with exit code $LASTEXITCODE" } } finally { Pop-Location }
Write-Output "Built $output"
