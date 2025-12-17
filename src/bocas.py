from src.calcs_vetor import obter_dados_intervalo, vetor_entre_pontos, normalizar, definir_pontos_na_secao, ponto_perpendicular_a_vetor, angulo_do_vetor
from pyautocad import Autocad, APoint
from src.comandos_cad import adicionar_texto_modelspace
from src.logs import log_spev

def verificar_se_boca_bate_na_mola(molas, boca, sentido):
    distancia_boca = boca
    for mola in molas:
        if mola-34 <= boca <= mola +34:#boca está batendo na mola
            if sentido == 'esquerda':
                distancia_boca = mola - 45
            else:
                distancia_boca = mola + 45
    return distancia_boca

def verificar_se_vidro_abre_na_boca(vidro, pivo_individual, sentido, boca, limite=0.6):
    limite_vidro = pivo_individual + vidro*limite -15 if sentido == 'esquerda' else pivo_individual - vidro*limite + 15
    if sentido == 'esquerda' and boca <= limite_vidro or sentido == 'direita' and boca >= limite_vidro:
        return False
    else:
        return True

def localizar_giratorio(quant_vidros, giratorio):
    indice_vidro_giratorio = giratorio - 1  # convertendo pra índice 0-based
    soma = 0
    for i, qtd in enumerate(quant_vidros):
        soma += qtd
        if indice_vidro_giratorio < soma:
            resultado = i
            break

    return resultado

def criar_nova_boca(meio_do_estacionamento, vidro, sentido):
    if sentido == 'esquerda':
        nova_boca = meio_do_estacionamento + (vidro - 15.0) - 15
    else:
        nova_boca = meio_do_estacionamento - (vidro - 15.0) + 15
    return nova_boca


def definir_pivos_individuais(pivo, quant_vidros_da_abertura, direcao):
    pivos_individuais = []
    pivos_individuais.append(pivo)
    contador = 1
    for vidro in range(0, quant_vidros_da_abertura-1):
        meio = pivo + 30*contador if direcao == 'esquerda' else pivo - 30*contador
        pivos_individuais.append(meio)
        contador += 1
    return pivos_individuais

def definir_molas(pivos_individuais, direcao):
    molas = []
    for vidro in pivos_individuais[:0:-3]:
        ponto_mola = vidro + 90 if direcao == 'esquerda' else vidro - 90
        molas.append(ponto_mola)
    return molas

def definir_bocas(final_do_giratorio, direcao, medida_vidros_da_abertura, pivos_individuais, molas, limite=0.6) -> tuple[list[float], list[int]]:
    bocas_lado = []
    quant_lado = []
    boca1 = final_do_giratorio - 30.0 if direcao == 'esquerda' else final_do_giratorio + 30.0
    boca1_final = verificar_se_boca_bate_na_mola(molas, boca1, direcao)
    bocas_lado.append(boca1_final)
    quant_lado.append(0)

    medida_vidros_da_abertura = reversed(medida_vidros_da_abertura) if direcao == 'direita' else medida_vidros_da_abertura

    # Definindo as outras bocas
    for i, vidro in enumerate(medida_vidros_da_abertura):
        pivo_do_vidro = pivos_individuais[i]
        ultima_boca = bocas_lado[-1]
        verificacao = verificar_se_vidro_abre_na_boca(vidro, pivo_do_vidro, direcao, ultima_boca, limite)

        if verificacao is False:
            nova_boca = criar_nova_boca(pivo_do_vidro, vidro, direcao)
            bocas_lado.append(nova_boca)
            quant_lado.append(1)
        else:
            quant_lado[-1] += 1
            continue
    return bocas_lado, quant_lado

def definir_aberturas(
        sentidos: list[int, int, int, int, tuple[int]],
        medidas_vidros: list[float],
        pontos_vidros: list[list[float]],
        pivos: list[int],
        quant_vidros: list[int],
        lcs
        ):
    medidas_bocas = []
    quant_vidro_por_boca = []
    pivos_individuais_sacada = []
    for i, sentido in enumerate(sentidos):
        vidro_ini = sentido[0]
        vidro_fim = sentido[1]
        direcao = sentido[4]
        pivo = pivos[i]

        medida_vidros_da_abertura = obter_dados_intervalo(medidas_vidros, vidro_ini, vidro_fim)
        posicao_vidros_da_abertura = obter_dados_intervalo(pontos_vidros, vidro_ini, vidro_fim)
        quant_vidros_da_abertura = vidro_fim - vidro_ini + 1
        giratorio = 0 if direcao == 'esquerda' else quant_vidros_da_abertura-1
        lcs_giratorio = localizar_giratorio(quant_vidros, sentido[2])
        final_do_giratorio = posicao_vidros_da_abertura[giratorio][1] if direcao == 'esquerda' else posicao_vidros_da_abertura[giratorio][0] - lcs[lcs_giratorio]

        pivos_individuais = definir_pivos_individuais(pivo, quant_vidros_da_abertura, direcao)
        pivos_individuais_sacada.append(pivos_individuais)
        molas = definir_molas(pivos_individuais, direcao)

        limite = 0.6
        medidas_lado, quant_vidro_lado = definir_bocas(final_do_giratorio, direcao, medida_vidros_da_abertura, pivos_individuais, molas, limite)

        while True:
            limite += 0.05
            if len(quant_vidro_lado) > 1 and quant_vidro_lado[-2] > quant_vidro_lado[-1]:
                novas_medidas, novas_quant = definir_bocas(final_do_giratorio, direcao, medida_vidros_da_abertura, pivos_individuais, molas, limite)
                if novas_quant[0] <= novas_quant[1]:
                    medidas_lado, quant_vidro_lado = novas_medidas, novas_quant
            else:
                break

        medidas_bocas.append(medidas_lado)
        quant_vidro_por_boca.append(quant_vidro_lado)

    return medidas_bocas, quant_vidro_por_boca, pivos_individuais_sacada

def desenhar_bocas(
        medidas_bocas: list[list[float]],
        quant_vidro_por_boca: list[list[int]],
        pos_lcs: list[list[float, float, float, float]],
        quant_vidros: list[int],
        sentidos_abert: list[int, int, int, int, tuple[int]]
        ):
    acad = Autocad(create_if_not_exists=True)

    try:
        for i, abertura in enumerate(sentidos_abert):
            medidas_bocas_lado = medidas_bocas[i]
            quant_vidro_por_lado = quant_vidro_por_boca[i]
            direcao = abertura[4]
            lcs_giratorio = localizar_giratorio(quant_vidros, abertura[2])
            x_ini, y_ini, x_fim, y_fim = pos_lcs[lcs_giratorio]
            p1 = (x_ini, y_ini)
            p2 = (x_fim, y_fim)
            vetor_lcs = vetor_entre_pontos(p1, p2)
            vetor_unitario = normalizar(vetor_lcs)
            onde_puxar_bocas = p1 if direcao == 'esquerda' else p2
            angulo_lcs = angulo_do_vetor(p1, p2)
            ponto_ref_medida = None
            ponto_guia = 0

            for j, boca in enumerate(medidas_bocas_lado):
                #desenhando guias das bocas
                quant_vidros_boca = quant_vidro_por_lado[j]
                coord_boca = definir_pontos_na_secao(onde_puxar_bocas, vetor_unitario, boca)
                p3 = ponto_perpendicular_a_vetor(coord_boca, p1, p2, -32)
                ponto_guia = p3 if ponto_guia == 0 else ponto_guia
                l = acad.model.AddLine(APoint(*coord_boca), APoint(*p3))
                l.Layer = 'Bocas'

                #desenhando simbolos de puxar as bocas
                vetor_guia = vetor_entre_pontos(coord_boca, p3)
                vetor_unitario_guia = normalizar(vetor_guia)

                deslocamento_perpendicular_guia = 50
                deslocamento_paralelo_guia = -50 if direcao == 'esquerda' else 50
                deslocamento_perpendicular = 50
                deslocamento_paralelo = -50 if direcao == 'esquerda' else 50

                #adicionando textos de medidas e quantidade
                if ponto_ref_medida is None:
                    ponto_l_meio = definir_pontos_na_secao(p3, vetor_unitario_guia, deslocamento_perpendicular_guia)
                    ponto_l_fim = definir_pontos_na_secao(ponto_l_meio, vetor_unitario, deslocamento_paralelo_guia)
                    ponto_ref_medida = definir_pontos_na_secao(ponto_l_fim, vetor_unitario, deslocamento_paralelo*3 if direcao == 'esquerda' else deslocamento_paralelo*0.2)
                    ponto_ref_medida = definir_pontos_na_secao(ponto_ref_medida, vetor_unitario_guia, 30)
                    ponto_ref_quantidade = definir_pontos_na_secao(ponto_ref_medida, vetor_unitario_guia, deslocamento_perpendicular*2)
                else:
                    p3 = definir_pontos_na_secao(ponto_guia, vetor_unitario, -deslocamento_paralelo_guia*(j*5))
                    ponto_guia = p3
                    ponto_l_meio = definir_pontos_na_secao(ponto_l_meio, vetor_unitario, -deslocamento_paralelo_guia*(j*5))
                    ponto_l_fim = definir_pontos_na_secao(ponto_l_fim, vetor_unitario, -deslocamento_paralelo_guia*(j*5))
                    ponto_ref_medida = definir_pontos_na_secao(ponto_ref_medida, vetor_unitario, deslocamento_paralelo*(j*-5) if direcao == 'esquerda' else deslocamento_paralelo*(j*-5))
                    ponto_ref_quantidade = definir_pontos_na_secao(ponto_ref_quantidade, vetor_unitario, deslocamento_paralelo*(j*-5) if direcao == 'esquerda' else deslocamento_paralelo*(j*-5))

                l1 = acad.model.AddLine(APoint(*p3), APoint(*ponto_l_meio))
                l1.Layer = 'Bocas guias'
                l2 = acad.model.AddLine(APoint(*ponto_l_meio), APoint(*ponto_l_fim))
                l2.Layer = 'Bocas guias'

                medida = adicionar_texto_modelspace(abs(boca), APoint(*ponto_ref_medida), 60)
                medida.Rotation = angulo_lcs
                quantidade = adicionar_texto_modelspace(f"{quant_vidros_boca:02}", APoint(*ponto_ref_quantidade), 60)
                quantidade.Rotation = angulo_lcs
    except Exception as e:
        log_spev(f"Erro ao adicionar texto de ângulo: {e}")

def desenhar_pivos_individuais(pivos_individuais, pos_lcs, quant_vidros, sentidos_abert):
    acad = Autocad(create_if_not_exists=True)
    try:
        for i, abertura in enumerate(sentidos_abert):
            pivos_individuais_lado = pivos_individuais[i]
            direcao = abertura[4]
            lcs_giratorio = localizar_giratorio(quant_vidros, abertura[2])
            x_ini, y_ini, x_fim, y_fim = pos_lcs[lcs_giratorio]
            p1 = (x_ini, y_ini)
            p2 = (x_fim, y_fim)
            vetor_lcs = vetor_entre_pontos(p1, p2)
            vetor_unitario = normalizar(vetor_lcs)
            onde_puxar_bocas = p1 if direcao == 'esquerda' else p2

            for pivo in pivos_individuais_lado:
                coord_pivo = definir_pontos_na_secao(onde_puxar_bocas, vetor_unitario, pivo)
                p3 = ponto_perpendicular_a_vetor(coord_pivo, p1, p2, -32)
                l = acad.model.AddLine(APoint(*coord_pivo), APoint(*p3))
                l.Layer = 'Pivo'
    except Exception as e:
        log_spev(f"Erro ao desenhar pivos individuais: {e}")

