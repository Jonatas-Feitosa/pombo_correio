import os
import time
import tkinter as tk
from tkinter import filedialog
from PIL import Image #pip install pillow

# Função para converter fotos para o formato jpg
def to_jpg(local='./Fotos'):
    arquivos = os.listdir(local)
    num_arquivos = len(arquivos)

    for x, arquivo in enumerate(os.listdir(local)):
        print(f'Convertendo fotos ({x+1}/{num_arquivos})', end='\r')

        # Verifica se o arquivo é uma imagem
        if arquivo.lower().endswith(('.png', '.jpeg', '.gif', '.bmp')):
            caminho_completo = os.path.join(local, arquivo)
            img = Image.open(caminho_completo)

            # Converte para RGB
            img = img.convert('RGB')

            # Salva a imagem como .jpg
            nome_jpg = os.path.splitext(arquivo)[0] + '.jpg'
            caminho_jpg = os.path.join(local, nome_jpg)
            img.save(caminho_jpg)

            # Exclui o arquivo original
            os.remove(caminho_completo)
    print(f'\nConvertendo fotos ({num_arquivos}/{num_arquivos})')
    return

def to_HD(local='./Fotos'):
    arquivos = os.listdir(local)
    num_arquivos = len(arquivos)

    for x, arquivo in enumerate(arquivos):
        print(f'Redimensionando fotos ({x+1}/{num_arquivos})', end='\r')
        caminho_completo = os.path.join(local, arquivo)
        imagem = Image.open(caminho_completo)

        largura, altura = imagem.size
        area_atual = largura * altura
        area_desejada = 921600

        if area_atual > area_desejada:
            fator_escala = (area_desejada / area_atual) ** 0.5
            nova_largura = int(largura * fator_escala)
            nova_altura = int(altura * fator_escala)

            imagem = imagem.resize((nova_largura,nova_altura))
            imagem.save(caminho_completo)

    print(f'Redimensionando fotos ({num_arquivos}/{num_arquivos})')
    return

def compress(local='./Fotos'):
    return

def selecionar_pasta():
    root = tk.Tk()
    root.withdraw()
    caminho_da_pasta = filedialog.askdirectory()

    if caminho_da_pasta:
       to_jpg(caminho_da_pasta)
       to_HD(caminho_da_pasta)
    
    else:
        to_jpg()

if __name__ == "__main__":
    print('========== Auto Edit - Editor de Fotos ==========')
    selecionar_pasta()
    print('============== Edições finalizadas ==============')