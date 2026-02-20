param(
  [Parameter(Mandatory = $true)]
  [string]$InFile
)

if (-not $env:DATABASE_URL) {
  throw "DATABASE_URL is required"
}

Get-Content -Path $InFile | psql $env:DATABASE_URL
Write-Output "Restore completed from: $InFile"
