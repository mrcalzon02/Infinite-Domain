param(
    [string]$SourceDirectory = "ROOT_tools\darknet_anchor_source\assets\ae2\textures\block",
    [string]$OutputDirectory = "kubejs\assets\ae2\textures\block"
)

Add-Type -AssemblyName System.Drawing
New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null

$palette = @{
    "33,32,64"   = @(40, 12, 16)
    "38,43,84"   = @(52, 15, 20)
    "51,45,88"   = @(58, 16, 22)
    "55,59,114"  = @(70, 18, 24)
    "65,63,84"   = @(58, 40, 42)
    "77,50,109"  = @(76, 17, 23)
    "77,77,103"  = @(68, 45, 48)
    "94,59,118"  = @(92, 20, 28)
    "96,84,166"  = @(104, 22, 30)
    "136,68,114" = @(128, 24, 34)
    "145,93,205" = @(142, 28, 39)
    "176,111,221" = @(178, 38, 52)
    "255,128,215" = @(235, 48, 68)
}

Get-ChildItem -LiteralPath $SourceDirectory -Filter "spatial_anchor*.png" | ForEach-Object {
    $source = [System.Drawing.Bitmap]::new($_.FullName)
    $output = [System.Drawing.Bitmap]::new($source.Width, $source.Height, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
    for ($y = 0; $y -lt $source.Height; $y++) {
        for ($x = 0; $x -lt $source.Width; $x++) {
            $color = $source.GetPixel($x, $y)
            $key = "$($color.R),$($color.G),$($color.B)"
            if ($palette.ContainsKey($key)) {
                $replacement = $palette[$key]
                $color = [System.Drawing.Color]::FromArgb($color.A, $replacement[0], $replacement[1], $replacement[2])
            }
            $output.SetPixel($x, $y, $color)
        }
    }
    $destination = Join-Path $OutputDirectory $_.Name
    $output.Save($destination, [System.Drawing.Imaging.ImageFormat]::Png)
    $output.Dispose()
    $source.Dispose()
}
