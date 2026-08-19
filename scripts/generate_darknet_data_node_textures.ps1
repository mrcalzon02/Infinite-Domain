$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$atlas = Join-Path $root 'docs\art-direction\darknet-data-node-production-atlas.png'
$reference = Join-Path $root 'docs\art-direction\darknet-content-reference.png'
$blockOutput = Join-Path $root 'kubejs\assets\kubejs\textures\block'
$itemOutput = Join-Path $root 'kubejs\assets\kubejs\textures\item'

if (-not (Test-Path -LiteralPath $atlas)) {
    throw "Missing Darknet production atlas: $atlas"
}
if (-not (Test-Path -LiteralPath $reference)) {
    throw "Missing Darknet content reference: $reference"
}

New-Item -ItemType Directory -Path $blockOutput, $itemOutput -Force | Out-Null
Add-Type -AssemblyName System.Drawing

$source = [System.Drawing.Bitmap]::new($atlas)
try {
    $tiles = @(
        @{ Name = 'fragmented_data_node'; X = 59; Y = 185; Size = 368 },
        @{ Name = 'corrupted_data_node'; X = 475; Y = 185; Size = 368 },
        @{ Name = 'encrypted_data_node'; X = 896; Y = 185; Size = 368 },
        @{ Name = 'root_access_node'; X = 1316; Y = 185; Size = 368 },
        @{ Name = 'darknet_bedrock'; X = 1738; Y = 185; Size = 368 }
    )

    foreach ($tile in $tiles) {
        $target = [System.Drawing.Bitmap]::new(32, 32, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
        try {
            $graphics = [System.Drawing.Graphics]::FromImage($target)
            try {
                $graphics.CompositingMode = [System.Drawing.Drawing2D.CompositingMode]::SourceCopy
                $graphics.CompositingQuality = [System.Drawing.Drawing2D.CompositingQuality]::HighSpeed
                $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::NearestNeighbor
                $graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::Half
                $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::None
                $destination = [System.Drawing.Rectangle]::new(0, 0, 32, 32)
                $crop = [System.Drawing.Rectangle]::new($tile.X, $tile.Y, $tile.Size, $tile.Size)
                $graphics.DrawImage($source, $destination, $crop, [System.Drawing.GraphicsUnit]::Pixel)
            } finally {
                $graphics.Dispose()
            }

            $path = Join-Path $blockOutput ($tile.Name + '.png')
            $target.Save($path, [System.Drawing.Imaging.ImageFormat]::Png)
            Write-Output "Generated $path"
        } finally {
            $target.Dispose()
        }
    }
} finally {
    $source.Dispose()
}

$itemSource = [System.Drawing.Bitmap]::new($reference)
try {
    # Remove the sheet's chroma-key field before scaling so the icons retain
    # true transparent edges in inventories, quests, and Echoes stores.
    for ($y = 0; $y -lt $itemSource.Height; $y++) {
        for ($x = 0; $x -lt $itemSource.Width; $x++) {
            $pixel = $itemSource.GetPixel($x, $y)
            if ($pixel.G -gt 120 -and $pixel.G -gt ($pixel.R * 1.45) -and $pixel.G -gt ($pixel.B * 1.45)) {
                $itemSource.SetPixel($x, $y, [System.Drawing.Color]::Transparent)
            }
        }
    }

    $icons = @(
        @{ Name = 'darknet_data_cache'; X = 10; Y = 510; Size = 240 },
        @{ Name = 'scraped_access_token'; X = 210; Y = 510; Size = 240 },
        @{ Name = 'encrypted_credential_bundle'; X = 415; Y = 510; Size = 240 },
        @{ Name = 'black_ice_kernel'; X = 615; Y = 510; Size = 240 },
        @{ Name = 'zero_day_archive'; X = 820; Y = 510; Size = 240 },
        @{ Name = 'root_authority_key'; X = 1005; Y = 500; Size = 240 }
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
                $graphics.DrawImage($itemSource, $destination, $crop, [System.Drawing.GraphicsUnit]::Pixel)
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
    $itemSource.Dispose()
}
