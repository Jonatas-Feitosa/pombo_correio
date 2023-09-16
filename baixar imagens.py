#bibliotecas necessarias, caso nao tenha instalada em sua maquina basta executar os comandos (pip instal....)
from selenium import webdriver  #pip install selenium
from webdriver_manager.chrome import ChromeDriverManager #pip install webdriver_manager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import re
import random
import urllib.request
import requests #pip install requests bs4
from bs4 import BeautifulSoup

mensagens = {}
def importar_mensagens():
    print("Importando mensagens...")

    with open("mensagens.txt","r", encoding="utf-8") as arquivo:
        marcas = arquivo.readlines()
        for linha in marcas:
            padrao = re.compile(r'(.*)(https?://\S+)')
            match = padrao.match(linha)

            chave = match.group(1).strip()
            link = match.group(2).strip()
            mensagens[chave] = link

    print(len(mensagens),"mensagens foram importadas!")

#Abrir o site do WhatsApp
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://modacaruaru.com.br")
importar_mensagens()

time.sleep(5)


for marca, link in mensagens.items():
    print("Baixando " + marca)
    #pesquisa a marca
    pesquisa = driver.find_element("xpath","/html/body/div[1]/div[1]/div/div/div/div/div/span/div/form/div/input")
    pesquisa.click()
    pesquisa.send_keys(marca)
    pesquisa.send_keys(Keys.ENTER)
    time.sleep(3)
    nome_da_marca = driver.find_element("xpath","//h5[contains(text(), '" + marca + "')]")
    nome_da_marca.click()
    
    #baixa a imagem
    endereco_atual = driver.current_url
    pagina = requests.get(endereco_atual)
    imagens = BeautifulSoup(pagina.content,"html.parser")
    imagens = imagens.find_all("img")
    imagens = imagens[5:-5]
    print(random.choice(imagens))

    #imagem_aleatoria = random.choice(imagens)
    #url_imagem = imagem_aleatoria.get_attribute("src")
    #caminho_para_salvar = os.path.join(os.getcwd(), "Imagens baixadas", marca + ".png")
    #urllib.request.urlretrieve(url_imagem, caminho_para_salvar)

    time.sleep(30)


