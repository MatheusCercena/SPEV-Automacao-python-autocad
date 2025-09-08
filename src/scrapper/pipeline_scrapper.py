from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from src.scrapper.scrapper_ecg import *
from src.scrapper.config import senha_ecg, usuario_ecg

def abrir_navegador():
    # if headless == True:
    #     options=Options()
    #     options.add_argument('--headless')
    #     options.add_argument('--width=1920')
    #     options.add_argument('--height=1080')

    navegador = webdriver.Firefox(service=Service(), options=Options())
    navegador.maximize_window()
    return navegador

def criar_dados(navegador, ordem_de_servico):
    numero_orcamento = ordem_de_servico[:-2]

    dados_obra = pegar_dados_obra(navegador, ordem_de_servico, numero_orcamento)
    nome_cliente = pegar_nome_cliente(navegador, ordem_de_servico)

    # enderecos = []
    # endereco_cliente = pegar_endereco_cliente(navegador, ordem_de_servico)
    # endereco_extra = pegar_enderecos_extras(navegador, ordem_de_servico)
    # enderecos.append(endereco_cliente)
    # enderecos.extend(endereco_extra)

    # endereco_obra = None
    # if len(enderecos) == 1:
    #     endereco_obra = enderecos[0]
    # else:
    #     # chamar_dialogo
    #     opcoes = [f'Endereço {i+1}: {endereco["logradouro"]}, {endereco["numero"]}, {endereco["bairro"]}, {endereco["cidade"]} - {endereco["uf"]}, {endereco["cep"]}' for i, endereco in enumerate(enderecos)]
    #     print('Mais de um endereço encontrado. Escolha um:')
    #     for opcao in opcoes:
    #         print(opcao)
    #     endereco_obra = enderecos[int(input('Digite o número do endereço desejado: '))-1]

    dados = {
        'nome' : nome_cliente,
        # 'cep' : endereco_obra['cep'],
        # 'numero' : endereco_obra['numero'],
        # 'complemento' : endereco_obra['complemento'],
        # 'bairro' : endereco_obra['bairro'],
        # 'cidade' : endereco_obra['cidade'],
        # 'uf' : endereco_obra['uf'],
        'cor' : dados_obra['cor'],
        'vidro' : dados_obra['vidro'],
    }
    return dados

