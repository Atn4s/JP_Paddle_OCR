import easygui, sys

# === Importa módulos personalizados ===
import Modulos.path as path 
import Modulos.image_processing as image_processing

# === Caminho resultado e carregamento de imagens obtidos ===
result_path = path.resultados
load_path =  path.carregar_imagens

# === Seleciona imagem ===
try:
    img_path = sys.argv[1] if len(sys.argv) > 1 else easygui.fileopenbox(default=f"{load_path}/*")
except:
    print("Erro ao selecionar a imagem.")
    exit()

if not img_path:
    print("Nenhuma imagem selecionada.")
    exit()

image_processing.process_image(img_path)