from pathlib import Path

# Caminho base: o diretório onde está o arquivo path.py
BASE_DIR = Path(__file__).resolve().parent.parent  # Sobe até a raiz do projeto (ajuste conforme necessário)

# Caminho resultados obtidos (relativo ao diretório do projeto)
resultados = BASE_DIR / "Resultados_OCR"

# Caminho para as imagens a serem carregadas
carregar_imagens = BASE_DIR / "OCRDatabase"

# Opcional: converter para string, se o resto do código não usa pathlib
resultados = str(resultados)
carregar_imagens = str(carregar_imagens)