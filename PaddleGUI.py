import os
import cv2
import sys
import json
import easygui
import numpy as np
import matplotlib.pyplot as plt
from paddleocr import PaddleOCR
from PIL import Image, ImageDraw, ImageFont
import path 

# === Leitura JSON ===
with open("imagem1.json", "r", encoding="utf-8") as f:
    correcao_manual = json.load(f)

# Novo iterador com base no novo JSON (esperado, ocr, correto)
correcao_iter = iter(correcao_manual)  # <- Aqui inicializa o iterador

# === Caminho resultados obtidos ===
result_path = path.resultados

# === Caminho para iniciar o Paddle ===
load_path =  path.carregar_imagens

# === Fonte personalizada ===
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
try:
    font = ImageFont.truetype(font_path, size=40)
except:
    print("Erro ao carregar a fonte personalizada, usando fonte padrão.")
    font = ImageFont.load_default()

# === Define cores de acordo com o metodo de validaçãom ocr_mode interno, json validação externa ===
mode = "json"

# === Inicializa OCR ===
ocr = PaddleOCR(
    use_dilation=False,         # Evita juntar por expansão
    ocr_version='PP-OCRv3',     # Versão do OCR
    use_angle_cls=True, 
    lang='pt',
    #det_lang = 'us',            # Defina um valor padrão, se necessário
    show_log=False,
)

# === Seleciona imagem ===
try:
    img_path = sys.argv[1] if len(sys.argv) > 1 else easygui.fileopenbox(default=f"{load_path}/*")
except:
    print("Erro ao selecionar a imagem.")
    exit()

if not img_path:
    print("Nenhuma imagem selecionada.")
    exit()

# === Nome base do arquivo ===
img_name = os.path.basename(img_path)
name_no_ext = os.path.splitext(img_name)[0]

# === Lê a imagem com OpenCV e converte para PIL ===
img_cv = cv2.imread(img_path)
img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
img_pil = Image.fromarray(img_rgb)
draw = ImageDraw.Draw(img_pil)

# === OCR ===
result = ocr.ocr(img_path, cls=True)[0]

# === Processa OCR e desenha ===
texto_bruto = ""

if mode == "json":
    def get_color():
        try:
            dado = next(correcao_iter)
            if dado.get("correto") is True:
                return (0, 255, 0)  # Verde
            elif dado.get("correto") is False:
                return (255, 0, 0)  # Vermelho
            else:
                return (0, 0, 255)  # fallback
        except StopIteration:
            return (0, 0, 255)
elif mode == "ocr_mode":
    def get_color(score):
        return (0, 255, 0) if score >= 0.85 else (255, 0, 0)


for box, (text, score) in result:
    pts = np.array(box).astype(int)

    x0 = min(pts[0][0], pts[2][0])
    y0 = min(pts[0][1], pts[2][1])
    x1 = max(pts[0][0], pts[2][0])
    y1 = max(pts[0][1], pts[2][1])

    top_left = (x0, y0)
    bottom_right = (x1, y1)
    if mode == "json":
        color = get_color()
    elif mode == "ocr_mode":
        color = get_color(score)

    draw.rectangle([top_left, bottom_right], outline=color, width=3)

    bbox = font.getbbox(text)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    text_x = top_left[0]
    text_y = top_left[1] - text_height - 2

    # Contorno preto
    for dx in [-1, 1]:
        for dy in [-1, 1]:
            draw.text((text_x + dx, text_y + dy), text, font=font, fill=(0, 0, 0))

    # Texto principal branco
    draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255))

    texto_bruto += f"{text} (score={score:.2f})\n"

# === Legenda na imagem ===
legenda_textos = [
    ("Verde: Texto CORRETO (match com esperado)", (0, 255, 0)),
    ("Vermelho: Texto ERRADO (não bate com esperado)", (255, 0, 0)),
    ("Azul: Sem correspondência no JSON", (0, 0, 255))
]

# Posição base da legenda
lx, ly = 20, img_pil.height - 100

for i, (legenda, cor) in enumerate(legenda_textos):
    draw.text((lx, ly + i * 30), legenda, fill=cor, font=font)

# === Salva texto extraído ===
txt_filename = os.path.join(result_path, f"{name_no_ext}_ocr.txt")
with open(txt_filename, "w", encoding="utf-8") as f:
    f.write(texto_bruto)

# === Salva imagem plotada ===
plot_filename = os.path.join(result_path, f"{name_no_ext}_plotagem.jpg")
img_pil.save(plot_filename)

# === Exibe com Matplotlib ===
img_final = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
plt.figure(figsize=(12, 16))  # Tamanho maior para melhor visualização  
plt.imshow(cv2.cvtColor(img_final, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.title(f"OCR: {img_name}")
plt.tight_layout()
plt.show()