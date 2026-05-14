# Install-ArkheExplorerMenu.ps1
$registryPath = "HKLM:\SOFTWARE\Classes\*\shell\ArkheVerify"
New-Item -Path $registryPath -Force | Out-Null
Set-ItemProperty -Path $registryPath -Name "MUIVerb" -Value "🔐 Verificar com Arkhe"
Set-ItemProperty -Path $registryPath -Name "Icon" -Value "$env:ProgramFiles\ArkheOS\arkhe.ico"

# Comando ao clicar
$commandPath = "$registryPath\command"
New-Item -Path $commandPath -Force | Out-Null
Set-ItemProperty -Path $commandPath -Name "(Default)" -Value '"$env:ProgramFiles\ArkheOS\arkh.exe" verify "%1"'

# Submenu adicional
$submenuPath = "HKLM:\SOFTWARE\Classes\*\shell\ArkheMenu"
New-Item -Path $submenuPath -Force | Out-Null
Set-ItemProperty -Path $submenuPath -Name "MUIVerb" -Value "Arkhe OS"
Set-ItemProperty -Path $submenuPath -Name "SubCommands" -Value "Arkhe.Verify;Arkhe.Seal;Arkhe.Anchor;Arkhe.GovernanceAudit"

Write-Host "✅ Menu de contexto do Explorer instalado" -ForegroundColor Green
