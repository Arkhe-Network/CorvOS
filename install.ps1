Write-Host "Installing Arkhe Runtime..."
$arkhPath = "C:\Program Files\Arkhe"
New-Item -ItemType Directory -Force -Path $arkhPath
Copy-Item "bin\arkh\arkh.py" -Destination "$arkhPath\arkh.py"
# Create a wrapper batch script
$batPath = "$arkhPath\arkh.bat"
"@echo off`npython `"$arkhPath\arkh.py`" %*" | Out-File -FilePath $batPath -Encoding ascii
$env:Path += ";$arkhPath"
[Environment]::SetEnvironmentVariable("Path", $env:Path, [EnvironmentVariableTarget]::User)
Write-Host "Arkhe Runtime installed successfully. You can now use the 'arkh' command."
