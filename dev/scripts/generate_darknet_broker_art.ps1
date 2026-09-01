$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$itemReference = Join-Path $root 'docs\art-direction\darknet-broker-items-reference.png'
$itemOutput = Join-Path $root 'kubejs\assets\kubejs\textures\item'
$entityOutput = Join-Path $root 'packdev\darknet-worldgen-patch\src\main\resources\assets\infinite_domain\textures\entity'
$minecraftJar = 'C:\Users\Admin\curseforge\minecraft\Install\versions\1.21.1\1.21.1.jar'

foreach ($required in @($itemReference, $minecraftJar)) {
    if (-not (Test-Path -LiteralPath $required)) {
        throw "Missing Darknet Broker art dependency: $required"
    }
}

New-Item -ItemType Directory -Path $itemOutput, $entityOutput -Force | Out-Null
Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName System.IO.Compression.FileSystem

$reference = [System.Drawing.Bitmap]::new($itemReference)
try {
    $icons = @(
        @{ Name = 'darknet_scrip'; X = 45; Y = 38; Size = 650 },
        @{ Name = 'ghost_market_cipher'; X = 753; Y = 38; Size = 650 },
        @{ Name = 'black_ledger_writ'; X = 1490; Y = 38; Size = 650 }
    )

    foreach ($icon in $icons) {
        $target = [System.Drawing.Bitmap]::new(32, 32, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
        try {
            $graphics = [System.Drawing.Graphics]::FromImage($target)
            try {
                $graphics.Clear([System.Drawing.Color]::Transparent)
                $graphics.CompositingMode = [System.Drawing.Drawing2D.CompositingMode]::SourceCopy
                $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::NearestNeighbor
                $graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::Half
                $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::None
                $destination = [System.Drawing.Rectangle]::new(0, 0, 32, 32)
                $crop = [System.Drawing.Rectangle]::new($icon.X, $icon.Y, $icon.Size, $icon.Size)
                $graphics.DrawImage($reference, $destination, $crop, [System.Drawing.GraphicsUnit]::Pixel)
            } finally {
                $graphics.Dispose()
            }

            $path = Join-Path $itemOutput ($icon.Name + '.png')
            $target.Save($path, [System.Drawing.Imaging.ImageFormat]::Png)
            Write-Output "Generated $path"
        } finally {
            $target.Dispose()
        }
    }
} finally {
    $reference.Dispose()
}

$archive = [System.IO.Compression.ZipFile]::OpenRead($minecraftJar)
try {
    $entry = $archive.GetEntry('assets/minecraft/textures/entity/wandering_trader.png')
    if (-not $entry) {
        throw 'The installed Minecraft jar has no wandering trader texture'
    }
    $stream = $entry.Open()
    try {
        $nativeLoaded = [System.Drawing.Bitmap]::new($stream)
        try {
            $native = [System.Drawing.Bitmap]::new($nativeLoaded)
        } finally {
            $nativeLoaded.Dispose()
        }
    } finally {
        $stream.Dispose()
    }
} finally {
    $archive.Dispose()
}

try {
    $target = [System.Drawing.Bitmap]::new($native.Width, $native.Height, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
    try {
        for ($y = 0; $y -lt $native.Height; $y++) {
            for ($x = 0; $x -lt $native.Width; $x++) {
                $pixel = $native.GetPixel($x, $y)
                if ($pixel.A -eq 0) {
                    $target.SetPixel($x, $y, [System.Drawing.Color]::Transparent)
                    continue
                }

                $luma = [Math]::Min(255, [int](0.30 * $pixel.R + 0.59 * $pixel.G + 0.11 * $pixel.B))
                $isSkin = $pixel.R -gt 60 -and $pixel.R -gt ($pixel.G * 1.20) -and $pixel.G -gt ($pixel.B * 1.20) -and $pixel.G -lt 125
                $isGold = $pixel.R -gt 125 -and $pixel.G -gt 75 -and $pixel.B -lt 70 -and -not $isSkin
                $isBlue = $pixel.B -gt ($pixel.R * 1.08) -or $pixel.B -gt ($pixel.G * 1.12)

                if ($isSkin) {
                    $r = [Math]::Min(255, [int]($pixel.R * 0.76))
                    $g = [Math]::Min(255, [int]($pixel.G * 0.66))
                    $b = [Math]::Min(255, [int]($pixel.B * 0.62))
                } elseif ($isGold) {
                    $r = [Math]::Min(255, 78 + [int]($luma * 0.62))
                    $g = [Math]::Min(255, 4 + [int]($luma * 0.07))
                    $b = [Math]::Min(255, 24 + [int]($luma * 0.24))
                } elseif ($isBlue) {
                    $r = [Math]::Min(255, 8 + [int]($luma * 0.45))
                    $g = [Math]::Min(255, 2 + [int]($luma * 0.10))
                    $b = [Math]::Min(255, 7 + [int]($luma * 0.18))
                } else {
                    $r = [Math]::Min(255, 6 + [int]($luma * 0.42))
                    $g = [Math]::Min(255, 2 + [int]($luma * 0.11))
                    $b = [Math]::Min(255, 5 + [int]($luma * 0.16))
                }

                if (-not $isSkin -and (($x + 2 * $y) % 19) -eq 0) {
                    $r = [Math]::Max($r, 132)
                    $g = [Math]::Max($g, 8)
                    $b = [Math]::Max($b, 28)
                } elseif (-not $isSkin -and (($x * 7 + $y * 11) % 101) -eq 0) {
                    $r = [Math]::Max($r, 8)
                    $g = [Math]::Max($g, 118)
                    $b = [Math]::Max($b, 170)
                }

                $target.SetPixel($x, $y, [System.Drawing.Color]::FromArgb($pixel.A, $r, $g, $b))
            }
        }

        # The villager face UV uses these two pixels as its eyes. A restrained
        # magenta visor mark makes the Broker recognizable even without overlays.
        foreach ($eye in @(@(9, 10), @(14, 10))) {
            $existing = $target.GetPixel($eye[0], $eye[1])
            if ($existing.A -gt 0) {
                $target.SetPixel($eye[0], $eye[1], [System.Drawing.Color]::FromArgb($existing.A, 245, 28, 180))
            }
        }

        $skinPath = Join-Path $entityOutput 'darknet_broker.png'
        $target.Save($skinPath, [System.Drawing.Imaging.ImageFormat]::Png)
        Write-Output "Generated $skinPath"
    } finally {
        $target.Dispose()
    }
} finally {
    $native.Dispose()
}
