import json
from PIL import ImageFont
from paddleocr import PaddleOCR

# === Fonte personalizada utilizada para plotagem, baseado no sistema Linux ===
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
try:    # Se encontrou a fonte será utilizada a DejaVuSans-Bold.ttf 
    font = ImageFont.truetype(font_path, size=40)
except: # Se não encontrou a fonte, será utilizada a fonte padrão do PIL
    print("Erro ao carregar a fonte personalizada, usando fonte padrão.")
    font = ImageFont.load_default()

# === Função para obter a fonte com tamanho dinâmico baseado no tamanho das bouding-boxes encontradas ===
def get_font(size=40):
    try:
        return ImageFont.truetype(font_path, size=size)
    except:
        print("Erro ao carregar a fonte personalizada, usando fonte padrão.")
        return ImageFont.load_default()

# === Opção para definir as cores de contorno dos bouding boxes de acordo com o metodo de validaçãom 
# caso seja ocr_mode o modo de validação é baseado no score do PaddleOCR definido como acuracia minima de 0.85
# caso o metodo seja json a validaçaõ é manual feita pelo usuário através de um arquivo json contendo a validação manual ===

mode = "ocr_mode"  # Modo de validação: "json" ou "ocr_mode"

# === Configurações do PaddleOCR  ===
ocr = PaddleOCR(
    use_dilation=False,         # A dilataçãao não foi utilizada
    ocr_version='PP-OCRv3',     # Versão do OCR utilizada atualmente é a PP-OCRv3
    use_angle_cls=True,         # Ativa a classificação de ângulo para melhorar a detecção de texto em diferentes orientações
    det_lang='pt',              # Definição do idioma para detecção de texto, definido como PORTUGUÊS
    #det_lang = 'us',           # Defina um valor padrão, se necessário
    show_log=False,             # Desativar logs de saída do PaddleOCR
)

# === Modo de validação manual via JSON ===
# Esse modo serve para fazer a validação manual dos resultados do OCR, onde o usuário pode corrigir os resultados e salvar em um arquivo JSON para 
# que o script possa fazer a plotagem das bouding boxes de acordo com a validação feita pelo usuário. A plotagem é feita sequencialemente, 
# ou seja, a cada iteração do loop, o script irá buscar o próximo dado do JSON e plotar a bouding box de acordo com a validação feita pelo usuário.
if mode == "json":
    with open("imagem1.json", "r", encoding="utf-8") as f:
        correcao_manual = json.load(f)
    correcao_iter = iter(correcao_manual)

# === Função definição de cor para a plotagem ===
def get_color(score=None):
    if mode == "json":                              # Se o modo for JSON, verifica a correção manual        
        try:
            dado = next(correcao_iter)
            if dado.get("correto") is True:         # caso o dado do json validado manualmente e feito pelo usuário esteja correto a cor será verde
                return (0, 255, 0)
            elif dado.get("correto") is False:      # caso o dado do json validado manualmente e feito pelo usuário esteja incorreto a cor será vermelha
                return (255, 0, 0)
            else:                                   # Se não houver correção manual, a cor será azul
                return (0, 0, 255)
        except StopIteration:
            return (0, 0, 255)
    elif mode == "ocr_mode":                                 # Se o modo for OCR, verifica o score do PaddleOCR, no qual está definido como 0.85
        return (0, 255, 0) if score >= 0.85 else (255, 0, 0) # se for maior ou igual a 0.85 a cor será verde, caso contrário será vermelha
    return (0, 0, 255)                                       # Se não houver modo definido, a cor será azul