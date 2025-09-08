from src.scrapper.acoes import *
from src.scrapper.config import usuario_ecg, senha_ecg
from src.scrapper.pipeline_scrapper import *
from src.scrapper.scrapper_ecg import *

def cadastrar_sacada(dados_sacada, lista_ferragens, lista_perfis_rolo):
    navegador = abrir_navegador()
    login_ecg(navegador, usuario_ecg, senha_ecg)
    acessar_ordem_servico(navegador, dados_sacada['ordem_servico'])
    acessar_listar_projetos(navegador, dados_sacada['ordem_servico'])
    clicar(navegador, By.CSS_SELECTOR, '#item_menu_dinamico_2')
    clicar(navegador, By.CSS_SELECTOR, '#pills-9 > div:nth-child(1) > div:nth-child(2) > a:nth-child(1)')
    clicar(navegador, By.CSS_SELECTOR, 'div.col-xl-2:nth-child(3) > div:nth-child(2) > a:nth-child(1) > img:nth-child(1)')
    escrever(navegador, By.ID, 'medida1', lista_perfis_rolo['comprimento_polietileno'])
    escrever(navegador, By.ID, 'medida2', dados_sacada['altura_vao'])
    escrever(navegador, By.ID, 'medida3', len(dados_sacada['aberturas']))
    escrever(navegador, By.ID, 'medida4', len(dados_sacada['giratorios']))

    if dados_sacada['quantidade_pe3'] == 2:
        possibilidade_pe3 = '1336'
    elif dados_sacada['quantidade_pe3'] == 3:
        possibilidade_pe3 = '1337'
    else:
        possibilidade_pe3 = '1362'

    selecionar_combo_box(navegador, By.NAME, 'select_possibilidade_opcao[]', possibilidade_pe3)
    clicar(navegador, By.ID, 'btnCadastrar')

    url_parcial = 'https://ecgglass.com/ecg_glass/projetos/admProjetos/gera_proj.php?tipo'
    while url_parcial not in navegador.current_url:
        sleep(1)
    WebDriverWait(navegador, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")
    apagar_itens_ferragens_ecg(navegador)
    apagar_itens_perfis_ecg(navegador)
    adicionar_itens_ferragem_ecg(navegador, lista_ferragens)

def apagar_itens_ferragens_ecg(navegador):
    itens = navegador.find_elements(By.CSS_SELECTOR, '#tabela_F > tbody > tr')
    itens.pop(0)
    itens.pop(-1)
    for i, item in enumerate(itens):
        escrever(navegador, By.ID, f'F{i}qtd', '0')

def apagar_itens_perfis_ecg(navegador):
    itens = navegador.find_elements(By.CSS_SELECTOR, '#tabela_P > tbody > tr')
    itens.pop(0)
    itens.pop(-1)
    for i, item in enumerate(itens):
        escrever(navegador, By.ID, f'P{i}qtd', '0')

def adicionar_itens_ferragem_ecg(navegador, lista_ferragens):
    itens = navegador.find_elements(By.CSS_SELECTOR, '#tabela_P > tbody > tr')
    itens.pop(0)
    itens.pop(-1)

    nomes_ferragens_ecg = {
        'KITAPARADORINOX-PINODUPLO': lista_ferragens['quant_kit_aparador'],
        'FECHOLEITO': lista_ferragens['quant_fecho_leito'],
        'MOLDURA': lista_ferragens['quant_molduras'],
        'GIRATÓRIO': lista_ferragens['quant_giratorio'],
        'MOLADOTRILHO': lista_ferragens['quant_molas'],
        'KITPAINEL': lista_ferragens['quant_kit_painel_producao'],
        'ADESIVOMOLA': lista_ferragens['quantidade_adesivos_cor'],
        'ETIQUETAVERSATEEL': lista_ferragens['quantidade_adesivos_versateel'],
        'ESTACIONAMENTO': lista_ferragens['quant_estacionamento'],
        'ETIQUETAKAIZEN': lista_ferragens['quantidade_adesivos_kaizen'],
    }
    contador = len(itens)+1
    for key, value in nomes_ferragens_ecg.items():
        escrever(navegador, By.CSS_SELECTOR, f'.custom-F{contador}id', key)
        escrever(navegador, By.ID, f'F{contador}qtd', value)
        contador += 1
