param(
    # Variant and Suite are validated against the matrix once it is loaded, not
    # by a ValidateSet here: a literal list in this attribute is a second copy of
    # the matrix's own keys, and it silently goes stale. Adding a variant to
    # worldgen_benchmark_matrix.json is meant to be the whole change.
    [string]$Variant = 'baseline',
    [string]$Suite = 'smoke',
    [ValidateRange(1, 20)]
    [int]$Repetitions = 1,
    [ValidateRange(4, 32)]
    [int]$MaxHeapGiB = 8,
    # Hard wall-clock cap per run. A smoke run on this pack takes about 7 minutes
    # (roughly 2 for mod loading, 3 for dimension construction, 1 for generation),
    # so 25 leaves generous headroom for the standard suite while still bounding a
    # wedged JVM. Raise it for long suites rather than removing the gate.
    [ValidateRange(2, 180)]
    [int]$RunTimeoutMinutes = 25,
    [string]$BatchId = '',
    [string]$ServerLauncherRoot = '',
    [switch]$ValidateLauncher,
    [switch]$KeepRuntime
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

# scripts live in dev/scripts/, so the instance root is two levels up
$instance = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$matrixPath = Join-Path $PSScriptRoot 'worldgen_benchmark_matrix.json'
$analyzer = Join-Path $PSScriptRoot 'analyze_worldgen_benchmark.py'
$serverModPolicyPath = Join-Path $PSScriptRoot 'worldgen_benchmark_server_mod_policy.json'
$matrix = Get-Content -LiteralPath $matrixPath -Raw | ConvertFrom-Json

$knownVariants = @($matrix.variants.PSObject.Properties.Name)
if ($knownVariants -notcontains $Variant) {
    throw "Unknown variant '$Variant'. The matrix defines: $($knownVariants -join ', ')"
}
$knownSuites = @($matrix.suites.PSObject.Properties.Name)
if ($knownSuites -notcontains $Suite) {
    throw "Unknown suite '$Suite'. The matrix defines: $($knownSuites -join ', ')"
}
$serverModPolicy = Get-Content -LiteralPath $serverModPolicyPath -Raw | ConvertFrom-Json
$neoForgeVersion = '21.1.248'
$runsRoot = [IO.Path]::GetFullPath((Join-Path $instance 'benchmark_runs'))
if (-not $ServerLauncherRoot) {
    $ServerLauncherRoot = Join-Path $runsRoot ".launcher-cache\neoforge-$neoForgeVersion-server"
}
$ServerLauncherRoot = [IO.Path]::GetFullPath($ServerLauncherRoot)

if (-not $BatchId) {
    $BatchId = '{0}_{1}_{2}' -f (Get-Date -Format 'yyyyMMdd-HHmmss'), $Variant, $Suite
}
if ($BatchId -notmatch '^[A-Za-z0-9._-]+$') {
    throw 'BatchId may contain only letters, digits, dots, underscores, and hyphens.'
}

$batchRoot = [IO.Path]::GetFullPath((Join-Path $runsRoot $BatchId))
if (-not $batchRoot.StartsWith($runsRoot + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
    throw 'Resolved batch directory escaped benchmark_runs.'
}
if (Test-Path -LiteralPath $batchRoot) {
    throw "Benchmark batch already exists: $batchRoot"
}
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

function New-IsolatedServerLibraries {
    param([string]$RuntimeRoot, [string]$LauncherRoot)
    $sourceRoot = Join-Path $LauncherRoot 'libraries'
    $destinationRoot = Join-Path $RuntimeRoot 'libraries'
    New-Item -ItemType Directory -Path $destinationRoot | Out-Null
    foreach ($source in Get-ChildItem -LiteralPath $sourceRoot -Recurse -File) {
        $relative = $source.FullName.Substring($sourceRoot.Length).TrimStart('\')
        $destination = Resolve-RuntimePath $RuntimeRoot (Join-Path 'libraries' $relative)
        $parent = Split-Path -Parent $destination
        if (-not (Test-Path -LiteralPath $parent)) {
            New-Item -ItemType Directory -Path $parent -Force | Out-Null
        }
        # Some Maven coordinates exceed legacy MAX_PATH once nested beneath a
        # descriptive batch ID. PowerShell's hard-link provider accepts the
        # Win32 extended-path prefix while Java consumes the ordinary path.
        $extendedDestination = '\\?\' + $destination
        $extendedSource = '\\?\' + $source.FullName
        New-Item -ItemType HardLink -Path $extendedDestination -Target $extendedSource | Out-Null
    }
}

function Test-IsolatedServerLibraries {
    param([string]$LauncherRoot)
    $testRoot = [IO.Path]::GetFullPath((Join-Path $runsRoot ('.launcher-isolation-validation-' + ('x' * 48))))
    if (-not $testRoot.StartsWith($runsRoot + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
        throw 'Resolved launcher-isolation validation directory escaped benchmark_runs.'
    }
    if (Test-Path -LiteralPath $testRoot) {
        throw "Launcher-isolation validation directory already exists: $testRoot"
    }
    New-Item -ItemType Directory -Path $testRoot | Out-Null
    try {
        New-IsolatedServerLibraries $testRoot $LauncherRoot
        $sourceRoot = Join-Path $LauncherRoot 'libraries'
        $sourceFiles = @(Get-ChildItem -LiteralPath $sourceRoot -Recurse -File)
        $destinationFiles = @(Get-ChildItem -LiteralPath (Join-Path $testRoot 'libraries') -Recurse -File)
        if ($sourceFiles.Count -ne $destinationFiles.Count) {
            throw "Isolated launcher copied $($destinationFiles.Count) of $($sourceFiles.Count) server-library files"
        }
        $missing = @($sourceFiles | Where-Object {
            $relative = $_.FullName.Substring($sourceRoot.Length).TrimStart('\')
            -not (Test-Path -LiteralPath (Join-Path (Join-Path $testRoot 'libraries') $relative) -PathType Leaf)
        })
        if ($missing.Count -gt 0) {
            throw "Isolated launcher is missing $($missing.Count) server-library file(s)"
        }
        $longestPath = ($destinationFiles | Sort-Object { $_.FullName.Length } -Descending | Select-Object -First 1).FullName.Length
        if ($longestPath -lt 260) {
            throw "Launcher-isolation validation did not exercise an extended-length path (longest: $longestPath)"
        }
        return [pscustomobject]@{ files = $destinationFiles.Count; longestPath = $longestPath }
    } finally {
        if (Test-Path -LiteralPath $testRoot) {
            Remove-Item -LiteralPath $testRoot -Recurse -Force
        }
    }
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
    param([string]$RuntimeRoot, [object[]]$OmitPatterns, [object]$ServerModPolicy)
    $destination = Join-Path $RuntimeRoot 'mods'
    New-Item -ItemType Directory -Path $destination | Out-Null
    $sourceMods = @(Get-ChildItem -LiteralPath (Join-Path $instance 'mods') -Filter '*.jar' -File | Sort-Object Name)
    $omitted = [Collections.Generic.List[object]]::new()
    foreach ($entry in @($ServerModPolicy.exclusions)) {
        $matches = @($sourceMods | Where-Object { $_.Name -like [string]$entry.pattern })
        if ($matches.Count -ne 1) {
            throw "Dedicated-server exclusion '$($entry.pattern)' matched $($matches.Count) mod jars; expected exactly one"
        }
    }
    foreach ($mod in $sourceMods) {
        $omit = $false
        $source = ''
        $reason = ''
        foreach ($entry in @($ServerModPolicy.exclusions)) {
            if ($mod.Name -like [string]$entry.pattern) {
                $omit = $true
                $source = 'dedicated_server_policy'
                $reason = [string]$entry.reason
                break
            }
        }
        foreach ($pattern in $OmitPatterns) {
            if ($mod.Name -like [string]$pattern) {
                $omit = $true
                $source = 'benchmark_variant'
                $reason = "variant pattern: $pattern"
                break
            }
        }
        if (-not $omit) {
            New-Item -ItemType HardLink -Path (Join-Path $destination $mod.Name) -Target $mod.FullName | Out-Null
        } else {
            $omitted.Add([pscustomobject]@{ name = $mod.Name; source = $source; reason = $reason })
        }
    }
    return [pscustomobject]@{
        included = @(Get-ChildItem -LiteralPath $destination -Filter '*.jar' -File | Sort-Object Name)
        omitted = @($omitted)
    }
}

function Get-ConfigurationEntries {
    param([string]$RuntimeRoot)
    $resolvedRuntimeRoot = [IO.Path]::GetFullPath($RuntimeRoot)
    $roots = [Collections.Generic.List[string]]::new()
    foreach ($fixed in @(
        'config/lostcities',
        'config/lostcities-server.toml',
        'defaultconfigs/lostcities-server.toml',
        'kubejs/server_scripts/worldgen_benchmark.js',
        'datapacks'
    )) { $roots.Add($fixed) | Out-Null }

    # Worldgen-relevant pack data, for every namespace rather than a hardcoded
    # two. The fingerprint exists so two runs cannot be compared unless they were
    # generated from the same configuration, and it was previously narrow enough
    # to miss changes that demonstrably alter terrain: on 2026-09-01 two runs
    # whose biome modifiers differed - changing feature order and doubling an
    # ore's density - recorded the identical fingerprint f9eb512d. Biome
    # modifiers and biome tags decide which features reach which biome, and the
    # Lost Cities asset registries decide what its cities are built from, so all
    # three belong in the hash. A false "different" only blocks a comparison; a
    # false "same" silently authorises an invalid one.
    $namespaceSubpaths = @(
        'worldgen',
        'tags/worldgen',
        'neoforge/biome_modifier',
        'lostcities',
        'dimension',
        'dimension_type'
    )
    $dataRoot = Resolve-RuntimePath $RuntimeRoot 'kubejs/data'
    if (Test-Path -LiteralPath $dataRoot -PathType Container) {
        foreach ($namespace in Get-ChildItem -LiteralPath $dataRoot -Directory) {
            foreach ($subpath in $namespaceSubpaths) {
                $candidate = Join-Path $namespace.FullName ($subpath -replace '/', '\')
                if (Test-Path -LiteralPath $candidate) {
                    $roots.Add("kubejs/data/$($namespace.Name)/$subpath") | Out-Null
                }
            }
        }
    }

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
    param([string]$LauncherRoot)
    $install = 'C:\Users\Admin\curseforge\minecraft\Install'
    $java = Join-Path $install 'java\Jre_21\bin\java.exe'
    $argumentRelative = "libraries/net/neoforged/neoforge/$neoForgeVersion/win_args.txt"
    $argumentFile = Join-Path $LauncherRoot ($argumentRelative -replace '/', '\')
    $serverJar = Join-Path $LauncherRoot "libraries\net\neoforged\neoforge\$neoForgeVersion\neoforge-$neoForgeVersion-server.jar"
    $bootstrap = Join-Path $PSScriptRoot 'bootstrap_worldgen_benchmark_server.ps1'
    if (-not (Test-Path -LiteralPath $java -PathType Leaf)) {
        throw "Java 21 runtime is missing: $java"
    }
    if (-not (Test-Path -LiteralPath $argumentFile -PathType Leaf) -or -not (Test-Path -LiteralPath $serverJar -PathType Leaf)) {
        throw "The official NeoForge dedicated-server runtime is missing or incomplete at $LauncherRoot. Run: .\scripts\bootstrap_worldgen_benchmark_server.ps1"
    }
    $argumentText = Get-Content -LiteralPath $argumentFile -Raw
    foreach ($required in @(
        '-DlegacyClassPath=',
        'cpw.mods.bootstraplauncher.BootstrapLauncher',
        '--launchTarget forgeserver',
        "--fml.neoForgeVersion $neoForgeVersion",
        '--fml.mcVersion 1.21.1'
    )) {
        if (-not $argumentText.Contains($required)) {
            throw "NeoForge server argument file is missing '$required': $argumentFile. Repair it with $bootstrap"
        }
    }
    $libraryReferences = @([regex]::Matches($argumentText, 'libraries/[A-Za-z0-9_.+@/-]+\.jar') | ForEach-Object { $_.Value } | Sort-Object -Unique)
    $missingLibraries = @($libraryReferences | Where-Object {
        -not (Test-Path -LiteralPath (Join-Path $LauncherRoot ($_ -replace '/', '\')) -PathType Leaf)
    })
    if ($missingLibraries.Count -gt 0) {
        throw "NeoForge server runtime is missing $($missingLibraries.Count) referenced library file(s). Repair it with $bootstrap"
    }
    return [pscustomobject]@{
        java = $java
        root = $LauncherRoot
        argumentRelative = $argumentRelative
        argumentFile = $argumentFile
        argumentFileSha256 = (Get-FileHash -LiteralPath $argumentFile -Algorithm SHA256).Hash.ToLowerInvariant()
        serverJarSha256 = (Get-FileHash -LiteralPath $serverJar -Algorithm SHA256).Hash.ToLowerInvariant()
        referencedLibraries = $libraryReferences.Count
    }
}

& python $analyzer validate-matrix --matrix $matrixPath
if ($LASTEXITCODE -ne 0) {
    throw 'Benchmark matrix validation failed.'
}

$launcher = Get-Launcher $ServerLauncherRoot
if ($ValidateLauncher) {
    $isolation = Test-IsolatedServerLibraries $launcher.root
    Write-Host "NeoForge $neoForgeVersion dedicated-server launcher is valid."
    Write-Host "Root: $($launcher.root)"
    Write-Host "Referenced libraries: $($launcher.referencedLibraries)"
    Write-Host "Isolated library files: $($isolation.files); longest exercised path: $($isolation.longestPath) characters"
    exit 0
}
New-Item -ItemType Directory -Path $batchRoot | Out-Null
$variantConfig = $matrix.variants.$Variant
$suiteTiles = @($matrix.suites.$Suite)

for ($repetition = 1; $repetition -le $Repetitions; $repetition++) {
    $runId = '{0}-r{1:d2}' -f $BatchId, $repetition
    $runRoot = Join-Path $batchRoot $runId
    $runtime = Join-Path $runRoot 'runtime'
    New-Item -ItemType Directory -Path $runtime | Out-Null
    New-IsolatedServerLibraries $runtime $launcher.root

    foreach ($directory in @('config', 'defaultconfigs', 'kubejs', 'datapacks')) {
        Copy-IsolatedDirectory $directory $runtime
    }
    $omitMods = @()
    if ($null -ne $variantConfig -and $null -ne $variantConfig.PSObject.Properties['omitMods']) {
        $omitMods = @($variantConfig.omitMods)
    }
    $stagedMods = New-IsolatedModDirectory $runtime $omitMods $serverModPolicy

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

    $benchmarkWorldName = [string]$matrix.worldName
    $worldDatapacks = Join-Path $runtime (Join-Path $benchmarkWorldName 'datapacks')
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
level-name=$benchmarkWorldName
level-seed=$($matrix.seed)
level-type=minecraft:normal
max-players=1
max-tick-time=-1
motd=Infinite Domain automated worldgen benchmark
online-mode=false
server-port=0
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
        launcher = [ordered]@{
            neoForgeVersion = $neoForgeVersion
            argumentFileSha256 = $launcher.argumentFileSha256
            serverJarSha256 = $launcher.serverJarSha256
            referencedLibraries = $launcher.referencedLibraries
        }
        serverModPolicy = [ordered]@{
            path = 'scripts/worldgen_benchmark_server_mod_policy.json'
            sha256 = (Get-FileHash -LiteralPath $serverModPolicyPath -Algorithm SHA256).Hash.ToLowerInvariant()
            omitted = @($stagedMods.omitted)
        }
        configurationFingerprint = $configurationFingerprint
        configurationFiles = $configurationEntries
        mods = @($stagedMods.included | ForEach-Object {
            [ordered]@{ name = $_.Name; bytes = $_.Length }
        })
        plan = $plan
    }
    $manifestPath = Join-Path $runRoot 'manifest.json'
    [IO.File]::WriteAllText($manifestPath, ($manifest | ConvertTo-Json -Depth 12), [Text.UTF8Encoding]::new($false))

    $jvmArgs = @(
        '-Xms2G', "-Xmx${MaxHeapGiB}G"
    )
    $argumentFile = '@' + $launcher.argumentRelative

    Write-Host "Starting fixed-seed benchmark $runId (hard cap ${RunTimeoutMinutes}m) ..."
    $consoleLog = Join-Path $runRoot 'server-console.log'
    $consoleErrorLog = Join-Path $runRoot 'server-console.err.log'

    # The server is launched detached and waited on with a deadline. It used to be
    # invoked as `& java ... | Tee-Object`, which blocks with no timeout at all:
    # the tileTimeoutSeconds gate lives inside the KubeJS controller, so it only
    # protects a run that reached chunk generation. A JVM that wedges earlier -
    # during mod loading or the ~3 minute dimension-construction block - was never
    # bounded by anything and would hold the batch indefinitely.
    $serverProcess = Start-Process -FilePath $launcher.java `
        -ArgumentList (@($jvmArgs) + @($argumentFile, 'nogui')) `
        -WorkingDirectory $runtime `
        -RedirectStandardOutput $consoleLog `
        -RedirectStandardError $consoleErrorLog `
        -NoNewWindow -PassThru

    # Windows PowerShell 5.1 returns a Process from Start-Process -PassThru whose
    # ExitCode stays $null even after WaitForExit, because it does not enable
    # process exit events. Setting this before the process exits makes the exit
    # code readable; without it every run fails with "exited with code ." since
    # $null -ne 0. Verified against a child returning a known non-zero code.
    $serverProcess.EnableRaisingEvents = $true

    $runTimeoutMs = $RunTimeoutMinutes * 60 * 1000
    if (-not $serverProcess.WaitForExit($runTimeoutMs)) {
        try { Stop-Process -Id $serverProcess.Id -Force -ErrorAction Stop } catch {
            Write-Warning "Could not kill benchmark server PID $($serverProcess.Id): $_"
        }
        # Give the kill a moment so the exit code below is readable.
        $serverProcess.WaitForExit(15000) | Out-Null
        throw "Benchmark server for $runId exceeded the ${RunTimeoutMinutes}-minute hard cap and was killed. Inspect $consoleLog and $(Join-Path $runtime 'logs\latest.log'); runtime retained at $runtime"
    }
    $serverExitCode = $serverProcess.ExitCode

    # Start-Process cannot merge the two streams into one file, so fold stderr
    # back into the console log that the existing diagnosis flow reads.
    if ((Test-Path -LiteralPath $consoleErrorLog) -and (Get-Item -LiteralPath $consoleErrorLog).Length -gt 0) {
        Add-Content -LiteralPath $consoleLog -Value "--- stderr ---"
        Get-Content -LiteralPath $consoleErrorLog | Add-Content -LiteralPath $consoleLog
    }

    $latestLog = Join-Path $runtime 'logs\latest.log'
    if (-not (Test-Path -LiteralPath $latestLog)) {
        throw "Benchmark server produced no latest.log (exit code $serverExitCode). Inspect $consoleLog; runtime retained at $runtime"
    }
    Copy-Item -LiteralPath $latestLog -Destination (Join-Path $runRoot 'latest.log')
    if ($serverExitCode -ne 0) {
        throw "Benchmark server exited with code $serverExitCode. Inspect $consoleLog and $(Join-Path $runRoot 'latest.log'); runtime retained at $runtime"
    }
    $resultPath = Join-Path $runRoot 'result.json'
    & python $analyzer analyze --log (Join-Path $runRoot 'latest.log') --manifest $manifestPath --output $resultPath
    $analysisExitCode = $LASTEXITCODE
    if ($analysisExitCode -ne 0) {
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
