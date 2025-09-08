from selenium.webdriver.common.by import By
from src.scrapper.acoes import *
from time import sleep

def login_ecg(navegador, usuario, senha):
    navegador.get('https://ecgglass.com/ecg_glass/login/login.php')
    escrever(navegador, By.NAME, 'text_usuario', usuario)
    escrever(navegador, By.NAME, 'password_senha', senha)
    clicar(navegador, By.CSS_SELECTOR, 'html body#bg_login_full div.container div#box_login_full form div.box_input.text-right input.btn.btn-primary')

def acessar_ordem_servico(navegador, ordem_de_servico):
    url = 'https://ecgglass.com/ecg_glass/geral/busca.php'
    if not navegador.current_url == url:
        navegador.get(url)
    escrever(navegador, By.ID, 'text_numero_os',ordem_de_servico)
    clicar(navegador, By.CSS_SELECTOR, 'div.formulario_filtro:nth-child(6) > div:nth-child(2) > input:nth-child(1)')

def acessar_orcamento(navegador, numero_orcamento):
    url = 'https://ecgglass.com/ecg_glass/geral/busca.php'
    if not navegador.current_url == url:
        navegador.get(url)
    escrever(navegador, By.ID, 'text_numero_orcamento', numero_orcamento)
    clicar(navegador, By.CSS_SELECTOR, 'div.formulario_filtro:nth-child(4) > div:nth-child(2) > input:nth-child(1)')

def acessar_dados_cliente(navegador, ordem_de_servico):
    url = 'https://ecgglass.com/ecg_glass/geral/busca.php'
    if not navegador.current_url == url:
        navegador.get(url)
    escrever(navegador, By.ID, 'text_numero_os', ordem_de_servico)
    clicar(navegador, By.CSS_SELECTOR, 'div.formulario_filtro:nth-child(6) > div:nth-child(2) > input:nth-child(1)')
    clicar(navegador, By.CSS_SELECTOR, 'a.f_16:nth-child(1)')
    clicar(navegador, By.CSS_SELECTOR, '.f_16 > b:nth-child(1)')

def acessar_listar_projetos(navegador, ordem_de_servico):
    url_parcial = 'https://ecgglass.com/ecg_glass/ordemServico/cadOrdemServico.php?tipo=view&cod='
    if url_parcial not in navegador.current_url:
        acessar_ordem_servico(navegador, ordem_de_servico)
    WebDriverWait(navegador, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")
    clicar(navegador, By.ID, 'item_menu_dinamico_0')

def pegar_dados_obra(navegador, ordem_de_servico, numero_orcamento):
    '''
    retorna um dicionario, com os itens 'area', 'cor', 'vidro' e preco.
    '''
    url_parcial = 'https://ecgglass.com/ecg_glass/ordemServico/cadOrdemServico.php?tipo=view&cod='
    if url_parcial not in navegador.current_url:
        acessar_ordem_servico(navegador, ordem_de_servico)
    WebDriverWait(navegador, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")
    clicar(navegador, By.ID, 'item_menu_dinamico_0')
    cor = ''
    vidro = ''
    listar_projetos = None
    try:
        cor = pegar_texto(navegador, By.CSS_SELECTOR, '.ml-3 > b:nth-child(1)').lower()
        vidro = pegar_texto(navegador, By.CSS_SELECTOR, 'div.row:nth-child(3) > div:nth-child(1) > label:nth-child(1) > b:nth-child(1)').lower()
    except:
        pass
    try:
        listar_projetos = navegador.find_element(By.NAME, 'itemProj')
    except:
        pass
    if listar_projetos:
        lista = Select(listar_projetos)
        for serial in lista.options:
            if '1-SACADA-KAIZEN' in serial.text or '2-PORTAS-KAIZEN' in serial.text:
                value = serial.get_attribute('value')
                selecionar_combo_box(navegador, By.NAME, 'itemProj', value)
                cor = pegar_texto(navegador, By.CSS_SELECTOR, '.ml-3 > b:nth-child(1)').lower()
                vidro = pegar_texto(navegador, By.CSS_SELECTOR, 'div.row:nth-child(3) > div:nth-child(1) > label:nth-child(1) > b:nth-child(1)').lower()
                break
    dados_obra = {
        'cor' : cor,
        'vidro' : vidro,
        }
    return dados_obra

def pegar_nome_cliente(navegador, ordem_de_servico):
    '''
    retorna um dicionario, com os itens 'nome', 'cpf', 'email', 'cep', 'numero', 'complemento' e 'telefone'.
    '''
    url_parcial = 'https://ecgglass.com/ecg_glass/pessoa/informacao.php?cod_pes='
    if url_parcial not in navegador.current_url:
        acessar_dados_cliente(navegador, ordem_de_servico)
    WebDriverWait(navegador, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")
    nome = pegar_texto(navegador, By.CSS_SELECTOR, '.font-weight-bold').title()
    return nome

def pegar_endereco_cliente(navegador, ordem_de_servico):
    '''
    retorna um dicionario, com os itens 'cep', 'numero', 'complemento' e 'telefone'.
    '''
    url_parcial = 'https://ecgglass.com/ecg_glass/pessoa/informacao.php?cod_pes='
    if url_parcial not in navegador.current_url:
        acessar_dados_cliente(navegador, ordem_de_servico)
    WebDriverWait(navegador, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")
    uf = pegar_texto(navegador, By.CSS_SELECTOR, 'form.formulario_cadastro:nth-child(3) > div:nth-child(7) > span:nth-child(2)')
    cidade = pegar_texto(navegador, By.CSS_SELECTOR, 'form.formulario_cadastro:nth-child(3) > div:nth-child(8) > span:nth-child(2)')
    bairro = pegar_texto(navegador, By.CSS_SELECTOR, 'form.formulario_cadastro:nth-child(3) > div:nth-child(9) > span:nth-child(2)')
    endereco = pegar_texto(navegador, By.CSS_SELECTOR, 'form.formulario_cadastro:nth-child(3) > div:nth-child(10) > span:nth-child(2) > a:nth-child(1)').strip().replace('.', '')
    logradouro = endereco.split(' ')[0]
    cep = pegar_texto(navegador, By.CSS_SELECTOR, 'form.formulario_cadastro:nth-child(3) > div:nth-child(6) > span:nth-child(2)')
    numero = pegar_texto(navegador, By.CSS_SELECTOR, 'form.formulario_cadastro:nth-child(3) > div:nth-child(11) > span:nth-child(2)')
    complemento = pegar_texto(navegador, By.CSS_SELECTOR, 'div.campo:nth-child(12) > span:nth-child(2)').title()

    endereco_cliente = {
    'cep' : cep,
    'uf' : uf,
    'cidade' : cidade,
    'bairro' : bairro,
    'endereco' : endereco,
    'logradouro' : logradouro,
    'numero' : numero,
    'complemento' : complemento,
    }
    return endereco_cliente

def pegar_enderecos_extras(navegador, ordem_de_servico):
    url_parcial = 'https://ecgglass.com/ecg_glass/pessoa/informacao.php?cod_pes='
    if url_parcial not in navegador.current_url:
        acessar_dados_cliente(navegador, ordem_de_servico)
    WebDriverWait(navegador, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")
    clicar(navegador, By.ID, 'endereco-instalacao-tab')

    lista_enderecos = navegador.findElements(By.CSS_SELECTOR, '#endereco-instalacao > form:nth-child(2)')
    dados_enderecos_extras = []

    for endereco in lista_enderecos:
        cep = pegar_texto(navegador, By.CSS_SELECTOR, '#endereco-instalacao > form:nth-child(2) > div:nth-child(6) > span:nth-child(2)')
        numero = pegar_texto(navegador, By.CSS_SELECTOR, '#endereco-instalacao > form:nth-child(2) > div:nth-child(11) > span:nth-child(2)')
        complemento = pegar_texto(navegador, By.CSS_SELECTOR, '#endereco-instalacao > form:nth-child(2) > div:nth-child(12) > span:nth-child(2)').title()
        uf = pegar_texto(navegador, By.CSS_SELECTOR, '#endereco-instalacao > form:nth-child(2) > div:nth-child(7) > span:nth-child(2)')
        cidade = pegar_texto(navegador, By.CSS_SELECTOR, '#endereco-instalacao > form:nth-child(2) > div:nth-child(8) > span:nth-child(2)')
        bairro = pegar_texto(navegador, By.CSS_SELECTOR, '#endereco-instalacao > form:nth-child(2) > div:nth-child(9) > span:nth-child(2)')
        endereco = pegar_texto(navegador, By.CSS_SELECTOR, '#endereco-instalacao > form:nth-child(2) > div:nth-child(10) > span:nth-child(2) > a:nth-child(1)').strip().replace('.', '')
        logradouro = endereco.split(' ')[0]

        endereco_extra = {
        'cep' : cep,
        'uf' : uf,
        'cidade' : cidade,
        'bairro' : bairro,
        'endereco' : endereco,
        'logradouro' : logradouro,
        'numero' : numero,
        'complemento' : complemento,
        }

        dados_enderecos_extras.append(endereco_extra)

    return dados_enderecos_extras

def pegar_data_aprovacao(navegador, ordem_de_servico):
    numero_orcamento = ordem_de_servico[:-2]
    acessar_orcamento(navegador, numero_orcamento)
    data_aprovacao = pegar_texto(navegador, By.CSS_SELECTOR, 'td.col-xs-2:nth-child(3) > b:nth-child(1)')
    return data_aprovacao