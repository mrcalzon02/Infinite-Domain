$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$minecraftJar = 'C:\Users\Admin\curseforge\minecraft\Install\versions\1.21.1\1.21.1.jar'
$entityOutput = Join-Path $root 'packdev\darknet-worldgen-patch\src\main\resources\assets\infinite_domain\textures\entity\darknet'
$foliageOutput = Join-Path $root 'kubejs\assets\kubejs\textures\block'

if (-not (Test-Path -LiteralPath $minecraftJar)) {
    throw "Missing installed Minecraft texture source: $minecraftJar"
}

New-Item -ItemType Directory -Path $entityOutput, $foliageOutput -Force | Out-Null
Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName System.IO.Compression.FileSystem

function Convert-DarknetTexture {
    param(
        [System.Drawing.Bitmap]$Source,
        [int]$Seed,
        [string]$Destination
    )

    $target = [System.Drawing.Bitmap]::new($Source.Width, $Source.Height, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
    try {
        for ($y = 0; $y -lt $Source.Height; $y++) {
            for ($x = 0; $x -lt $Source.Width; $x++) {
                $pixel = $Source.GetPixel($x, $y)
                if ($pixel.A -eq 0) {
                    $target.SetPixel($x, $y, [System.Drawing.Color]::Transparent)
                    continue
                }

                $luma = [Math]::Min(255, [int](0.30 * $pixel.R + 0.59 * $pixel.G + 0.11 * $pixel.B))
                $r = [Math]::Min(255, 8 + [int]($luma * 0.42))
                $g = [Math]::Min(255, 2 + [int]($luma * 0.08))
                $b = [Math]::Min(255, 5 + [int]($luma * 0.12))

                # Thin deterministic signal traces and very rare data sparks.
                # Transparency and the native UV layout remain untouched.
                if ((($x + 3 * $y + $Seed) % 17) -eq 0 -or (($x * 5 + $y + $Seed) % 41) -eq 0) {
                    $r = [Math]::Max($r, 176)
                    $g = [Math]::Max($g, 10)
                    $b = [Math]::Max($b, 28)
                }
                if ((($x * 11 + $y * 7 + $Seed) % 137) -eq 0) {
                    $r = [Math]::Max($r, 8)
                    $g = [Math]::Max($g, 165)
                    $b = [Math]::Max($b, 205)
                } elseif ((($x * 13 + $y * 17 + $Seed) % 181) -eq 0) {
                    $r = [Math]::Max($r, 190)
                    $g = [Math]::Max($g, 8)
                    $b = [Math]::Max($b, 155)
                }

                $target.SetPixel($x, $y, [System.Drawing.Color]::FromArgb($pixel.A, $r, $g, $b))
            }
        }
        $target.Save($Destination, [System.Drawing.Imaging.ImageFormat]::Png)
        Write-Output "Generated $Destination"
    } finally {
        $target.Dispose()
    }
}

$skins = @(
    @{ Source = 'assets/minecraft/textures/entity/rabbit/brown.png'; Output = 'rabbit.png'; Seed = 3 },
    @{ Source = 'assets/minecraft/textures/entity/cow/cow.png'; Output = 'cow.png'; Seed = 11 },
    @{ Source = 'assets/minecraft/textures/entity/wolf/wolf.png'; Output = 'wolf.png'; Seed = 19 },
    @{ Source = 'assets/minecraft/textures/entity/wolf/wolf_tame.png'; Output = 'wolf_tame.png'; Seed = 23 },
    @{ Source = 'assets/minecraft/textures/entity/wolf/wolf_angry.png'; Output = 'wolf_angry.png'; Seed = 29 },
    @{ Source = 'assets/minecraft/textures/entity/fox/fox.png'; Output = 'fox.png'; Seed = 31 },
    @{ Source = 'assets/minecraft/textures/entity/fox/fox_sleep.png'; Output = 'fox_sleep.png'; Seed = 37 },
    @{ Source = 'assets/minecraft/textures/entity/slime/slime.png'; Output = 'slime.png'; Seed = 43 }
)

$archive = [System.IO.Compression.ZipFile]::OpenRead($minecraftJar)
try {
    foreach ($skin in $skins) {
        $entry = $archive.GetEntry($skin.Source)
        if (-not $entry) { throw "Missing vanilla UV texture: $($skin.Source)" }
        $stream = $entry.Open()
        try {
            $loaded = [System.Drawing.Bitmap]::new($stream)
            try { $source = [System.Drawing.Bitmap]::new($loaded) } finally { $loaded.Dispose() }
        } finally {
            $stream.Dispose()
        }
        try {
            Convert-DarknetTexture -Source $source -Seed $skin.Seed -Destination (Join-Path $entityOutput $skin.Output)
        } finally {
            $source.Dispose()
        }
    }
} finally {
    $archive.Dispose()
}

$black = [System.Drawing.Color]::FromArgb(255, 8, 6, 9)
$oxblood = [System.Drawing.Color]::FromArgb(255, 72, 8, 22)
$red = [System.Drawing.Color]::FromArgb(255, 229, 24, 48)
$cyan = [System.Drawing.Color]::FromArgb(255, 21, 210, 224)
$magenta = [System.Drawing.Color]::FromArgb(255, 205, 18, 166)

function Set-PixelSafe([System.Drawing.Bitmap]$Bitmap, [int]$X, [int]$Y, [System.Drawing.Color]$Color) {
    if ($X -ge 0 -and $X -lt 16 -and $Y -ge 0 -and $Y -lt 16) { $Bitmap.SetPixel($X, $Y, $Color) }
}

function New-FoliageTexture([string]$Name, [scriptblock]$Painter) {
    $bitmap = [System.Drawing.Bitmap]::new(16, 16, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
    try {
        for ($y = 0; $y -lt 16; $y++) { for ($x = 0; $x -lt 16; $x++) { $bitmap.SetPixel($x, $y, [System.Drawing.Color]::Transparent) } }
        & $Painter $bitmap
        $path = Join-Path $foliageOutput ($Name + '.png')
        $bitmap.Save($path, [System.Drawing.Imaging.ImageFormat]::Png)
        Write-Output "Generated $path"
    } finally { $bitmap.Dispose() }
}

New-FoliageTexture 'darknet_signal_grass' {
    param($b)
    foreach ($stem in @(@(3,15,4), @(6,15,8), @(9,15,6), @(12,15,10))) {
        $x=$stem[0]; $bottom=$stem[1]; $top=$stem[2]
        for ($y=$bottom; $y -ge $top; $y--) { Set-PixelSafe $b $x $y $oxblood; if (($y+$x)%3 -eq 0) { Set-PixelSafe $b ($x+1) $y $red } }
    }
    Set-PixelSafe $b 7 10 $cyan; Set-PixelSafe $b 12 12 $magenta
}

New-FoliageTexture 'darknet_packet_fern' {
    param($b)
    for ($y=3; $y -le 15; $y++) { Set-PixelSafe $b 8 $y ($(if($y%3 -eq 0){$red}else{$oxblood})) }
    foreach ($y in @(5,7,9,11,13)) {
        $reach = [Math]::Min(6, [int](($y+1)/2))
        for ($d=1; $d -le $reach; $d++) {
            Set-PixelSafe $b (8-$d) ($y+[int]($d/3)) $black
            Set-PixelSafe $b (8+$d) ($y+[int]($d/3)) $black
            if ($d%2 -eq 0) { Set-PixelSafe $b (8-$d) ($y+[int]($d/3)) $oxblood; Set-PixelSafe $b (8+$d) ($y+[int]($d/3)) $oxblood }
        }
    }
    Set-PixelSafe $b 4 10 $cyan; Set-PixelSafe $b 11 8 $magenta
}

New-FoliageTexture 'darknet_cipher_bloom' {
    param($b)
    for ($y=7; $y -le 15; $y++) { Set-PixelSafe $b 8 $y $oxblood }
    foreach ($p in @(@(8,3),@(6,4),@(10,4),@(5,6),@(11,6),@(6,8),@(10,8),@(8,9))) { Set-PixelSafe $b $p[0] $p[1] $red }
    foreach ($p in @(@(7,5),@(8,5),@(9,5),@(7,6),@(8,6),@(9,6),@(8,7))) { Set-PixelSafe $b $p[0] $p[1] $cyan }
    Set-PixelSafe $b 5 5 $magenta; Set-PixelSafe $b 11 7 $magenta
}

New-FoliageTexture 'darknet_blackroot_shrub' {
    param($b)
    foreach ($p in @(@(3,13),@(4,11),@(5,9),@(6,12),@(7,7),@(8,10),@(9,5),@(10,9),@(11,7),@(12,12),@(13,10))) {
        Set-PixelSafe $b $p[0] $p[1] $black
        Set-PixelSafe $b $p[0] ($p[1]+1) $oxblood
        Set-PixelSafe $b ($p[0]-1) ($p[1]+1) $black
        Set-PixelSafe $b ($p[0]+1) ($p[1]+1) $black
    }
    for ($x=3; $x -le 13; $x++) { Set-PixelSafe $b $x 14 ($(if($x%3 -eq 0){$red}else{$oxblood})) }
    Set-PixelSafe $b 9 6 $magenta; Set-PixelSafe $b 4 12 $cyan
}
