param(
    [string]$QuickPlayWorld = ''
)

$ErrorActionPreference = 'Stop'

$instance = Split-Path -Parent $PSScriptRoot
$install = 'C:\Users\Admin\curseforge\minecraft\Install'
$libraries = Join-Path $install 'libraries'
$base = Get-Content -LiteralPath (Join-Path $install 'versions\1.21.1\1.21.1.json') -Raw | ConvertFrom-Json
$forge = Get-Content -LiteralPath (Join-Path $install 'versions\neoforge-21.1.248\neoforge-21.1.248.json') -Raw | ConvertFrom-Json
$java = Join-Path $install 'java\Jre_21\bin\java.exe'
$natives = Join-Path $install 'natives\neoforge-21.1.248'

$classpath = [System.Collections.Generic.List[string]]::new()
foreach ($library in @($base.libraries) + @($forge.libraries)) {
    if ($null -ne $library.downloads.artifact.path) {
        $candidate = Join-Path $libraries ($library.downloads.artifact.path -replace '/', '\')
        if (Test-Path -LiteralPath $candidate) { $classpath.Add($candidate) }
    }
}
$gameJar = Join-Path $install 'versions\neoforge-21.1.248\neoforge-21.1.248.jar'
if (-not (Test-Path -LiteralPath $gameJar -PathType Leaf)) {
    throw "NeoForge game jar is missing: $gameJar"
}
$classpath.Add($gameJar)
$classpath = @($classpath | Select-Object -Unique)

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

$jvmArgs = @(
    '-Xms1G', '-Xmx8G',
    "-Djava.library.path=$natives", "-Djna.tmpdir=$natives",
    "-Dorg.lwjgl.system.SharedLibraryExtractPath=$natives", "-Dio.netty.native.workdir=$natives",
    '-Dminecraft.launcher.brand=codex-smoke-test', '-Dminecraft.launcher.version=1',
    '-Djava.net.preferIPv6Addresses=system', '-DignoreList=client-extra,neoforge-21.1.248.jar',
    "-DlibraryDirectory=$libraries", '-p', ($modulePath -join ';'), '--add-modules', 'ALL-MODULE-PATH',
    '--add-opens', 'java.base/java.util.jar=cpw.mods.securejarhandler',
    '--add-opens', 'java.base/java.lang.invoke=cpw.mods.securejarhandler',
    '--add-exports', 'java.base/sun.security.util=cpw.mods.securejarhandler',
    '--add-exports', 'jdk.naming.dns/com.sun.jndi.dns=java.naming',
    '-cp', ($classpath -join ';')
)

$gameArgs = @(
    '--username', 'CodexSmoke', '--version', 'neoforge-21.1.248', '--gameDir', $instance,
    '--assetsDir', (Join-Path $install 'assets'), '--assetIndex', '17',
    '--uuid', '00000000000000000000000000000001', '--accessToken', '0',
    '--clientId', '0', '--xuid', '0', '--userType', 'legacy', '--versionType', 'release',
    '--width', '1024', '--height', '768',
    '--fml.neoForgeVersion', '21.1.248', '--fml.fmlVersion', '4.0.43',
    '--fml.mcVersion', '1.21.1', '--fml.neoFormVersion', '20240808.144430',
    '--launchTarget', 'forgeclient'
)

if ($QuickPlayWorld) {
    $gameArgs += @('--quickPlaySingleplayer', $QuickPlayWorld)
}

& $java @jvmArgs 'cpw.mods.bootstraplauncher.BootstrapLauncher' @gameArgs
exit $LASTEXITCODE
