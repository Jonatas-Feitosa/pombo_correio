# =========================================================================
# Projeto: Pombo correio - Automatização de mensagens
# Autor: jonatasitalofeitosa@gmail.com
# =========================================================================

# - Bibliotecas integradas (não são necessárias instalação)
import time
import os
import re

# - Bibliotecas de terceiros necessarias, caso não tenha instalada em sua maquina basta executar os comandos (pip instal...)
from selenium import webdriver  #pip install selenium
from webdriver_manager.chrome import ChromeDriverManager #pip install webdriver_manager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService

# - Bibliotecas importadas de arquivos
from converter_fotos import to_jpg as converter_fotos

#Indica o local das fotos para as publicações
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_fotos = os.path.join(diretorio_atual, 'Fotos/')

#Funcao que importa os contatos do documento
contatos = []
def importar_contatos():
    contatos.clear()
    with open("contatos.txt","r", encoding="utf-8") as arquivo:
        empresas = arquivo.readlines()
        for linha in empresas:
            contatos.append(linha)
    print(len(contatos),"contatos foram importados!")

#Funcao que importa as mensagems do documetno
mensagens = {}
def importar_mensagens():
    mensagens.clear
    with open("mensagens.txt","r", encoding="utf-8") as arquivo:
        marcas = arquivo.readlines()
        for linha in marcas:
            padrao = re.compile(r'(.*)(https?://\S+)')
            match = padrao.match(linha)

            chave = match.group(1).strip()
            link = match.group(2).strip()
            mensagens[chave] = link

    print(len(mensagens),"mensagens foram importadas!")

#Funcao que pesquisa o contato/grupo
def buscar_contato(contato):

    campo_pesquisa = driver.find_element("xpath",'/html/body/div[1]/div/div/div[4]/div/div[1]/div/div/div[2]/div/div')
    campo_pesquisa.send_keys('selecionando contato')
    campo_pesquisa.send_keys(Keys.CONTROL + 'A')
    texto_pesquisa = driver.find_element("xpath",'/html/body/div[1]/div/div/div[4]/div/div[1]/div/div/div[2]/div/div/p/span')
    #script para colar texto com emojis
    driver.execute_script(
      f'''
const text = `{contato}`;
const dataTransfer = new DataTransfer();
dataTransfer.setData('text', text);
const event = new ClipboardEvent('paste', {{
  clipboardData: dataTransfer,
  bubbles: true
}});
arguments[0].dispatchEvent(event)
''',
      texto_pesquisa)
    campo_pesquisa .send_keys(Keys.ENTER)
    time.sleep(1)

#Envia a mensagem
def enviar_mensagem(contato,mensagem,imagem=None):
    buscar_contato(contato)
    time.sleep(1)
    #anexa midia
    botao_anexo = driver.find_element("xpath","//div[@title='Anexar']")
    botao_anexo.click()
    importar_midia = driver.find_elements("xpath", "//input[@type='file']")[1]

    importar_midia.send_keys(str(imagem))
    time.sleep(1)

    caixa_de_mensagem = driver.find_element("xpath","//div[@title='Digite uma mensagem']")
    caixa_de_mensagem.send_keys(mensagem)
    caixa_de_mensagem.send_keys(Keys.ENTER)
    time.sleep(1)

#Funcao que inicia a opcao 2
def opcao2():
    converter_fotos()
    importar_contatos()
    importar_mensagens()

    time.sleep(3)
    os.system("cls") or None

    contador = 0
    for marca, link in mensagens.items():
        contador += 1
        contador_msg = '[' + str(contador) + '/' + str(len(mensagens)) + ']'
        for j, contato in enumerate(contatos):
            progresso = round((j / len(contatos)) * 100)
            print(f"{contador_msg} Postando {marca} ({progresso}%)", end="\r")
            caminho_da_foto = os.path.join(caminho_fotos, marca + ".jpg")
            enviar_mensagem(contato,(marca + ' ' + link),(caminho_da_foto))
        print(f"{contador_msg} Postando {marca} (100%)")

    os.system("cls") or None
    print("Publicações finalizadas\n")

#Procura as configurações locais do whatsapp para salvar a sessão
dir_path = os.getcwd()
profile = os.path.join(dir_path, "profile", "wpp")
opcoes = webdriver.ChromeOptions()
opcoes.add_argument(r"user-data-dir={}".format(profile))

#Abrir o site do WhatsApp
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=opcoes)
driver.get("https://web.whatsapp.com")

#Verifica se o WhatsApp está logado
print("Escaneie o QR code para continuar!")
while True:
    try:
        pesquisa = driver.find_element("xpath",'//*[@id="side"]/div[1]/div/div/div[2]/div/div[2]')
        os.system("cls") or None
        break
    except NoSuchElementException:
        print("Aguardando conexão.  ",end='\r')
        time.sleep(0.3)
        print("Aguardando conexão.. ",end='\r')
        time.sleep(0.3)
        print("Aguardando conexão...",end='\r')
        time.sleep(0.3)

os.system("cls") or None

# ========== Menu principal ========== #
while True:
    
    print('Selecione uma opção: \n0.Fechar app \n1.Texto simples (Inativa) \n2.Imagem com Texto e link')
    opcao = str(input('Opção: '))
 
    if opcao == "0":
        os.system("cls") or None
        print("Finalizando...")
        break
    elif opcao == "1":
        os.system("cls") or None
        print("Você escolheu a opção 1")

    elif opcao == "2":
        os.system("cls") or None
        print("Você escolheu a opção 2")
        opcao2()

    else:
        os.system("cls") or None
        print("Opção inválida. Tente novamente.")

    time.sleep(1)