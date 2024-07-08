import time
import os
import re
import sys
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from converter_fotos import to_jpg as converter_fotos
from converter_fotos import to_HD as redimensionar_fotos
from auth import autenticar

# identificar o diretório atual
if getattr(sys, 'frozen', False):
    # Executando em um executável (PyInstaller)
    diretorio_atual = sys._MEIPASS
else:
    # Executando o script diretamente
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))

# Biblioteca para gerenciar erros
logging.basicConfig(
    filename="log_info.log",  # Nome do arquivo de log
    level=logging.WARNING,  # Nível de log mínimo
    #format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Formato da mensagem de log
    format='''==================================================
Data: %(asctime)s
Origem: %(name)s
Nível: %(levelname)s
Mensagem: %(message)s
==================================================''',  # Formato da mensagem de log
)
logger = logging.getLogger(__name__)  # Nome do logger

doc_contatos = os.path.join(diretorio_atual, 'contatos.txt')
doc_mensagens = os.path.join(diretorio_atual, 'mensagens.txt')
caminho_fotos = os.path.join(diretorio_atual, 'Fotos\\')

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
    reticencias = ''
    while True:
        try:
            pesquisa = driver.find_element("xpath",'//*[@id="side"]/div[1]/div/div/div[2]/div/div[2]')
            time.sleep(3)
            os.system("cls") or None
            break
        except NoSuchElementException:
            reticencias += '.'
            if len(reticencias) > 3:
                reticencias = ''
            os.system("cls") or None
            print(f'''========== Pombo Correio - Envio de Mensagens ==========
                  
Escaneie o QR code para continuar!
Aguardando conexão{reticencias}

========================================================''')
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
    try:
        campo_pesquisa = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Caixa de texto de pesquisa']"))
        )
        logger.info('Campo de pesquisa encontrado')
    except Exception as e:
        logger.error(f'Erro ao encontrar o campo de pesquisa: {e}')
        return

    while True:
        try:
            campo_pesquisa.send_keys('selecionando contato')
            campo_pesquisa.send_keys(Keys.CONTROL + 'A')
            logger.info('Enviando comandos de seleção de contato')

            texto_pesquisa = WebDriverWait(campo_pesquisa, 10).until(
                EC.presence_of_element_located((By.XPATH, "./p/span"))
            )
            logger.info('Texto de pesquisa encontrado')

            colar_emoji(driver, contato, texto_pesquisa)
            time.sleep(1)
            campo_pesquisa.send_keys(Keys.ENTER)
            logger.info('Pressionando ENTER para selecionar o contato')

            nome_contato = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/header/div[2]/div[1]/div/span'))
            )
            logger.info('Nome do contato encontrado')

            if contato[0:-2] in nome_contato.get_attribute('textContent'):
                logger.info('Contato encontrado com sucesso')
                break
        except NoSuchElementException as e:
            logger.warning(f'Elemento não encontrado, tentando novamente: {e}')
            time.sleep(0.1)
        except Exception as e:
            logger.error(f'Ocorreu um erro inesperado: {e}')
            break

def enviar_imagem(driver, legenda, imagem):
    try:
        botao_anexo = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@title='Anexar']"))
        )
        botao_anexo.click()
        logger.info('Botão de anexo clicado')
    except Exception as e:
        logger.error(f'Erro ao clicar no botão de anexo: {e}')
        return

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
        )
        importar_imagem = driver.find_elements(By.XPATH, "//input[@type='file']")[1]
        importar_imagem.send_keys(str(imagem))
        logger.info(f'Imagem {imagem} enviada para o campo de upload')
    except Exception as e:
        logger.error(f'Erro ao enviar a imagem: {e}')
        return

    try:
        caixa_de_legenda = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Adicione uma legenda']"))
        )
        caixa_de_legenda.send_keys(legenda)
        caixa_de_legenda.send_keys(Keys.ENTER)
        logger.info('Legenda enviada com sucesso')
        time.sleep(3)
    except Exception as e:
        logger.error(f'Erro ao enviar a legenda: {e}')
        return

def verificar_imagens(mensagens):
    imagens_faltando = ''
    total_verificadas = len(mensagens)
    total_faltando = 0
    for msg, link in mensagens.items():
        caminho = msg + '.jpg'
        if not os.path.exists(caminho_fotos + caminho):
            imagens_faltando += f'{caminho}\n'
            total_faltando += 1

    if total_faltando > 0:
        print(f'''
    Não foram encontradas {total_faltando}/{total_verificadas} imagens:
{imagens_faltando}''')
    return total_faltando

def opcao2(driver):
    os.system("cls") or None
    print('============== Preparando postagens ==============')

    converter_fotos(caminho_fotos)
    redimensionar_fotos(caminho_fotos)
    contatos = importar_contatos()
    mensagens = importar_mensagens()
    
    # Verifica se todas as imagens existem
    integridade = verificar_imagens(mensagens)
    while integridade > 0:
        print('''Escolha uma opção abaixo: 
1. Continuar mesmo assim
2. Verificar novamente
0. Fechar app''')
        opcao = input('Opção: ')
        if  opcao == '1':
            integridade = 0
        elif opcao == '2':
            mensagens = importar_mensagens()
            converter_fotos(caminho_fotos)
            redimensionar_fotos(caminho_fotos)
            integridade = verificar_imagens(mensagens)
        elif opcao == '0':
            driver.sys.exit()
            sys.exit()
        else:
            print('Opção invalida, tente novamente ❌')
            continue

    os.system("cls") or None
    print('============== Iniciando postagens ==============')
    contador = 0

    # Loop para cada postagem
    for marca, link in mensagens.items():
        contador += 1
        contador_msg = '[' + str(contador) + '/' + str(len(mensagens)) + ']'

        # Loop para cada grupo
        for j, contato in enumerate(contatos):
            progresso = round((j / len(contatos)) * 100)
            print(f"{contador_msg} Postando {marca} ({progresso}%)                                    ", end="\r")
            caminho_da_foto = os.path.join(caminho_fotos, marca + ".jpg")

            buscar_contato(driver,contato)
            enviar_imagem(driver,(marca + ' ' + link),(caminho_da_foto))
            
        print(f"{contador_msg} Postando {marca} ✅         ")

    os.system("cls") or None
    print("Publicações finalizadas ✅")

def opcao3(driver):
    conversas_arquivas = driver.find_element("xpath","//*[@id='pane-side']/button/div/div[2]/div/div")
    conversas_arquivas.click()
    converter_fotos()
    contatos = importar_contatos()
    mensagens = importar_mensagens()
    
    time.sleep(3)

    elementos_grupos = driver.find_elements("xpath",f"//span[contains(@title,'Grupo')]")
    grupos = elementos_grupos[1:len(contatos)-1]

    for i in range(len(contatos)):
        for j in range(len(grupos)):
            if (contatos[i])[1:-1] in grupos[j].get_attribute('textContent'):
                print(f'achado o nome {grupos[j].get_attribute("textContent")} em: {contatos[i]}')
    time.sleep(10)

def info():
    print('''             
============== Como usar o Pombo Correio? ==============

1. Coloque os nomes dos grupos no arquivo 'contatos.txt'
   um grupo por linha, não envie mensagens para contatos
   , seu número pode ser bloqueado por isso!
                                     
2. Defina as mensagens no arquivo 'mensagens.txt', uma 
   linha por mensagem, cada linha deve conter texto e 
   link, o app usará o texto para buscar as imagens.
                      
3. Coloque as imagens na pasta 'imagens', elas devem 
   estar renomeadas com o texto (sem link) de cada 
   mensagem, as imagens serão redimensionadas e 
   convertidas para jpg automaticamente.

4. Selecione uma opção de envio.
                  
========================================================                 
            ''')
    input('Aperte qualquer tecla para voltar: ')
    os.system("cls") or None
    return
    
def menu():
    if autenticar():
        driver = iniciar_driver()
        verificar_sessao(driver)
        while True:
            print('''========== Pombo Correio - Envio de Mensagens ==========
                  
Selecione uma opção:
0. Fechar app
1. Como usar?
2. Imagem com Texto e link
3. Imagem com Texto e link (Modo headless) *experimental
                  
========================================================''')
            opcao = input('Opção: ')
            
            if opcao == "0":
                os.system("cls") or None
                print("Finalizando...")
                driver.close()
                sys.exit()
            elif opcao == "1":
                os.system("cls") or None
                info()
            elif opcao == "2":
                opcao2(driver)
            elif opcao == "3":
                os.system("cls") or None
                driver.close()
                driver = iniciar_driver(headless=True)
                verificar_sessao(driver)
                opcao2(driver)
            else:
                os.system("cls") or None
                print("Opção inválida. Tente novamente.")
            time.sleep(1)
    else:
        print('Não foi possível inciar o app, contate o desenvolvedor')
        logger.error("Não foi possível verificar a autenticação para utilizar o app")
        time.sleep(5)
        sys.exit()

if __name__ == "__main__":
    menu()