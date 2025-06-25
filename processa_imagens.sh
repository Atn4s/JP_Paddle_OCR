#!/bin/bash
source bin/activate

# Diretório onde estão as imagens
DIRETORIO_IMAGENS="./OCRDatabase"

# Loop através de todos os arquivos de imagem no diretório
for imagem in "$DIRETORIO_IMAGENS"/*.{jpg,jpeg,webp,png,gif}; do
    # Verifica se o arquivo existe
    if [ -f "$imagem" ]; then
        echo "Processando $imagem..."
        # Chama o script Python com a imagem como argumento
        python3 PaddleGUI.py "$imagem"
    else
        echo "Nenhuma imagem encontrada no diretório."
    fi
done

echo "Vamos processar as imagens para sair em formato JSON."
# Chama o script Python para processar as imagens
python3 OCR_schema.py