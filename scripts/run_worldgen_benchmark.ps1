param(
    [ValidateSet('baseline', 'optimized_heightmap', 'height_sample_6', 'no_adjacent_avoidance', 'no_abyssal_structures', 'no_custom_structures', 'no_gradient_ocean', 'no_lostcities')]
    [string]$Variant = 'baseline',
    [ValidateSet('smoke', 'standard', 'terrain')]
    [string]$Suite = 'smoke',
    [ValidateRange(1, 20)]
    [int]$Repetitions = 1,
    [ValidateRange(4, 32)]
    [int]$MaxHeapGiB = 8,
    [string]$BatchId = '',
    [switch]$KeepRuntime
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$instance = Split-Path -Parent $PSScriptRoot
$matrixPath = Join-Path $PSScriptRoot 'worldgen_benchmark_matrix.json'
$analyzer = Join-Path $PSScriptRoot 'analyze_worldgen_benchmark.py'
$matrix = Get-Content -LiteralPath $matrixPath -Raw | ConvertFrom-Json

if (-not $BatchId) {
    $BatchId = '{0}_{1}_{2}' -f (Get-Date -Format 'yyyyMMdd-HHmmss'), $Variant, $Suite
}
if ($BatchId -notmatch '^[A-Za-z0-9._-]+$') {
    throw 'BatchId may contain only letters, digits, dots, underscores, and hyphens.'
}

$runsRoot = [IO.Path]::GetFullPath((Join-Path $instance 'benchmark_runs'))
$batchRoot = [IO.Path]::GetFullPath((Join-Path $runsRoot $BatchId))
if (-not $batchRoot.StartsWith($runsRoot + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
    throw 'Resolved batch directory escaped benchmark_runs.'
}
if (Test-Path -LiteralPath $batchRoot) {
    throw "Benchmark batch already exists: $batchRoot"
}
New-Item -ItemType Directory -Path $batchRoot | Out-Null

function Resolve-RuntimePath {
    param([string]$RuntimeRoot, [string]$RelativePath)
    $resolvedRoot = [IO.Path]::GetFullPath($RuntimeRoot)
    $nativeRelative = $RelativePath -replace '/', [IO.Path]::DirectorySeparatorChar
    $resolved = [IO.Path]::GetFullPath((Join-Path $resolvedRoot $nativeRelative))
    if (-not $resolved.StartsWith($resolvedRoot + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Variant path escaped the isolated runtime: $RelativePath"
    }
    return $resolved
}

function Set-IsolatedTomlValue {
    param([string]$RuntimeRoot, [string]$RelativePath, [string]$Key, [string]$Value)
    $target = Resolve-RuntimePath $RuntimeRoot $RelativePath
    if (-not (Test-Path -LiteralPath $target -PathType Leaf)) {
        throw "Variant TOML target does not exist: $RelativePath"
    }
    $content = Get-Content -LiteralPath $target -Raw
    $pattern = '(?m)^(\s*' + [Regex]::Escape($Key) + '\s*=\s*).*$'
    $regex = [Regex]::new($pattern)
    if ($regex.Matches($content).Count -ne 1) {
        throw "Expected exactly one $Key entry in $RelativePath"
    }
    $updated = $regex.Replace($content, { param($match) $match.Groups[1].Value + $Value }, 1)
    [IO.File]::WriteAllText($target, $updated, [Text.UTF8Encoding]::new($false))
}

function Copy-IsolatedDirectory {
    param([string]$Name, [string]$RuntimeRoot)
    $source = Join-Path $instance $Name
    if (Test-Path -LiteralPath $source) {
        Copy-Item -LiteralPath $source -Destination (Join-Path $RuntimeRoot $Name) -Recurse
    }
}

function New-IsolatedModDirectory {
    param([string]$RuntimeRoot, [object[]]$OmitPatterns)
    $destination = Join-Path $RuntimeRoot 'mods'
    New-Item -ItemType Directory -Path $destination | Out-Null
    foreach ($mod in Get-ChildItem -LiteralPath (Join-Path $instance 'mods') -File) {
        $omit = $false
        foreach ($pattern in $OmitPatterns) {
            if ($mod.Name -like [string]$pattern) {
                $omit = $true
                break
            }
        }
        if (-not $omit) {
            New-Item -ItemType HardLink -Path (Join-Path $destination $mod.Name) -Target $mod.FullName | Out-Null
        }
    }
}

function Get-ConfigurationEntries {
    param([string]$RuntimeRoot)
    $resolvedRuntimeRoot = [IO.Path]::GetFullPath($RuntimeRoot)
    $roots = @(
        'config/lostcities',
        'config/lostcities-server.toml',
        'defaultconfigs/lostcities-server.toml',
        'kubejs/data/infinite_domain/worldgen',
        'kubejs/data/minecraft/worldgen',
        'kubejs/server_scripts/worldgen_benchmark.js',
        'datapacks'
    )
    $files = [Collections.Generic.List[IO.FileInfo]]::new()
    foreach ($relative in $roots) {
        $target = Resolve-RuntimePath $RuntimeRoot $relative
        if (Test-Path -LiteralPath $target -PathType Leaf) {
            $files.Add((Get-Item -LiteralPath $target))
        } elseif (Test-Path -LiteralPath $target -PathType Container) {
            foreach ($file in Get-ChildItem -LiteralPath $target -Recurse -File) {
                $files.Add($file)
            }
        }
    }
    return @($files | Sort-Object FullName -Unique | ForEach-Object {
        $relativePath = $_.FullName.Substring($resolvedRuntimeRoot.Length).TrimStart('\')
        [pscustomobject]@{
            path = $relativePath.Replace('\', '/')
            bytes = $_.Length
            sha256 = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
        }
    })
}

function Get-Launcher {
    $install = 'C:\Users\Admin\curseforge\minecraft\Install'
    $libraries = Join-Path $install 'libraries'
    $base = Get-Content -LiteralPath (Join-Path $install 'versions\1.21.1\1.21.1.json') -Raw | ConvertFrom-Json
    $forge = Get-Content -LiteralPath (Join-Path $install 'versions\neoforge-21.1.248\neoforge-21.1.248.json') -Raw | ConvertFrom-Json
    $classpath = [Collections.Generic.List[string]]::new()
    foreach ($library in @($base.libraries) + @($forge.libraries)) {
        if ($null -ne $library.downloads.artifact.path) {
            $candidate = Join-Path $libraries ($library.downloads.artifact.path -replace '/', '\')
            if (Test-Path -LiteralPath $candidate) {
                $classpath.Add($candidate)
            }
        }
    }
    $modulePath = @(
        'cpw\mods\bootstraplauncher\2.0.2\bootstraplauncher-2.0.2.jar',
        'cpw\mods\securejarhandler\3.0.8\securejarhandler-3.0.8.jar',
        'org\ow2\asm\asm-commons\9.10.1\asm-commons-9.10.1.jar',
        'org\ow2\asm\asm-util\9.10.1\asm-util-9.10.1.jar',
        'org\ow2\asm\asm-analysis\9.10.1\asm-analysis-9.10.1.jar',
        'org\ow2\asm\asm-tree\9.10.1\asm-tree-9.10.1.jar',
        'org\ow2\asm\asm\9.10.1\asm-9.10.1.jar',
        'net\neoforged\JarJarFileSystems\0.4.1\JarJarFileSystems-0.4.1.jar'
    ) | ForEach-Object { Join-Path $libraries $_ }
    return [pscustomobject]@{
        java = Join-Path $install 'java\Jre_21\bin\java.exe'
        libraries = $libraries
        classpath = @($classpath | Select-Object -Unique)
        modulePath = $modulePath
    }
}

& python $analyzer validate-matrix --matrix $matrixPath
if ($LASTEXITCODE -ne 0) {
    throw 'Benchmark matrix validation failed.'
}

$launcher = Get-Launcher
$variantConfig = $matrix.variants.$Variant
$suiteTiles = @($matrix.suites.$Suite)

for ($repetition = 1; $repetition -le $Repetitions; $repetition++) {
    $runId = '{0}-r{1:d2}' -f $BatchId, $repetition
    $runRoot = Join-Path $batchRoot $runId
    $runtime = Join-Path $runRoot 'runtime'
    New-Item -ItemType Directory -Path $runtime | Out-Null

    foreach ($directory in @('config', 'defaultconfigs', 'kubejs', 'datapacks')) {
        Copy-IsolatedDirectory $directory $runtime
    }
    $omitMods = @()
    if ($null -ne $variantConfig -and $null -ne $variantConfig.PSObject.Properties['omitMods']) {
        $omitMods = @($variantConfig.omitMods)
    }
    New-IsolatedModDirectory $runtime $omitMods

    if ($null -ne $variantConfig -and $null -ne $variantConfig.PSObject.Properties['toml']) {
        foreach ($edit in @($variantConfig.toml)) {
            Set-IsolatedTomlValue $runtime ([string]$edit.path) ([string]$edit.key) ([string]$edit.value)
        }
    }
    if ($null -ne $variantConfig -and $null -ne $variantConfig.PSObject.Properties['remove']) {
        foreach ($relative in @($variantConfig.remove)) {
            $target = Resolve-RuntimePath $runtime ([string]$relative)
            if (Test-Path -LiteralPath $target) {
                Remove-Item -LiteralPath $target -Recurse -Force
            }
        }
    }

    $plan = [ordered]@{
        enabled = $true
        runId = $runId
        variant = $Variant
        suite = $Suite
        worldName = [string]$matrix.worldName
        seed = [string]$matrix.seed
        warmupTicks = [int]$matrix.defaults.warmupTicks
        cooldownTicks = [int]$matrix.defaults.cooldownTicks
        pollIntervalTicks = [int]$matrix.defaults.pollIntervalTicks
        tileTimeoutSeconds = [int]$matrix.defaults.tileTimeoutSeconds
        stopServerWhenComplete = $true
        tiles = $suiteTiles
    }
    $planPath = Join-Path $runtime 'kubejs\config\worldgen_benchmark.json'
    [IO.File]::WriteAllText($planPath, ($plan | ConvertTo-Json -Depth 8), [Text.UTF8Encoding]::new($false))

    $worldDatapacks = Join-Path $runtime 'world\datapacks'
    New-Item -ItemType Directory -Path $worldDatapacks -Force | Out-Null
    $globalDatapacks = Join-Path $runtime 'datapacks'
    if (Test-Path -LiteralPath $globalDatapacks) {
        foreach ($pack in Get-ChildItem -LiteralPath $globalDatapacks) {
            Copy-Item -LiteralPath $pack.FullName -Destination $worldDatapacks -Recurse
        }
    }

    $serverProperties = @"
allow-flight=true
difficulty=peaceful
enable-command-block=false
enable-jmx-monitoring=false
enable-query=false
enable-rcon=false
enable-status=false
enforce-secure-profile=false
gamemode=spectator
generate-structures=true
level-name=world
level-seed=$($matrix.seed)
level-type=minecraft:normal
max-players=1
max-tick-time=-1
motd=Infinite Domain automated worldgen benchmark
online-mode=false
simulation-distance=2
spawn-protection=0
sync-chunk-writes=true
view-distance=2
white-list=true
"@
    [IO.File]::WriteAllText((Join-Path $runtime 'server.properties'), $serverProperties, [Text.UTF8Encoding]::new($false))
    [IO.File]::WriteAllText((Join-Path $runtime 'eula.txt'), "eula=true`n", [Text.UTF8Encoding]::new($false))

    $configurationEntries = Get-ConfigurationEntries $runtime
    $fingerprintText = ($configurationEntries | ForEach-Object { "$($_.path)|$($_.bytes)|$($_.sha256)" }) -join "`n"
    $fingerprintBytes = [Text.Encoding]::UTF8.GetBytes($fingerprintText)
    $sha = [Security.Cryptography.SHA256]::Create()
    try {
        $configurationFingerprint = ([BitConverter]::ToString($sha.ComputeHash($fingerprintBytes))).Replace('-', '').ToLowerInvariant()
    } finally {
        $sha.Dispose()
    }
    $gitHead = (& git -C $instance rev-parse HEAD 2>$null)
    $manifest = [ordered]@{
        schemaVersion = 1
        batchId = $BatchId
        runId = $runId
        repetition = $repetition
        variant = $Variant
        suite = $Suite
        seed = [string]$matrix.seed
        worldName = [string]$matrix.worldName
        maxHeapGiB = $MaxHeapGiB
        createdUtc = [DateTime]::UtcNow.ToString('o')
        gitHead = [string]$gitHead
        configurationFingerprint = $configurationFingerprint
        configurationFiles = $configurationEntries
        mods = @(Get-ChildItem -LiteralPath (Join-Path $runtime 'mods') -File | Sort-Object Name | ForEach-Object {
            [ordered]@{ name = $_.Name; bytes = $_.Length }
        })
        plan = $plan
    }
    $manifestPath = Join-Path $runRoot 'manifest.json'
    [IO.File]::WriteAllText($manifestPath, ($manifest | ConvertTo-Json -Depth 12), [Text.UTF8Encoding]::new($false))

    $jvmArgs = @(
        '-Xms2G', "-Xmx${MaxHeapGiB}G",
        '-Djava.net.preferIPv6Addresses=system', '-DignoreList=client-extra,neoforge-21.1.248.jar',
        "-DlibraryDirectory=$($launcher.libraries)", '-p', ($launcher.modulePath -join ';'), '--add-modules', 'ALL-MODULE-PATH',
        '--add-opens', 'java.base/java.util.jar=cpw.mods.securejarhandler',
        '--add-opens', 'java.base/java.lang.invoke=cpw.mods.securejarhandler',
        '--add-exports', 'java.base/sun.security.util=cpw.mods.securejarhandler',
        '--add-exports', 'jdk.naming.dns/com.sun.jndi.dns=java.naming',
        '-cp', ($launcher.classpath -join ';')
    )
    $gameArgs = @(
        '--fml.neoForgeVersion', '21.1.248', '--fml.fmlVersion', '4.0.43',
        '--fml.mcVersion', '1.21.1', '--fml.neoFormVersion', '20240808.144430',
        '--launchTarget', 'forgeserver', 'nogui'
    )

    Write-Host "Starting fixed-seed benchmark $runId ..."
    $consoleLog = Join-Path $runRoot 'server-console.log'
    Push-Location $runtime
    try {
        & $launcher.java @jvmArgs 'cpw.mods.bootstraplauncher.BootstrapLauncher' @gameArgs 2>&1 | Tee-Object -FilePath $consoleLog
        $serverExitCode = $LASTEXITCODE
    } finally {
        Pop-Location
    }

    $latestLog = Join-Path $runtime 'logs\latest.log'
    if (-not (Test-Path -LiteralPath $latestLog)) {
        throw "Benchmark server produced no latest.log (exit code $serverExitCode). Runtime retained at $runtime"
    }
    Copy-Item -LiteralPath $latestLog -Destination (Join-Path $runRoot 'latest.log')
    $resultPath = Join-Path $runRoot 'result.json'
    & python $analyzer analyze --log (Join-Path $runRoot 'latest.log') --manifest $manifestPath --output $resultPath
    $analysisExitCode = $LASTEXITCODE
    if ($serverExitCode -ne 0 -or $analysisExitCode -ne 0) {
        throw "Benchmark $runId failed. Runtime retained at $runtime"
    }

    if (-not $KeepRuntime) {
        $resolvedRuntime = [IO.Path]::GetFullPath($runtime)
        $resolvedRunRoot = [IO.Path]::GetFullPath($runRoot)
        if (-not $resolvedRuntime.StartsWith($resolvedRunRoot + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
            throw 'Refusing to clean a runtime outside its exact run directory.'
        }
        Remove-Item -LiteralPath $resolvedRuntime -Recurse -Force
    }
}

$summaryCsv = Join-Path $batchRoot 'summary.csv'
$summaryJson = Join-Path $batchRoot 'summary.json'
& python $analyzer aggregate --root $batchRoot --csv $summaryCsv --json $summaryJson
if ($LASTEXITCODE -ne 0) {
    throw 'Benchmark aggregation failed.'
}
Write-Host "Benchmark batch complete: $summaryCsv"
