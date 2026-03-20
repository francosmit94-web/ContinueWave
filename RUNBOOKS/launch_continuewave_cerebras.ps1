$envFile = "C:\Users\Franco\Desktop\ContinueWave\.env"
if (Test-Path $envFile) {
  Get-Content $envFile | ForEach-Object {
    if ($_ -match '^\s*#' -or $_ -match '^\s*$') { return }
    $parts = $_ -split '=', 2
    if ($parts.Length -eq 2) {
      [System.Environment]::SetEnvironmentVariable($parts[0], $parts[1], 'Process')
    }
  }
}

$env:OPENAI_API_KEY = $env:CEREBRAS_API_KEY
$env:OPENAI_API_BASE = "https://api.cerebras.ai/v1"
$env:PATH = "C:\Users\Franco\AppData\Roaming\npm;$env:PATH"

Set-Location "C:\Users\Franco\Desktop\ContinueWave"

& "C:\Users\Franco\AppData\Roaming\npm\cn.cmd" `
  --config "C:\Users\Franco\.continue\config.yaml" `
  --rule ".\.continue\rules\brain.md"
