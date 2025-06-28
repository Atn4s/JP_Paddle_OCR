import easygui, sys

# === Importa módulos personalizados ===
import Modulos.path as path 
import Modulos.image_processing as image_processing

# === PaddleGUI é o script principal para processamento de imagens utilizando o PaddleOCR + plotagem do Matplotlib e correção de saída para JSON 
# O ciclo envolve selecionar uma imagem por argumento ou através do EasyGUI no qual é feito o processamento na imagem 
# e salva os resultados em .txt, a imagem plotada e o JSON com os resultados do OCR, dentro de Resultados_OCR e Saida_Processada ===  

# === Caminho resultado e carregamento de imagens obtidos ===
result_path = path.resultados           # Caminho onde os resultados serão salvos definidos no path.py
load_path =  path.carregar_imagens      # Caminho onde os arquivos de entrada para carregar pelo EasyGUI serão carregados definidos no path.py

# === Seleciona imagem ou por argumento ou pelo processo do EasyGUI === 
try:
    img_path = sys.argv[1] if len(sys.argv) > 1 else easygui.fileopenbox(default=f"{load_path}/*")
except:
    print("Erro ao selecionar a imagem.")
    exit()

if not img_path:
    print("Nenhuma imagem selecionada.")
    exit()

image_processing.process_image(img_path) # Após a imagem ser selecionada, chama a função process_iomage do módulo image_processing para processar a imagem e aplicar OCR