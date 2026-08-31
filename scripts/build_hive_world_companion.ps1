$ErrorActionPreference = 'Stop'

$instanceRoot = Split-Path -Parent $PSScriptRoot
$projectRoot = Join-Path $instanceRoot 'packdev\hive-world-companion'
$sourceRoot = Join-Path $projectRoot 'src\main\java'
$resourceRoot = Join-Path $projectRoot 'src\main\resources'
$buildRoot = Join-Path $projectRoot 'build'
$classRoot = Join-Path $buildRoot 'classes'
$stagingRoot = Join-Path $buildRoot 'staging'
$candidateJar = Join-Path $buildRoot 'infinite-domain-hive-world-companion-0.1.0.jar'
$modsRoot = Join-Path $instanceRoot 'mods'
$outputJar = Join-Path $modsRoot 'infinite-domain-hive-world-companion-0.1.0.jar'

$minecraftLibraries = 'C:\Users\Admin\curseforge\minecraft\Install\libraries'
$dependencyPaths = @(
    (Join-Path $minecraftLibraries 'net\minecraft\client\1.21.1-20240808.144430\client-1.21.1-20240808.144430-srg.jar'),
    (Join-Path $minecraftLibraries 'net\neoforged\fancymodloader\loader\4.0.43\loader-4.0.43.jar'),
    (Join-Path $minecraftLibraries 'net\neoforged\bus\8.0.5\bus-8.0.5.jar'),
    (Join-Path $minecraftLibraries 'com\mojang\brigadier\1.3.10\brigadier-1.3.10.jar'),
    (Join-Path $minecraftLibraries 'com\mojang\datafixerupper\8.0.16\datafixerupper-8.0.16.jar'),
    (Join-Path $minecraftLibraries 'net\neoforged\mergetool\2.0.7\mergetool-2.0.7-api.jar'),
    (Join-Path $minecraftLibraries 'org\joml\joml\1.10.5\joml-1.10.5.jar'),
    (Join-Path $minecraftLibraries 'net\neoforged\neoforge\21.1.248\neoforge-21.1.248-universal.jar')
)
$javac = 'C:\Program Files\Pylo\MCreator\jdk\bin\javac.exe'
$java = 'C:\Program Files\Pylo\MCreator\jdk\bin\java.exe'
$jarTool = 'C:\Program Files\Pylo\MCreator\jdk\bin\jar.exe'

foreach ($required in @($dependencyPaths + $javac + $java + $jarTool)) {
    if (-not (Test-Path -LiteralPath $required)) { throw "Missing build dependency: $required" }
}

if (Test-Path -LiteralPath $buildRoot) { Remove-Item -LiteralPath $buildRoot -Recurse -Force }
New-Item -ItemType Directory -Path $classRoot, $stagingRoot -Force | Out-Null

$sources = Get-ChildItem -LiteralPath $sourceRoot -Recurse -Filter '*.java' | Select-Object -ExpandProperty FullName
$compilerOutput = @(& $javac --release 21 -proc:none -classpath ($dependencyPaths -join ';') -d $classRoot $sources 2>&1)
$compilerExitCode = $LASTEXITCODE
$compilerOutput | ForEach-Object { Write-Output $_ }
$compilerTranscript = $compilerOutput -join "`n"
if ($compilerExitCode -ne 0 -or $compilerTranscript.Contains('An exception has occurred in the compiler')) {
    throw "javac failed or crashed (exit code $compilerExitCode)"
}

& $java -cp $classRoot infinitedomain.hiveworld.worldgen.HiveMacroLayoutSelfTest
if ($LASTEXITCODE -ne 0) { throw "Hive macro-layout self-test failed with exit code $LASTEXITCODE" }

Copy-Item -Path (Join-Path $classRoot '*') -Destination $stagingRoot -Recurse -Force
Copy-Item -Path (Join-Path $resourceRoot '*') -Destination $stagingRoot -Recurse -Force
Push-Location $stagingRoot
try {
    & $jarTool --create --file $candidateJar .
    if ($LASTEXITCODE -ne 0) { throw "jar failed with exit code $LASTEXITCODE" }
} finally {
    Pop-Location
}

$requiredEntries = @(
    'META-INF/neoforge.mods.toml',
    'infinitedomain/hiveworld/HiveWorldCompanion.class',
    'infinitedomain/hiveworld/client/HiveAtmosphereClient$HiveDimensionEffects.class',
    'infinitedomain/hiveworld/client/HiveCloudRenderer.class',
    'infinitedomain/hiveworld/client/HiveSulfurRain.class',
    'infinitedomain/hiveworld/client/LayeredFogProfile.class',
    'infinitedomain/hiveworld/worldgen/HiveDensityFunctions.class',
    'infinitedomain/hiveworld/worldgen/HiveMacroLayout.class',
    'infinitedomain/hiveworld/worldgen/HiveStackField.class',
    'infinitedomain/hiveworld/worldgen/HiveTrunkAxis.class'
)
$jarEntries = @(& $jarTool --list --file $candidateJar)
if ($LASTEXITCODE -ne 0) { throw "jar verification failed with exit code $LASTEXITCODE" }
$missingEntries = @($requiredEntries | Where-Object { $_ -notin $jarEntries })
if ($missingEntries.Count -gt 0) {
    throw "Candidate jar is incomplete: $($missingEntries -join ', ')"
}

# Do not remove the installed working artifact until compilation, packaging, and
# content verification have all succeeded.
Copy-Item -LiteralPath $candidateJar -Destination $outputJar -Force
foreach ($oldJar in Get-ChildItem -LiteralPath $modsRoot -Filter 'infinite-domain-hive-world-companion-*.jar') {
    if ($oldJar.FullName -ne $outputJar) {
        Remove-Item -LiteralPath $oldJar.FullName -Force
    }
}
$candidateHash = (Get-FileHash -LiteralPath $candidateJar -Algorithm SHA256).Hash
$installedHash = (Get-FileHash -LiteralPath $outputJar -Algorithm SHA256).Hash
if ($candidateHash -ne $installedHash) { throw 'Installed jar hash does not match the verified candidate' }
Write-Output "Built $outputJar"
