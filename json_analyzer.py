import json
import os
import sys
import easygui
import path

# === Função de classificação ===
def classifica(item):
    if item["correto"]:
        return "VP" if item["esperado"] == item["ocr"] else "VN"
    else:
        return "FP" if item["ocr"] != item["esperado"] else "FN"

# === Obter arquivo JSON via argumento ou EasyGUI ===
def obter_arquivo_json():
    if len(sys.argv) > 1:
        return sys.argv[1]
    elif easygui:
        return easygui.fileopenbox(title="Selecione o arquivo JSON", filetypes=["*.json"])
    else:
        print("Uso: python script.py arquivo.json")
        sys.exit(1)

arquivo = obter_arquivo_json()

# === Carregamento dos dados ===
with open(arquivo, "r", encoding="utf-8") as f:
    dados = json.load(f)

resultados_detalhados = []
classificacoes = []

# === Análise item por item ===
for i, item in enumerate(dados, start=1):
    tipo = classifica(item)
    classificacoes.append(tipo)
    resultados_detalhados.append(
        f"{i:03d}) ESPERADO: \"{item['esperado']}\" | OCR: \"{item['ocr']}\" => {tipo}"
    )

# === Contagem para matriz pai ===
vp = classificacoes.count("VP")
vn = classificacoes.count("VN")
fp = classificacoes.count("FP")
fn = classificacoes.count("FN")
total_analisados = len(classificacoes)

# === Construção do texto final ===
saida = []
saida.append(f"Arquivo analisado: {os.path.basename(arquivo)}")
saida.append("Resultados por item:")
saida.extend(resultados_detalhados)
saida.append("\nMatriz de Confusão Geral:")
saida.append("         VP\tVN")
saida.append(f"FP\t {vp}\t{vn}")
saida.append(f"FN\t {fp}\t{fn}")
saida.append("")
saida.append(f"Total de itens analisados: {total_analisados}\n")

texto_final = "\n".join(saida)

# === Exibe no terminal ===
print(texto_final)

# === Salvar como TXT com nome correspondente ===
result_path = path.matriz_confusao
nome_saida = os.path.splitext(os.path.basename(arquivo))[0] + "_matriz_confusao.txt"
caminho_completo = os.path.join(result_path, nome_saida)

# Garante que o diretório exista
os.makedirs(os.path.dirname(caminho_completo), exist_ok=True)

with open(caminho_completo, "w", encoding="utf-8") as f:
    f.write(texto_final)

print(f"\nMatriz salva em: {result_path}{nome_saida}")

