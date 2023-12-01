import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image

# Função para converter fotos para o formato jpg
def to_jpg(local='./Fotos'):
    for x, arquivo in enumerate(os.listdir(local)):
        progresso = (x // len(os.listdir(local))) * 100
        print(f'Convertendo fotos ({progresso})', end='\r')

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
    print('Convertendo fotos (100%)')
    return

def selecionar_pasta():
    root = tk.Tk()
    root.withdraw()
    caminho_da_pasta = filedialog.askdirectory()

    if caminho_da_pasta:
       to_jpg(caminho_da_pasta)
    
    else:
        to_jpg()

if __name__ == "__main__":
    selecionar_pasta()