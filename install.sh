# Garantir que o python3.12-venv e libgomp1 estejam instalados.
sudo apt install python3.12-venv libgomp1

# inicia ambiente python
python3 -m venv PaddleOCR

# ativa o ambiente
source PaddleOCR/bin/activate

#criação de diretórios necessários:
cd PaddleOCR/
mkdir Matriz_Confusao
mkdir Resultados_OCR
touch path.py

# Em path.py insirá os caminhos que seram utilizados durante o projeto como no exemplo abaixo:
# === Caminho resultados obtidos ===
#resultados = "/home/Usuario/Documentos/Resultados_OCR"
# === Caminho para iniciar o Paddle ===
#carregar_imagens = "/home/Usuario/IMAGENS_OCR"
# === Caminho para resultados oe JSON ===
#matriz_confusao = "/home/Usuario/Documentos/Matriz_Confusao/"

# Antes de instalar verifique o modelo que deseja, se é baseado na CPU ou GPU
#cpu
pip install paddlepaddle
# gpu
pip install paddlepaddle-gpu

# pip dependencias:
pip install paddleocr setuptools wheel

# garantir que ambiente está configurado e atualizado
pip install -U pip paddleocr setuptools wheel

# Uso Paddle:
# paddleocr --image_dir doc/imgs_en/254.jpg --lang=pt # suporta en também no idioma