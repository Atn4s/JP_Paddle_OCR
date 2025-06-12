import json
from PIL import ImageFont
from paddleocr import PaddleOCR

# === Fonte personalizada ===
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
try:
    font = ImageFont.truetype(font_path, size=40)
except:
    print("Erro ao carregar a fonte personalizada, usando fonte padrão.")
    font = ImageFont.load_default()

# === Define cores de acordo com o metodo de validaçãom ocr_mode interno, json validação externa ===
mode = "ocr_mode"  # Pode ser "json" ou "ocr_mode"

# === Inicializa OCR ===
ocr = PaddleOCR(
    use_dilation=False,         # Evita juntar por expansão
    ocr_version='PP-OCRv3',     # Versão do OCR
    use_angle_cls=True, 
    det_lang='pt',
    #det_lang = 'us',            # Defina um valor padrão, se necessário
    show_log=False,
)

# === Inicializa JSON (se necessário) ===
if mode == "json":
    with open("imagem1.json", "r", encoding="utf-8") as f:
        correcao_manual = json.load(f)
    correcao_iter = iter(correcao_manual)

# === Função universal de cor ===
def get_color(score=None):
    if mode == "json":
        try:
            dado = next(correcao_iter)
            if dado.get("correto") is True:
                return (0, 255, 0)
            elif dado.get("correto") is False:
                return (255, 0, 0)
            else:
                return (0, 0, 255)
        except StopIteration:
            return (0, 0, 255)
    elif mode == "ocr_mode":
        return (0, 255, 0) if score >= 0.85 else (255, 0, 0)
    return (0, 0, 255)