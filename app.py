#bibliotecas necessarias, caso nao tenha instalada em sua maquina basta executar os comandos (pip instal....)
from selenium import webdriver  #pip install selenium
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager #pip install webdriver_manager
from selenium.common.exceptions import NoSuchElementException
import time
import os

#Abrir o Chrome
#testeaqui

dir_path = os.getcwd()
profile = os.path.join(dir_path, "profile", "wpp")
options = webdriver.ChromeOptions()
options.add_argument(r"user-data-dir={}".format(profile))

#Abrir o site do WhatsApp

driver = webdriver.Chrome("./chromedriver.exe", options=options)
driver.get("https://web.whatsapp.com")

#Verifica a sessão
print("Escaneie o QR code para continuar!")

while True:
    try:
        pesquisa = driver.find_element("xpath",'//*[@id="side"]/div[1]/div/div/div[2]/div/div[2]')
        break
    except NoSuchElementException:
        print("Aguardando conexão.  ",end='\r')
        time.sleep(0.3)
        print("Aguardando conexão.. ",end='\r')
        time.sleep(0.3)
        print("Aguardando conexão...",end='\r')
        time.sleep(0.3) 

time.sleep(10)

#Importa o documento contendo os contatos ou grupos para onde as mensagens serão enviadas    

contatos = []

with open("contatos.txt","r") as arquivo:
    empresas = arquivo.readlines()
    for linha in empresas:
        contatos.append(linha)

#Contatos/Grupos - Informar o nome(s) de Grupos ou Contatos que serao enviadas as mensagens
#contatos = ['Grupo de teste 1','Grupo de teste 2','Grupo de teste 3']

#Mensagem - Mensagem que sera enviada
texto = input('Digite a mensagem a ser enviada: ')
#link = ' ,enviada com python via selenium'

#Midia = imagem, pdf, documento, video (caminho do arquivo, lembrando que mesmo no windows o caminho deve ser passado com barra invertida */* ) 
#midia = "G:/Meu Drive/Trabalhos profissionais/python/Mandar mensagens em massa/Fotos/"

#Funcao que pesquisa o Contato/Grupo
def buscar_contato(contato):
    campo_pesquisa = driver.find_element("xpath",'//div[contains(@class,"copyable-text selectable-text")]')
    time.sleep(2)
    campo_pesquisa.click()
    campo_pesquisa.send_keys(contato)
    campo_pesquisa.send_keys(Keys.ENTER)

#Funcao que envia midia como mensagem
def enviar_msg(texto):

    #driver.find_element("css selector","#main > footer > div._2BU3P.tm2tP.copyable-area > div > span:nth-child(2) > div > div._3HQNh._1un-p > div._2jitM > div > div > span").click()
    #attach = driver.find_element("css selector","#main > footer > div._2BU3P.tm2tP.copyable-area > div > span:nth-child(2) > div > div._3HQNh._1un-p > div._2jitM > div > span > div > div > ul > li:nth-child(1) > button > input[type=file]")
    #attach.send_keys(foto)
    #time.sleep(1)
    campo_mensagem = driver.find_element("xpath",'//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[1]/p')
    campo_mensagem.send_keys(str(texto))
    campo_mensagem.send_keys(Keys.ENTER)
    time.sleep(1)
    send = driver.find_element("css selector","#app > div > div > div._2QgSC > div._2Ts6i._2xAQV > span > div > span > div > div > div.g0rxnol2.thghmljt.p357zi0d.rjo8vgbg.ggj6brxn.f8m0rgwh.gfz4du6o.r7fjleex.bs7a17vp > div > div._1HI4Y > div._33pCO")
    send.click()    

#Percorre todos os contatos/Grupos e envia as mensagens

for contato in contatos:
    buscar_contato(contato)     
    enviar_msg(texto) 
    time.sleep(0.5)
