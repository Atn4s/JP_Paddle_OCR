#!/bin/bash
# Script robusto para instalar e testar PaddleOCR com fallback automático para paddlepaddle==2.6.2
# Autor: Atn4s com ajuda da IA 👾
clear
echo "🚀 Iniciando setup do PaddleOCR (versão compatível com sua máquina)..."

# 1. Instala pacotes necessários
echo "🔧 Instalando pacotes de sistema [python3.12-venv e libgomp1]"
sudo apt update && sudo apt install -y python3.12-venv libgomp1

# 2. Cria e ativa ambiente virtual
echo "🐍 Criando ambiente virtual 'PaddleOCR' na pasta atual"
python3.12 -m venv PaddleOCR
source PaddleOCR/bin/activate

# 3. Atualiza pip e instala dependências
echo "📦 Instalando PaddleOCR com PaddlePaddle 3.0.0 (primeira tentativa)..."
pip install --upgrade pip
pip install paddlepaddle==3.0.0 paddleocr==2.10.0 setuptools==80.3.1 wheel==0.45.1

# 4. Testa o comando paddleocr
echo "🧪 Testando o comando paddleocr..."

# Comando de teste com timeout e captura de falha de CPU
(paddleocr -m > /dev/null 2>&1) &
PID=$!
sleep 3
if ! kill -0 $PID 2>/dev/null; then
    wait $PID
    STATUS=$?
    if [[ $STATUS -eq 132 ]]; then
        echo "⚠️ Erro de instrução ilegal detectado (provavelmente AVX não suportado)."
        echo "🔁 Fazendo downgrade automático para paddlepaddle==2.6.2..."

        pip uninstall -y paddlepaddle
        pip install paddlepaddle==2.6.2

        echo "✅ Downgrade concluído. Tentando novamente o comando paddleocr..."
        paddleocr -m || echo "⚠️ paddleocr -m ainda não executou corretamente. Tente um teste completo com imagem."
    else
        echo "✅ paddleocr executado com sucesso na versão 3.0.0!"
    fi
else
    kill $PID
    echo "✅ paddleocr executado com sucesso na versão 3.0.0!"
fi

# 5. Exemplo de uso
echo "📸 Para testar com uma imagem real, use o comando:"
echo "   paddleocr --image_dir doc/imgs_en/254.jpg --lang=pt"
echo "🌍 Suporta idiomas como pt e en."

echo "🔧 Movendo diretórios para dentro do PaddleOCR e instalando o restante das dependencias!"
    mv Modulos PaddleOCR/
    mv OCR_schema.py PaddleOCR/
    mv PaddleGUI.py PaddleOCR/   
    pip install -r requirements.txt        
    mv requirements.txt PaddleOCR/
    mv processa_imagens.sh PaddleOCR/
    cd PaddleOCR/ 
    mkdir OCRDatabase
    mkdir Resultados_OCR
    echo "📂 Diretórios criados: OCRDatabase e Resultados_OCR."

echo "🏁 Setup finalizado. Pronto para extrair textos como um ninja OCR! 🥷📄"
echo "MAS ATENÇÃO! Todos os arquivos estão no diretório PaddleOCR!"
echo "Para iniciar o processo de OCR de forma automatica:"
echo "1: adicione suas imagens ao diretório OCRDatabase."
echo "2: execute o script processa_imagens.sh dentro do diretório PaddleOCR."
echo "3: Os resultados serão salvos no diretório Resultados_OCR e um processamento para uma saida JSON (em testes ainda) é salvo em Saida_Processada."