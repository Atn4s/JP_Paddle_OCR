import os, cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

# Importação dos módulos path, config e OCR_schema para processamento do JSON
import Modulos.path as path
import Modulos.config as config
from OCR_schema import OCRProcessor

# Função para processar a imagem e aplicar OCR
def process_image(img_path):    
    img_name = os.path.basename(img_path)         # Nome base do arquivo a ser feito o processamento de imagem
    name_no_ext = os.path.splitext(img_name)[0]   # Remove a extensão do nome do arquivo para uso posterior 

    # === Lê a imagem com OpenCV e converte para PIL ===
    img_cv = cv2.imread(img_path)
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    draw = ImageDraw.Draw(img_pil)

    # === OCR utilizando as configurações do modulo config ===
    result = config.ocr.ocr(img_path, cls=True)[0]

    # === Processa OCR e desenha ===
    texto_bruto = ""

    # Itera sobre os resultados do OCR
    for box, (text, score) in result:
        pts = np.array(box).astype(int)

        # Define os pontos extremos da caixa delimitadora 
        x0 = min(pts[0][0], pts[2][0])
        y0 = min(pts[0][1], pts[2][1])
        x1 = max(pts[0][0], pts[2][0])
        y1 = max(pts[0][1], pts[2][1])

        top_left = (x0, y0)                     # Topo superior esquerdo da caixa delimitadora
        bottom_right = (x1, y1)                 # Canto inferior direito da caixa delimitadora
        if config.mode == "json":               # Verifica o modo de validação se é manual ou OCR
            color = config.get_color()          # Se for JSON, a cor será do iterador do JSON 
        elif config.mode == "ocr_mode":         # Se for OCR, a cor será baseada no score do PaddleOCR
            color = config.get_color(score)

        draw.rectangle([top_left, bottom_right], outline=color, width=3) # Desenha a caixa delimitadora do texto para evitar sobreposiçaõ

        box_height = bottom_right[1] - top_left[1]  # Define dinamicamente o tamanho da fonte com base na altura da caixa
        font_size = max(10, int(box_height * 0.5))  # 50% da altura da caixa para garantir que o texto caiba na plotagem 
        font = config.get_font(size=font_size)      # Definição do tamanho da fonte baseado na altura da caixa 

        bbox = font.getbbox(text)                   # Obtém a caixa delimitadora do texto para calcular o tamanho do texto
        text_width = bbox[2] - bbox[0]              # Definição da largura do texto  
        text_height = bbox[3] - bbox[1]             # Definição da altuira do texto 

        text_x = top_left[0]                        # Posição X do texto, alinhado à esquerda da caixa delimitadora
        text_y = top_left[1] - text_height - 2      # Posição Y do texto, acima da caixa delimitadora 
        
        if text_y < 0:                              # Se o texto subir demais (sair da imagem), joga pra baixo da caixa
            text_y = bottom_right[1] + 2            # Desenha logo abaixo da caixa
        
        if text_x + text_width > img_pil.width:     # Se ultrapassar a borda direita, ajusta para caber 
            text_x = img_pil.width - text_width - 2 
        
        if text_x < 0:                              # Se ultrapassar a borda esquerda, ajusta para cab er
            text_x = 2

        # Contorno preto no texto para garantir melhor legibilidade
        for dx in [-1, 1]:                                                                      
            for dy in [-1, 1]:
                draw.text((text_x + dx, text_y + dy), text, font=font, fill=(0, 0, 0))

        # Texto principal branco 
        draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255))

        # A saída do OCR é formatada para incluir o texto identificado, o score baseado na confiança do Paddle e as coordenadas do bounding box
        texto_bruto += f"OCR='{text}', score={score:.2f}, bbox=[{x0},{y0},{x1},{y1}]\n"

    # === Legenda na imagem ===
    legenda_textos = [
        ("Verde: Texto CORRETO (match com esperado)", (0, 255, 0)),
        ("Vermelho: Texto ERRADO (não bate com esperado)", (255, 0, 0))
    ]

    # Posição base da legenda na imagem
    lx, ly = 20, img_pil.height - 100

    # Dssenha a legenda na imagem 
    for i, (legenda, cor) in enumerate(legenda_textos):
        draw.text((lx, ly + i * 30), legenda, fill=cor, font=font)

    # === Salva texto extraído ===
    txt_filename = os.path.join(path.resultados, f"{name_no_ext}_Paddle_ocr.txt")
    with open(txt_filename, "w", encoding="utf-8") as f:
        f.write(texto_bruto)

    # === Salva imagem plotada ===
    plot_filename = os.path.join(path.resultados, f"{name_no_ext}_Paddle_plotagem.jpg")
    img_pil.save(plot_filename)

    # === Exibe com Matplotlib ===
    img_final = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR) #Converte de RGB para BGR para compatibilidade com OpenCV
    plt.figure(figsize=(12, 16))                           # Tamanho maior para melhor visualização  
    plt.imshow(cv2.cvtColor(img_final, cv2.COLOR_BGR2RGB)) # Converte de BGR para RGB para garantir a exibição das cores do Matplotlib
    plt.axis("off")                                        # Desativa os eixos para uma visualização mais limpa
    plt.title(f"OCR: {img_name}")                          # Titulo da imagem com o nome do arquivo 
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)  # Preenche toda a figura
    #plt.show()                                            # Opção para exibir a imagem plotada após o processamento, desativado para ser mais rapido
    
    # === Processa imediatamente o .txt salvo ===
    processor = OCRProcessor()                            # Invoca a classe OCRProcessor do módulo OCR_schema para iniciar o processamento do arquivo .txt
    processor.output_dir = "Saida_Processada"             # Diretório de saída para os arquivos processados
    processor.ensure_output_dir()                         # Garante que o diretório de saída exista
    output_name = f"{name_no_ext}_Paddle_processado.json" # Nome do arquivo de saída processado
    processor.process_file(txt_filename, output_name)     # Processa o arquivo .txt e salva o resultado no formato JSON