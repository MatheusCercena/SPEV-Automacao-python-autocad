from math import ceil
from src.calcs_vetor import contar_entre_numeros

# PEGAR TODAS AS POSICOES DO PAPERSPACE
# FAZER AS FORMULAS DAS FERRAGENS - feito
# VER O QUE PRECISA PEGAR DO ECG PELO SELENIUM E DA AUTOMACAO DE TRTS


def formula_tampa_de_leito(juncoes):
    juncoes_lista = [juncao for lado in juncoes for juncao in lado]
    quantidade = 0
    for juncao in juncoes_lista:
        if juncao == 1 or juncao == 2:
            quantidade += 1
    juncoes_45 = quantidade/2
    quant_tampinhas_45 = juncoes_45*2
    return quant_tampinhas_45

def formula_molduras(medidas_bocas):
    quantidade_bocas = 0
    for bocas_vao in medidas_bocas:
        quantidade_bocas += len(bocas_vao)
    return quantidade_bocas

def formula_molas(sentidos_abert):
    molas = 0
    for sentido in sentidos_abert:
        quant_vidros_abertura = contar_entre_numeros(sentido[0], sentido[1])
        quant_molas = ceil((quant_vidros_abertura - 1)/3)
        molas += quant_molas
    return molas

def formula_tubo_aparador(sentidos_abert):
    tubos = []
    for sentido in sentidos_abert:
        quant_vidros = contar_entre_numeros(sentido[0], sentido[1])
        tamanho_aparador = 30*(quant_vidros + 2)
        if tamanho_aparador < 180:
            tamanho_aparador = 180
        tubos.append(tamanho_aparador)
    return tubos

def formula_kit_aparador(giratorios):
    return len(giratorios)

def formula_estacionamento(sentidos_abert):
    estacionamentos = 0
    for sentido in sentidos_abert:
        quant_vidros = contar_entre_numeros(sentido[0], sentido[1])
        quant_corrigida = quant_vidros + (quant_vidros % 2)
        quant_estac = quant_corrigida-2
        estacionamentos += quant_estac
    return estacionamentos

def formula_giratorio(giratorios):
    return len(giratorios)*2

def formula_kit_painel_producao(quant_vidros, giratorios):
    return sum(quant_vidros)-len(giratorios)

def formula_kit_painel_instalacao(giratorios):
    return len(giratorios)

def formula_polietileno(medidas_perfis_U):
    comprimento_sacada = int(sum([round(sum(lado), 0) for lado in medidas_perfis_U]))
    return comprimento_sacada

def formula_escovinha_7x8(medidas_perfis_U):
    comprimento_sacada = int(sum([round(sum(lado), 0) for lado in medidas_perfis_U]))
    return comprimento_sacada

def formula_escovinha_5x7(comprimento_pe3, quantidade_pe3):
    return int((comprimento_pe3 - 164) * quantidade_pe3)

def formula_fecho_leito(giratorios):
    return len(giratorios)

def calcular_adesivos(quant_molas):
    '''ordem: versateel, kaizen, cor'''
    adesivo_versateel = 1 if quant_molas >= 1 else 0
    adesivo_kaizen = 1 if quant_molas >= 2 else 0
    adesivo_cor = quant_molas - 2 if quant_molas >= 3 else 0
    return adesivo_versateel, adesivo_kaizen, adesivo_cor

def calcular_lista_ferragens(dados: dict) -> dict:
    quant_tampas_leito = formula_tampa_de_leito(dados['juncoes'])
    quant_molduras = formula_molduras(dados['medidas_bocas'])
    quant_molas = formula_molas(dados['aberturas'])
    comprimento_tubo_aparador = formula_tubo_aparador(dados['aberturas'])
    quant_kit_aparador = formula_kit_aparador(dados['giratorios'])
    quant_estacionamento = formula_estacionamento(dados['aberturas'])
    quant_giratorio = formula_giratorio(dados['giratorios'])
    quant_kit_painel_producao = formula_kit_painel_producao(dados['quantidade_vidros'], dados['giratorios'])
    quant_kit_painel_instalacao = formula_kit_painel_instalacao(dados['giratorios'])
    quant_fecho_leito = formula_fecho_leito(dados['giratorios'])
    quantidade_adesivos_versateel, quantidade_adesivos_kaizen, quantidade_adesivos_cor = calcular_adesivos(quant_molas)

    lista_ferragens = {
        'quant_tampas_leito': quant_tampas_leito,
        'quant_molduras': quant_molduras,
        'quant_molas': quant_molas,
        'comprimento_tubo_aparador': comprimento_tubo_aparador,
        'quant_kit_aparador': quant_kit_aparador,
        'quant_estacionamento': quant_estacionamento,
        'quant_giratorio': quant_giratorio,
        'quant_kit_painel_producao': quant_kit_painel_producao,
        'quant_kit_painel_instalacao': quant_kit_painel_instalacao,
        'quant_fecho_leito': quant_fecho_leito,
        'quantidade_adesivos_versateel': quantidade_adesivos_versateel,
        'quantidade_adesivos_kaizen': quantidade_adesivos_kaizen,
        'quantidade_adesivos_cor': quantidade_adesivos_cor
    }

    return lista_ferragens

def calcular_lista_perfis_rolo(dados):
    lista_vidros = [vidro for vao in dados['vidros'] for vidro in vao]
    lista_leitos = [round(medida, 0) for medida in dados['medidas_leitos']]
    lista_perfis_U = [round(medida, 0) for vao in dados['medidas_perfis_U'] for medida in vao]
    lista_pe3 = [dados['altura_pe3'] for _ in range(dados['quantidade_pe3'])]

    comprimento_polietileno = formula_polietileno(dados['medidas_perfis_U'])
    comprimento_escovinha_7x8 = formula_escovinha_7x8(dados['medidas_perfis_U'])
    comprimento_escovinha_5x7 = formula_escovinha_5x7(dados['comprimento_pe3'], dados['quantidade_pe3'])

    listagem_perfis_rolo = {
        'lista_vidros': lista_vidros,
        'lista_leitos': lista_leitos,
        'lista_perfis_U': lista_perfis_U,
        'lista_pe3': lista_pe3,
        'comprimento_polietileno': comprimento_polietileno,
        'comprimento_escovinha_7x8': comprimento_escovinha_7x8,
        'comprimento_escovinha_5x7': comprimento_escovinha_5x7,

    }

    return listagem_perfis_rolo