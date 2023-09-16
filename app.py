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
import pyperclip #pip install pyperclip
#importar função de converter fotos do arquivo local
from converter_fotos import converter_imagens


from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


#Indica o local das fotos para as publicações
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_fotos = os.path.join(diretorio_atual, 'Fotos/')

#Funcao que importa os contatos do documento
contatos = []
def importar_contatos():
    print("Importando contatos...")

    with open("contatos.txt","r", encoding="utf-8") as arquivo:
        empresas = arquivo.readlines()
        for linha in empresas:
            contatos.append(linha)

    print(len(contatos),"contatos foram importados!")

#Funcao que importa as mensagems do documetno
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

#Funcao que pesquisa o contato/grupo
def buscar_contato(contato):

    #Procura o campo de pesquisa
    campo_pesquisa = driver.find_element("xpath",'/html/body/div[1]/div/div/div[4]/div/div[1]/div/div/div[2]/div/div[1]/p')
    
    pyperclip.copy(contato)

    campo_pesquisa.send_keys(Keys.SHIFT, Keys.INSERT)
    campo_pesquisa.send_keys(Keys.ENTER)
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
    time.sleep(2)

    # Copia a mensagem para a área de transferência
    driver.execute_script('navigator.clipboard.writeText(arguments[0]);', mensagem)
    actions = ActionChains(driver)

    # Adiciona a ação de pressionar Ctrl + V
    actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL)

    # Executa as ações
    actions.perform()
    time.sleep(1)
    actions.send_keys(Keys.ENTER)
    actions.perform()

    time.sleep(5)

#Funcao que abre as conversas arquivadas (atualmente não usado)
def abrir_conversas_arquivadas():
    gaveta_arquivadas = driver.find_element("xpath",'//*[@id="pane-side"]/button/div/div[2]/div')
    gaveta_arquivadas.click()

#Funcao que inicia a opcao 2
def opcao2():
    print("\n")
    converter_imagens()
    importar_contatos()
    importar_mensagens()
    print("\n")
    for marca, link in mensagens.items():
        print("Postando " + marca)

        for contato in contatos:
            caminho_da_foto = os.path.join(caminho_fotos, marca + ".jpg")
            enviar_mensagem(contato,(marca + ' ' + link),(caminho_da_foto))
    print("Publicações finalizadas\n")

#Procura as configurações locais do whatsapp para salvar a sessão
dir_path = os.getcwd()
profile = os.path.join(dir_path, "profile", "wpp")
opcoes = webdriver.ChromeOptions()
opcoes.add_argument(r"user-data-dir={}".format(profile))

#Abrir o site do WhatsApp
driver = webdriver.Chrome(ChromeDriverManager().install(), options=opcoes)
driver.get("https://web.whatsapp.com")

#Verifica se o WhatsApp está logado
print("Escaneie o QR code para continuar!")
while True:
    try:
        pesquisa = driver.find_element("xpath",'//*[@id="side"]/div[1]/div/div/div[2]/div/div[2]')
        print("Conectado              ")
        print('====================')
        break
    except NoSuchElementException:
        print("Aguardando conexão.  ",end='\r')
        time.sleep(0.3)
        print("Aguardando conexão.. ",end='\r')
        time.sleep(0.3)
        print("Aguardando conexão...",end='\r')
        time.sleep(0.3) 

# ========== Menu principal ========== #
while True:
    print('Selecione uma opção: \n0.Fechar app \n1.Texto simples \n2.Imagem com Texto e link')
    opcao = str(input('Opção: '))
    print('====================')
 
    if opcao == "0":
        # código para a opção 1
        print("Finalizando...")
        break
    elif opcao == "1":
        # código para a opção 2
        print("Você escolheu a opção 1")

    elif opcao == "2":
        print("Você escolheu a opção 2")
        opcao2()

    else:
        # opção inválida
        print("Opção inválida. Tente novamente.")

    time.sleep(1)