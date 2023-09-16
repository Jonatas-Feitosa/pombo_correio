from PIL import Image #pip install Pillow
import os

# Recebe o caminho da pasta do usuário
pasta = './Fotos'

# Loop pelos arquivos da pasta
def converter_imagens():
    print('Convertendo fotos')
    for arquivo in os.listdir(pasta):
        # Verifica se o arquivo é uma imagem
        if arquivo.lower().endswith(('.png', '.jpeg', '.gif', '.bmp')):
            # Abre a imagem
            caminho_completo = os.path.join(pasta, arquivo)
            img = Image.open(caminho_completo)

            # Converte para RGB
            img = img.convert('RGB')

            # Salva a imagem como .jpg
            nome_jpg = os.path.splitext(arquivo)[0] + '.jpg'
            caminho_jpg = os.path.join(pasta, nome_jpg)
            img.save(caminho_jpg)

            # Exclui o arquivo original
            os.remove(caminho_completo)
    print('Fotos convertidas')
    return "Concluido"