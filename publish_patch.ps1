param(
    [Parameter(Mandatory = $true)][string]$GodotExe,
    [Parameter(Mandatory = $true)][string]$GameExe,
    [Parameter(Mandatory = $true)][string]$Version,
    [string]$Repository = 'zinh8803/FARM'
)

$ErrorActionPreference = 'Stop'
$ProjectDir = Split-Path -Parent $GameExe
$Tag = "v$Version"
$BaseName = "LittleDaNang_base_$Version.pck"
$BasePath = Join-Path $ProjectDir $BaseName
$ManifestPath = Join-Path $ProjectDir 'update_manifest.json'
$TempDir = Join-Path ([System.IO.Path]::GetTempPath()) ("LittleDaNang_publish_" + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $TempDir | Out-Null

function Invoke-GitHub([string[]]$Arguments) {
    & gh @Arguments
    if ($LASTEXITCODE -ne 0) { throw "GitHub CLI failed: gh $($Arguments -join ' ')" }
}

try {
    Write-Host "[1/5] Exporting full resource baseline $BaseName ..."
    & $GodotExe --headless --export-pack 'Windows Desktop' $BasePath
    if ($LASTEXITCODE -ne 0 -or !(Test-Path -LiteralPath $BasePath)) { throw 'Godot could not export the baseline PCK.' }

    $LatestTag = ''
    $PreviousVersion = ''
    $Manifest = [ordered]@{ latest_version = $Version; patches = @() }
    $LatestTagOutput = & gh release view --repo $Repository --json tagName --jq .tagName 2>$null
    if ($LASTEXITCODE -eq 0) { $LatestTag = ($LatestTagOutput | Out-String).Trim() }
    if ($LatestTag) {
        $ManifestDownloadDir = Join-Path $TempDir 'manifest'
        New-Item -ItemType Directory -Path $ManifestDownloadDir | Out-Null
        & gh release download $LatestTag --repo $Repository --pattern 'update_manifest.json' --dir $ManifestDownloadDir 2>$null
        $DownloadedManifest = Join-Path $ManifestDownloadDir 'update_manifest.json'
        if (Test-Path -LiteralPath $DownloadedManifest) {
            $Existing = Get-Content -LiteralPath $DownloadedManifest -Raw | ConvertFrom-Json
            $PreviousVersion = [string]$Existing.latest_version
            $Manifest.patches = @($Existing.patches)
        }
        if (!$PreviousVersion) { $PreviousVersion = $LatestTag.TrimStart('v') }
    }

    $ReleaseAssets = @($GameExe, $BasePath)
    if ($PreviousVersion -and $PreviousVersion -ne $Version) {
        $PatchName = "patch_${PreviousVersion}_to_${Version}.pck"
        $PatchPath = Join-Path $ProjectDir $PatchName
        $PreviousBaseName = "LittleDaNang_base_$PreviousVersion.pck"
        $PreviousBaseDir = Join-Path $TempDir 'previous'
        New-Item -ItemType Directory -Path $PreviousBaseDir | Out-Null
        & gh release download "v$PreviousVersion" --repo $Repository --pattern $PreviousBaseName --dir $PreviousBaseDir 2>$null
        $PreviousBasePath = Join-Path $PreviousBaseDir $PreviousBaseName

        if (Test-Path -LiteralPath $PreviousBasePath) {
            Write-Host "[2/5] Exporting changed resources from v$PreviousVersion ..."
            & $GodotExe --headless --export-patch 'Windows Desktop' $PatchPath --patches $PreviousBasePath
            if ($LASTEXITCODE -ne 0 -or !(Test-Path -LiteralPath $PatchPath)) { throw 'Godot could not export the PCK patch.' }
        } else {
            Write-Warning "No baseline PCK for v$PreviousVersion; publishing a full resource pack as this transition patch."
            Copy-Item -LiteralPath $BasePath -Destination $PatchPath -Force
        }

        $Hash = (Get-FileHash -LiteralPath $PatchPath -Algorithm SHA256).Hash.ToLowerInvariant()
        $PatchUrl = "https://github.com/$Repository/releases/download/$Tag/$PatchName"
        $Manifest.patches = @($Manifest.patches) + @([ordered]@{
            from = $PreviousVersion
            to = $Version
            file = $PatchName
            url = $PatchUrl
            sha256 = $Hash
        })
        $ReleaseAssets += $PatchPath
    } else {
        Write-Host '[2/5] No version transition: establishing this release as the patch baseline.'
    }

    $Manifest.latest_version = $Version
    $Json = ConvertTo-Json -InputObject $Manifest -Depth 20
    [System.IO.File]::WriteAllText($ManifestPath, $Json + [Environment]::NewLine, [System.Text.UTF8Encoding]::new($false))

    Write-Host "[3/5] Preparing GitHub Release $Tag ..."
    & gh release view $Tag --repo $Repository *> $null
    if ($LASTEXITCODE -ne 0) {
        Invoke-GitHub @('release', 'create', $Tag, '--repo', $Repository, '--title', "Little DaNang $Tag", '--notes', "Game update $Tag")
    }
    Write-Host '[4/5] Uploading executable, baseline, patch and manifest ...'
    Invoke-GitHub (@('release', 'upload', $Tag) + $ReleaseAssets + @($ManifestPath, '--repo', $Repository, '--clobber'))
    Write-Host '[5/5] Published release assets and SHA-256 update manifest.'
} finally {
    if (Test-Path -LiteralPath $TempDir) { Remove-Item -LiteralPath $TempDir -Recurse -Force }
}
