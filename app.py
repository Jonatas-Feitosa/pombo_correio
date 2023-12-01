import time
import os
import re
import sys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from converter_fotos import to_jpg as converter_fotos
from auth import autenticar

if getattr(sys, 'frozen', False):
    # Executando em um executável (PyInstaller)
    diretorio_atual = sys._MEIPASS
else:
    # Executando o script diretamente
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))


doc_contatos = os.path.join(diretorio_atual, 'contatos.txt')
doc_mensagens = os.path.join(diretorio_atual, 'mensagens.txt')
caminho_fotos = os.path.join(diretorio_atual, 'Fotos/')

def iniciar_driver(headless=False):
    dir_path = os.getcwd()
    profile = os.path.join(dir_path, "profile", "wpp")
    opcoes = webdriver.ChromeOptions()
    opcoes.add_argument(r"user-data-dir={}".format(profile))
    if headless:
        opcoes.add_argument("--headless=new")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=opcoes)
    driver.get("https://web.whatsapp.com")
    return driver

def verificar_sessao(driver):
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

def importar_contatos():
    contatos = []
    with open(doc_contatos,"r", encoding="utf-8") as arquivo:
        empresas = arquivo.readlines()
        for linha in empresas:
            contatos.append(linha)
    print(len(contatos),"contatos foram importados!")
    return contatos

def importar_mensagens():
    mensagens = {}
    with open(doc_mensagens,"r", encoding="utf-8") as arquivo:
        marcas = arquivo.readlines()
        for linha in marcas:
            padrao = re.compile(r'(.*)(https?://\S+)')
            match = padrao.match(linha)

            chave = match.group(1).strip()
            link = match.group(2).strip()
            mensagens[chave] = link
    print(len(mensagens),"mensagens foram importadas!")
    return mensagens

def colar_emoji(driver,texto,elemento):
    driver.execute_script(
      f'''
    const text = `{texto}`;
    const dataTransfer = new DataTransfer();
    dataTransfer.setData('text', text);
    const event = new ClipboardEvent('paste', {{
    clipboardData: dataTransfer,
    bubbles: true
    }});
    arguments[0].dispatchEvent(event)
    ''',
      elemento)

def buscar_contato(driver,contato):
    campo_pesquisa = driver.find_element("xpath","//div[@title='Caixa de texto de pesquisa']")
    
    while True:
        try:
            campo_pesquisa.send_keys('selecionando contato')
            campo_pesquisa.send_keys(Keys.CONTROL + 'A')
            time.sleep(0.5)
            texto_pesquisa = campo_pesquisa.find_element("xpath",'./p/span')
            colar_emoji(driver,contato,texto_pesquisa)
            campo_pesquisa .send_keys(Keys.ENTER)
            time.sleep(1)
            nome_contato = driver.find_element("xpath",'//*[@id="main"]/header/div[2]/div[1]/div/span')
            if contato[0:-2] in nome_contato.get_attribute('textContent'):
                break
        except NoSuchElementException:
            time.sleep(0.1)

def enviar_mensagem(driver,mensagem,imagem=None):
    botao_anexo = driver.find_element("xpath","//div[@title='Anexar']")
    botao_anexo.click()
    importar_midia = driver.find_elements("xpath", "//input[@type='file']")[1]

    importar_midia.send_keys(str(imagem))
    time.sleep(1)

    caixa_de_mensagem = driver.find_element("xpath","//div[@title='Digite uma mensagem']")
    caixa_de_mensagem.send_keys(mensagem)
    caixa_de_mensagem.send_keys(Keys.ENTER)
    time.sleep(1)

def opcao2(driver):
    converter_fotos(caminho_fotos)
    contatos = importar_contatos()
    mensagens = importar_mensagens()
    time.sleep(1)
    os.system("cls") or None

    contador = 0
    for marca, link in mensagens.items():
        contador += 1
        contador_msg = '[' + str(contador) + '/' + str(len(mensagens)) + ']'
        for j, contato in enumerate(contatos):
            buscar_contato(driver,contato)
            progresso = round((j / len(contatos)) * 100)
            print(f"{contador_msg} Postando {marca} ({progresso}%)                                    ", end="\r")
            caminho_da_foto = os.path.join(caminho_fotos, marca + ".jpg")
            enviar_mensagem(driver,(marca + ' ' + link),(caminho_da_foto))
        print(f"{contador_msg} Postando {marca} (100%)")
    os.system("cls") or None
    print("Publicações finalizadas")

def opcao3(driver):
    conversas_arquivas = driver.find_element("xpath","//*[@id='pane-side']/button/div/div[2]/div/div")
    conversas_arquivas.click()
    converter_fotos()
    contatos = importar_contatos()
    mensagens = importar_mensagens()
    
    time.sleep(3)

    #elementos_grupos = driver.find_elements("xpath","//div[@class='lhggkp7q ln8gz9je rx9719la']")
    elementos_grupos = driver.find_elements("xpath",f"//span[contains(@title,'Grupo')]")
    grupos = elementos_grupos[1:len(contatos)-1]

    for i in range(len(contatos)):
        for j in range(len(grupos)):
            if (contatos[i])[1:-1] in grupos[j].get_attribute('textContent'):
                print(f'achado o nome {grupos[j].get_attribute("textContent")} em: {contatos[i]}')
    time.sleep(10)

def menu():
    if autenticar():
        driver = iniciar_driver()
        verificar_sessao(driver)
        while True:
            print('''
Selecione uma opção:
0. Fechar app
1. Texto simples (Inativa)
2. Imagem com Texto e link
3. Imagem com Texto e link (Modo headless *experimental)
            ''')
            opcao = input('Opção: ')
            
            if opcao == "0":
                os.system("cls") or None
                print("Finalizando...")
                driver.close()
                break
            elif opcao == "1":
                os.system("cls") or None
                print("Você escolheu a opção 1")
            elif opcao == "2":
                os.system("cls") or None
                time.sleep(10)
                print("Você escolheu a opção 2")
                opcao2(driver)
            elif opcao == "3":
                os.system("cls") or None
                print("Você escolheu a opção 3")
                driver.close()
                driver = iniciar_driver(True)
                verificar_sessao(driver)
                opcao2(driver)
            else:
                os.system("cls") or None
                print("Opção inválida. Tente novamente.")
            time.sleep(1)

if __name__ == "__main__":
    menu()