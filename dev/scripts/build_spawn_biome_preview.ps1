$ErrorActionPreference = 'Stop'

$instanceRoot = Split-Path -Parent $PSScriptRoot
$projectRoot = Join-Path $instanceRoot 'packdev\spawn-biome-preview'
$sourceRoot = Join-Path $projectRoot 'src\main\java'
$resourceRoot = Join-Path $projectRoot 'src\main\resources'
$buildRoot = Join-Path $projectRoot 'build'
$classRoot = Join-Path $buildRoot 'classes'
$stagingRoot = Join-Path $buildRoot 'staging'
$modsRoot = Join-Path $instanceRoot 'mods'
$outputJar = Join-Path $modsRoot 'infinite-domain-spawn-biome-preview-1.0.0.jar'

$minecraftLibraries = 'C:\Users\Admin\curseforge\minecraft\Install\libraries'
$dependencyPaths = @(
    (Join-Path $minecraftLibraries 'net\minecraft\client\1.21.1-20240808.144430\client-1.21.1-20240808.144430-srg.jar'),
    (Join-Path $minecraftLibraries 'net\neoforged\fancymodloader\loader\4.0.43\loader-4.0.43.jar'),
    (Join-Path $minecraftLibraries 'net\neoforged\bus\8.0.5\bus-8.0.5.jar'),
    (Join-Path $minecraftLibraries 'com\mojang\brigadier\1.3.10\brigadier-1.3.10.jar'),
    (Join-Path $minecraftLibraries 'com\mojang\datafixerupper\8.0.16\datafixerupper-8.0.16.jar'),
    (Join-Path $minecraftLibraries 'org\joml\joml\1.10.5\joml-1.10.5.jar'),
    (Join-Path $minecraftLibraries 'net\fabricmc\sponge-mixin\0.15.2+mixin.0.8.7\sponge-mixin-0.15.2+mixin.0.8.7.jar'),
    (Join-Path $minecraftLibraries 'net\neoforged\mergetool\2.0.7\mergetool-2.0.7-api.jar'),
    (Join-Path $minecraftLibraries 'net\neoforged\neoforge\21.1.248\neoforge-21.1.248-universal.jar')
)
$javac = 'C:\Program Files\Pylo\MCreator\jdk\bin\javac.exe'
$jarTool = 'C:\Program Files\Pylo\MCreator\jdk\bin\jar.exe'

foreach ($required in @($dependencyPaths + $javac + $jarTool)) {
    if (-not (Test-Path -LiteralPath $required)) { throw "Missing build dependency: $required" }
}

if (Test-Path -LiteralPath $buildRoot) { Remove-Item -LiteralPath $buildRoot -Recurse -Force }
New-Item -ItemType Directory -Path $classRoot, $stagingRoot -Force | Out-Null

$sources = Get-ChildItem -LiteralPath $sourceRoot -Recurse -Filter '*.java' | Select-Object -ExpandProperty FullName
& $javac --release 21 -proc:none -classpath ($dependencyPaths -join ';') -d $classRoot $sources
if ($LASTEXITCODE -ne 0) { throw "javac failed with exit code $LASTEXITCODE" }

$expectedClasses = @(
    (Join-Path $classRoot 'infinitedomain\biomepreview\SpawnBiomePreview.class'),
    (Join-Path $classRoot 'infinitedomain\biomepreview\BiomePreviewGenerator.class'),
    (Join-Path $classRoot 'infinitedomain\biomepreview\BiomePreviewServer.class'),
    (Join-Path $classRoot 'infinitedomain\biomepreview\PreviewPayload.class'),
    (Join-Path $classRoot 'infinitedomain\biomepreview\client\BiomePreviewClient.class'),
    (Join-Path $classRoot 'infinitedomain\biomepreview\mixin\PaintingRendererMixin.class')
)
foreach ($compiledClass in $expectedClasses) {
    if (-not (Test-Path -LiteralPath $compiledClass)) {
        throw "javac returned without producing required class: $compiledClass"
    }
}

Copy-Item -Path (Join-Path $classRoot '*') -Destination $stagingRoot -Recurse -Force
Copy-Item -Path (Join-Path $resourceRoot '*') -Destination $stagingRoot -Recurse -Force
foreach ($oldJar in Get-ChildItem -LiteralPath $modsRoot -Filter 'infinite-domain-spawn-biome-preview-*.jar') {
    Remove-Item -LiteralPath $oldJar.FullName -Force
}
Push-Location $stagingRoot
try {
    & $jarTool --create --file $outputJar .
    if ($LASTEXITCODE -ne 0) { throw "jar failed with exit code $LASTEXITCODE" }
} finally {
    Pop-Location
}
Write-Output "Built $outputJar"
