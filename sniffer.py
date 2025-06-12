import easygui
from exif import Image


def revela_dono(img):
    if not img.has_exif:
        print("🧼 Imagem limpa. Nada a ver aqui.")
        return

    print("🕵️ [ALERTA] Dados sensíveis detectados:\n")
    for tag in sorted(my_image.list_all()):
        try:
            valor = getattr(my_image, tag)
            print(f"🔸 {tag}: {valor}")
        except Exception as e:
            print(f"⚠️ {tag}: erro ao acessar ({e})")

image_file = easygui.fileopenbox()
my_image = Image(image_file)

def limpar_metadados(img):
    if img.has_exif:
        img.delete_all()
        print(f"\n🧼 Metadados removidos com sucesso!")
    else:
        print("✅ Nenhum metadado para remover.")

print("BEM VINDO AO EXIFFER! Você tem dados na sua imagem?")
revela_dono(my_image)
print("Para garantir a segurança vamos limpar!")
limpar_metadados(my_image)
print("Vamos testar novamente!")
revela_dono(my_image)