#!/bin/bash
source bin/activate

# Diretório onde estão as imagens
DIRETORIO_IMAGENS="./images"

# Loop através de todos os arquivos de imagem no diretório
for imagem in "$DIRETORIO_IMAGENS"/*.{jpg,jpeg,webp,png,gif}; do
    # Verifica se o arquivo existe
    if [ -f "$imagem" ]; then
        echo "Processando $imagem..."
        # Chama o script Python com a imagem como argumento
        python3.12 PaddleGUI.py "$imagem"        
    else
        echo "Nenhuma imagem encontrada no diretório ou processamento acabou."
        echo "Verifique se o diretório $DIRETORIO_IMAGENS contém imagens"
        echo "Saindo do script."
    fi
done