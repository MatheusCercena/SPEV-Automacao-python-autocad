from src.calcs_vetor import contar_entre_numeros

def formula_polietileno(medidas_perfis_U):
    comprimento_sacada = int(sum([round(sum(lado), 0) for lado in medidas_perfis_U]))
    return {'POLIETILENO-UHMW': [2, comprimento_sacada]}

def formula_escovinha_7x8(medidas_perfis_U):
    comprimento_sacada = int(sum([round(sum(lado), 0) for lado in medidas_perfis_U]))
    return {'ESCOVINHA6.5X6.5': [2, comprimento_sacada]}

def formula_escovinha_5x8(quantidade_pe3, comprimento_pe3):
    return {'ESCOVINHA5X8CINZA': [quantidade_pe3, int((comprimento_pe3 - 164))]}

def formula_vep(quantidade_vidros, altura_vidros):
    return {'VEP': [sum(quantidade_vidros), altura_vidros+40]}

def formula_tubo_aparador(sentidos_abert):
    tubos = []
    for sentido in sentidos_abert:
        quant_vidros = contar_entre_numeros(sentido[0], sentido[1])
        tamanho_aparador = 30*(quant_vidros + 2)
        if tamanho_aparador < 180:
            tamanho_aparador = 180
        tubos.append(tamanho_aparador)
    return [{'TUBOAPARADOR': [1, tubo]} for tubo in tubos]

def formula_leito(medidas_leitos):
    return [{'PE-008': [2, medida_leito]} for medida_leito in medidas_leitos]

def formula_perfil_U_inf(medidas_perfis_U):
    medidas_finais = [round(medida) for lado in medidas_perfis_U for medida in lado]
    for i, medida_U_inf in enumerate(medidas_finais):
        if i == 0 and i == len(medidas_finais)-1:
            medidas_finais.append(medida_U_inf)
        elif i == 0:
            medidas_finais[0] = medida_U_inf
        elif i == len(medidas_finais)-1:
            medidas_finais[-1] = medida_U_inf
    return [{'PE-1': [1, medida_U_inf]} for medida_U_inf in medidas_finais]

def formula_perfil_U_sup(medidas_perfis_U, prumos):
    medidas_finais = [round(medida) for lado in medidas_perfis_U for medida in lado]
    for i, medida_U_sup in enumerate(medidas_finais):
        if i == 0 and i == len(medidas_finais)-1:
            medidas_finais[0] = medida_U_sup + prumos[0] + prumos[1]
        elif i == 0:
            medidas_finais[0] = medida_U_sup + prumos[0]
        elif i == len(medidas_finais)-1:
            medidas_finais[-1] = medida_U_sup + prumos[1]
    return [{'CEG-235': [1, medida_U_sup]} for medida_U_sup in medidas_finais]

def formula_trilho(medidas_perfis_U, prumos):
    medidas_finais = [round(medida) for lado in medidas_perfis_U for medida in lado]
    # for i, medida_U_inf in enumerate(medidas_finais):
    #     if i == 0 and i == len(medidas_finais)-1:
    #         medidas_finais[0] = medida_U_inf + prumos[0] + prumos[1]
    #     elif i == 0:
    #         medidas_finais[0] = medida_U_inf + prumos[0]
    #     elif i == len(medidas_finais)-1:
    #         medidas_finais[-1] = medida_U_inf + prumos[1]

    lista_trilhos = []
    for i, medida_trilho in enumerate(medidas_finais):
        if i == 0 and i == len(medidas_finais)-1:
            lista_trilhos.append({'PE-007' : [1, medida_trilho]})
            lista_trilhos.append({'PE-007' : [1, medida_trilho+prumos[0] + prumos[1]]})
        elif i == 0:
            lista_trilhos.append({'PE-007' : [1, medida_trilho]})
            lista_trilhos.append({'PE-007' : [1, medida_trilho + prumos[0]]})
        elif i == len(medidas_finais)-1:
            lista_trilhos.append({'PE-007' : [1, medida_trilho]})
            lista_trilhos.append({'PE-007' : [1, medida_trilho + prumos[1]]})
        else:
            lista_trilhos.append({'PE-007' : [2, medida_trilho]})
    return lista_trilhos

def formula_capa(medidas_perfis_U, prumos):
    medidas_finais = [int(medida) for lado in medidas_perfis_U for medida in lado]
    # for i, medida_U_inf in enumerate(medidas_finais):
    #     if i == 0 and i == len(medidas_finais)-1:
    #         medidas_finais.append(medida_U_inf) + prumos[0] + prumos[1]
    #     elif i == 0:
    #         medidas_finais[0] = medida_U_inf+prumos[0]
    #     elif i == len(medidas_finais)-1:
    #         medidas_finais[-1] = medida_U_inf+prumos[1]

    lista_capas = []
    for i, medida_capa in enumerate(medidas_finais):
        if i == 0 and i == len(medidas_finais)-1:
            lista_capas.append({'SAC-0005' : [1, medida_capa]})
            lista_capas.append({'SAC-0005' : [1, medida_capa+prumos[0] + prumos[1]]})
        elif i == 0:
            lista_capas.append({'SAC-0005' : [1, medida_capa]})
            lista_capas.append({'SAC-0005' : [1, medida_capa + prumos[0]]})
        elif i == len(medidas_finais)-1:
            lista_capas.append({'SAC-0005' : [1, medida_capa]})
            lista_capas.append({'SAC-0005' : [1, medida_capa + prumos[1]]})
        else:
            lista_capas.append({'SAC-0005' : [2, medida_capa]})
    return lista_capas

def formula_cantoneira_com_escova(giratorios : list[int], quant_vidros : list, altura_vidros : int) -> dict[
    str, list[int]]:
    quant_cantoneira = 0
    comprimento_cantoneiras = altura_vidros + 33 + 98

    if giratorios[0] == 1:
        quant_cantoneira += 1
    else:
        quant_cantoneira += 2

    if giratorios[-1] == sum(quant_vidros):
        quant_cantoneira += 1
    else:
        quant_cantoneira += 2

    return {'PE-3': [quant_cantoneira, comprimento_cantoneiras]}


def calcular_lista_perfis_rolo(dados: dict, prumos: list[int, int]) -> list[dict]:
    polietileno = formula_polietileno(dados['medidas_perfis_U'])
    escovinha_7x8 = formula_escovinha_7x8(dados['medidas_perfis_U'])
    veps = formula_vep(dados['quantidade_vidros'], dados['altura_vidros'])
    cantoneiras_com_escova = formula_cantoneira_com_escova(dados['giratorios'], dados['quantidade_vidros'], dados['altura_vidros'])
    escovinha_5x8 = formula_escovinha_5x8(cantoneiras_com_escova['PE-3'][0], cantoneiras_com_escova['PE-3'][1])

    lista_tubo_aparador = formula_tubo_aparador(dados['aberturas'])
    lista_leitos = formula_leito([int(medida) for medida in dados['medidas_leitos']])
    lista_perfis_u_inf = formula_perfil_U_inf(dados['medidas_perfis_U'])
    lista_perfis_u_sup = formula_perfil_U_sup(dados['medidas_perfis_U'], prumos)
    lista_trilhos = formula_trilho(dados['medidas_perfis_U'], prumos)
    lista_capas = formula_capa(dados['medidas_perfis_U'], prumos)
    lista_perfis_final = {}

    # Perfis únicos (dicionários)
    for perfil_dict in [polietileno, escovinha_7x8, escovinha_5x8, veps, cantoneiras_com_escova]:
        for k, v in perfil_dict.items():
            lista_perfis_final.setdefault(k, v)

    # Perfis múltiplos (listas de dicionários)
    for perfil_lista in [lista_tubo_aparador, lista_leitos, lista_perfis_u_inf, lista_perfis_u_sup, lista_trilhos, lista_capas]:
        for perfil_dict in perfil_lista:
            for k, v in perfil_dict.items():
                lista_perfis_final.setdefault(k, []).append(v)

    # print(lista_perfis_final)
    #falta pe-3
    return lista_perfis_final