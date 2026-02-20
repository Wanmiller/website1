param(
  [Parameter(Mandatory = $false)]
  [string]$OutDir = "backups"
)

if (-not $env:DATABASE_URL) {
  throw "DATABASE_URL is required"
}

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$outFile = Join-Path $OutDir "cineverse_$stamp.sql"

pg_dump $env:DATABASE_URL | Set-Content -Path $outFile -Encoding utf8
Write-Output "Backup saved: $outFile"
