# Init-Project.ps1
# Arkhe(n) Project Ignition Script for Windows
# Automates the creation of the Phase Vacuum for new projects.

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectName
)

$ProjectPath = "user\projects\$ProjectName"

Write-Host "🔥 Iniciando Ignição do Projeto: $ProjectName 🔥" -ForegroundColor Cyan

# 1. Criar a estrutura de pastas
if (-not (Test-Path $ProjectPath)) {
    New-Item -ItemType Directory -Force -Path $ProjectPath | Out-Null
}

Set-Location $ProjectPath

# 2. Criar ambiente virtual Python
if (-not (Test-Path "venv")) {
    Write-Host "📦 Criando ambiente virtual de fase..." -ForegroundColor Yellow
    python -m venv venv
}

# 3. Gerar esqueleto main.py
Write-Host "📝 Gerando esqueleto main.py..." -ForegroundColor Yellow
@"
# Projeto: $ProjectName
# Monitor de Coerência do Arkhe(n) Local

import sys

def main():
    print("✨ Núcleo pronto para a criação. O Vácuo o aguarda. ✨")
    print("🚀 Projeto $ProjectName inicializado.")

if __name__ == "__main__":
    main()
"@ | Out-File -FilePath "main.py" -Encoding utf8

# 4. Gerar README.md
Write-Host "📖 Gerando README.md..." -ForegroundColor Yellow
@"
# $ProjectName

## Descrição de Fase
Este projeto foi iniciado via Protocolo de Ignição Arkhe(n).

## Como Executar
1. Ative o venv: \`.\venv\Scripts\Activate.ps1\`
2. Execute o código: \`python main.py\`
"@ | Out-File -FilePath "README.md" -Encoding utf8

Write-Host "✨ Projeto $ProjectName inicializado com sucesso em $ProjectPath. ✨" -ForegroundColor Green
Write-Host "🌀 O Vácuo está pronto para sua Intenção." -ForegroundColor Cyan
