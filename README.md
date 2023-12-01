**Título:** Pombo Correio - Automatização de mensagens

**Descrição:**

Este projeto automatiza o envio de mensagens no WhatsApp. Ele pode ser usado para enviar mensagens simples ou mensagens com imagens e links.

**Requisitos:**

* Python 3
* Bibliotecas Selenium e webdriver_manager

**Instalação:**

```
pip install selenium
pip install pyperclip
pip install webdriver_manager
```

**Execução:**

```
python app.py
```

**Menu principal:**

Ao executar o código, você será apresentado ao menu principal. No menu, você pode escolher uma das seguintes opções:

* **0. Fechar app:** Finaliza o programa.
* **1. Texto simples:** Envia uma mensagem simples para todos os contatos.
* **2. Imagem com Texto e link:** Envia uma mensagem com uma imagem, um texto e um link para todos os contatos.

**Opção 2:**

A opção 2 é a mais complexa. Ela permite que você envie uma mensagem com uma imagem, um texto e um link para todos os contatos.

Para usar essa opção, você precisa criar dois arquivos de texto:

* **contatos.txt:** Este arquivo contém uma lista de contatos para os quais você deseja enviar a mensagem. Cada linha do arquivo deve conter um contato.
* **mensagens.txt:** Este arquivo contém uma lista de mensagens para os quais você deseja enviar a mensagem. Cada linha do arquivo deve conter uma mensagem.

O código irá converter todas as imagens mencionadas nas mensagens para o formato JPG. Em seguida, ele irá enviar uma mensagem para cada contato com a imagem, o texto e o link especificados.

**Exemplo:**

```
# contatos.txt (Cada linha corresponde a 1 contato, podendo ser nome, número de telefone ou nome de grupo)

contato1
contato2
contato3

# mensagens.txt (Cada linha corresponde a 1 mensagem)

Samsung - https://www.samsung.com/br/
Apple - https://www.apple.com/br/
Motorola - https://www.motorola.com.br/
```

Para as imagens corresponderem as mensagens, cada imagem deve estar renomeada com o texto antes do link da mensagem, ex:

```
Para entregar a imagem da samsung na mensagem dela que corresponde a ela:
mensagem: Nova linha galaxy, corfira: https://samsung.com.br
renomeie a imagem para: "Nova linha galaxy, confira:" sem as aspas
```

**Observações:**

* O código usa o WhatsApp Web para enviar mensagens. Portanto, você precisa ter uma conta do WhatsApp Web ativa.
* O código pode ser personalizado para atender às suas necessidades. Por exemplo, você pode adicionar mais opções ao menu principal ou alterar a maneira como as mensagens são formatadas.

**Espero que este código seja útil para você.**