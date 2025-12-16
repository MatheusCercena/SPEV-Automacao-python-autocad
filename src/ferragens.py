from math import ceil
from src.calcs_vetor import contar_entre_numeros

def calcular_molduras(medidas_bocas):
    quantidade_bocas = 0
    for bocas_vao in medidas_bocas:
        quantidade_bocas += len(bocas_vao)
    return quantidade_bocas*2

def calcular_molas(sentidos_abert):
    molas = 0
    for sentido in sentidos_abert:
        quant_vidros_abertura = contar_entre_numeros(sentido[0], sentido[1])
        quant_molas = ceil((quant_vidros_abertura - 1)/3)
        molas += quant_molas
    return molas

def calcular_kit_aparador(giratorios):
    return len(giratorios)

def calcular_estacionamento(sentidos_abert):
    estacionamentos = 0
    for sentido in sentidos_abert:
        quant_vidros = contar_entre_numeros(sentido[0], sentido[1])
        quant_corrigida = quant_vidros + (quant_vidros % 2)
        quant_estac = quant_corrigida-2
        estacionamentos += quant_estac
    return estacionamentos

def calcular_giratorio(giratorios):
    return len(giratorios)*2

def calcular_kit_painel_producao(quant_vidros, giratorios):
    return sum(quant_vidros)-len(giratorios)

def calcular_kit_painel_instalacao(giratorios):
    return len(giratorios)

def calcular_fecho_leito(giratorios):
    return len(giratorios)

def calcular_adesivos(quant_molas):
    '''ordem: versateel, kaizen, cor'''
    adesivo_versateel = 1 if quant_molas >= 1 else 0
    adesivo_kaizen = 1 if quant_molas >= 2 else 0
    adesivo_cor = quant_molas - 2 if quant_molas >= 3 else 0
    return adesivo_versateel, adesivo_kaizen, adesivo_cor

def calcular_mangueira(giratorios):
    quantidade = giratorios * 3
    comprimento = 50
    return quantidade, comprimento

def calcular_tampas_leito_45(angs_in):
    quantidade = 0
    for ang in angs_in:
        if 84 < ang/2 < 93: 
            quantidade += 2            
    return quantidade

def calcular_lista_ferragens(dados: dict) -> dict:
    quant_molduras = calcular_molduras(dados['medidas_bocas'])
    quant_molas = calcular_molas(dados['aberturas'])
    quant_kit_aparador = calcular_kit_aparador(dados['giratorios'])
    quant_estacionamento = calcular_estacionamento(dados['aberturas'])
    quant_giratorio = calcular_giratorio(dados['giratorios'])
    quant_kit_painel_producao = calcular_kit_painel_producao(dados['quantidade_vidros'], dados['giratorios'])
    quant_kit_painel_instalacao = calcular_kit_painel_instalacao(dados['giratorios'])
    quant_fecho_leito = calcular_fecho_leito(dados['giratorios'])
    quantidade_adesivos_versateel, quantidade_adesivos_kaizen, quantidade_adesivos_cor = calcular_adesivos(quant_molas)
    quantidade_tampas_leito = calcular_tampas_leito_45(dados['angulos_internos'])

    lista_ferragens = {
        'quant_molduras': quant_molduras,
        'quant_molas': quant_molas,
        'quant_kit_aparador': quant_kit_aparador,
        'quant_estacionamento': quant_estacionamento,
        'quant_giratorio': quant_giratorio,
        'quant_kit_painel_producao': quant_kit_painel_producao,
        'quant_kit_painel_instalacao': quant_kit_painel_instalacao,
        'quant_fecho_leito': quant_fecho_leito,
        'quantidade_adesivos_versateel': quantidade_adesivos_versateel,
        'quantidade_adesivos_kaizen': quantidade_adesivos_kaizen,
        'quantidade_adesivos_cor': quantidade_adesivos_cor,
        'tampa_leito_45_esq' : quantidade_tampas_leito,
        'tampa_leito_45_dir' : quantidade_tampas_leito,
    }

    return lista_ferragens

