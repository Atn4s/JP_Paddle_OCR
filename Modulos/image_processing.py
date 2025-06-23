import os, cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

import Modulos.path as path
import Modulos.config as config

def process_image(img_path):
    # === Nome base do arquivo ===
    img_name = os.path.basename(img_path)
    name_no_ext = os.path.splitext(img_name)[0]

    # === Lê a imagem com OpenCV e converte para PIL ===
    img_cv = cv2.imread(img_path)
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    draw = ImageDraw.Draw(img_pil)

    # === OCR ===
    result = config.ocr.ocr(img_path, cls=True)[0]

    # === Processa OCR e desenha ===
    texto_bruto = ""

    for box, (text, score) in result:
        pts = np.array(box).astype(int)

        x0 = min(pts[0][0], pts[2][0])
        y0 = min(pts[0][1], pts[2][1])
        x1 = max(pts[0][0], pts[2][0])
        y1 = max(pts[0][1], pts[2][1])

        top_left = (x0, y0)
        bottom_right = (x1, y1)
        if config.mode == "json":
            color = config.get_color()
        elif config.mode == "ocr_mode":
            color = config.get_color(score)

        draw.rectangle([top_left, bottom_right], outline=color, width=3)

        bbox = config.font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        text_x = top_left[0]
        text_y = top_left[1] - text_height - 2

        # Se o texto subir demais (sair da imagem), joga pra baixo da caixa
        if text_y < 0:
            text_y = bottom_right[1] + 2  # Desenha logo abaixo da caixa

        # Se ultrapassar a borda direita, ajusta para caber
        if text_x + text_width > img_pil.width:
            text_x = img_pil.width - text_width - 2

        # Se ultrapassar a borda esquerda
        if text_x < 0:
            text_x = 2

        # Contorno preto
        for dx in [-1, 1]:
            for dy in [-1, 1]:
                draw.text((text_x + dx, text_y + dy), text, font=config.font, fill=(0, 0, 0))

        # Texto principal branco
        draw.text((text_x, text_y), text, font=config.font, fill=(255, 255, 255))

        texto_bruto += f"OCR='{text}', score={score:.2f}, bbox=[{x0},{y0},{x1},{y1}]\n"

    # === Legenda na imagem ===
    legenda_textos = [
        ("Verde: Texto CORRETO (match com esperado)", (0, 255, 0)),
        ("Vermelho: Texto ERRADO (não bate com esperado)", (255, 0, 0))
    ]

    # Posição base da legenda
    lx, ly = 20, img_pil.height - 100

    for i, (legenda, cor) in enumerate(legenda_textos):
        draw.text((lx, ly + i * 30), legenda, fill=cor, font=config.font)

    # === Salva texto extraído ===
    txt_filename = os.path.join(path.resultados, f"{name_no_ext}_ocr.txt")
    with open(txt_filename, "w", encoding="utf-8") as f:
        f.write(texto_bruto)

    # === Salva imagem plotada ===
    plot_filename = os.path.join(path.resultados, f"{name_no_ext}_plotagem.jpg")
    img_pil.save(plot_filename)

    # === Exibe com Matplotlib ===
    img_final = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    plt.figure(figsize=(12, 16))  # Tamanho maior para melhor visualização  
    plt.imshow(cv2.cvtColor(img_final, cv2.COLOR_BGR2RGB))
    plt.axis("off")
    plt.title(f"OCR: {img_name}")
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)  # Preenche toda a figura
    plt.show()