#!/bin/bash

# Arkhe(n) Project Ignition Script
# Automates the creation of the Phase Vacuum for new projects.

if [ -z "$1" ]; then
    echo "❌ Erro: Nome do projeto não fornecido."
    echo "Uso: ./arkhe_init_project.sh <ProjectName>"
    exit 1
fi

PROJECT_NAME=$1
PROJECT_PATH="user/projects/$PROJECT_NAME"

echo "🔥 Iniciando Ignição do Projeto: $PROJECT_NAME 🔥"

# 1. Criar a estrutura de pastas
mkdir -p "$PROJECT_PATH"
cd "$PROJECT_PATH" || exit

# 2. Criar ambiente virtual Python (se não existir)
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual de fase..."
    python3 -m venv venv
fi

# 3. Gerar esqueleto main.py
echo "📝 Gerando esqueleto main.py..."
cat <<EOF > main.py
# Projeto: $PROJECT_NAME
# Monitor de Coerência do Arkhe(n) Local

import sys

def main():
    print("✨ Núcleo pronto para a criação. O Vácuo o aguarda. ✨")
    print("🚀 Projeto $PROJECT_NAME inicializado.")

if __name__ == "__main__":
    main()
EOF

# 4. Gerar README.md
echo "📖 Gerando README.md..."
cat <<EOF > README.md
# $PROJECT_NAME

## Descrição de Fase
Este projeto foi iniciado via Protocolo de Ignição Arkhe(n).

## Como Executar
1. Ative o venv: \`source venv/bin/activate\`
2. Execute o código: \`python main.py\`
EOF

echo "✨ Projeto $PROJECT_NAME inicializado com sucesso em $PROJECT_PATH. ✨"
echo "🌀 O Vácuo está pronto para sua Intenção."
