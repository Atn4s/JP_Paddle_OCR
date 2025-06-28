from pathlib import Path

# Caminho base: o diretório onde está o arquivo path.py
BASE_DIR = Path(__file__).resolve().parent.parent  # Sobe até a raiz do projeto (ajuste conforme necessário)

# Caminho onde os resultados obtidos serão salvos (relativo ao diretório do projeto)
resultados = BASE_DIR / "Resultados_OCR"

# Caminho para as imagens a serem carregadas pelo EasyGUI, caso não seja especificado como argumento 
carregar_imagens = BASE_DIR / "images"

# Converter para string para garantir a compatibilidade com outros módulos do projeto
resultados = str(resultados)
carregar_imagens = str(carregar_imagens)