import pythoncom
from pyautocad import Autocad, APoint
from src.autocad_conn import get_acad
from src.calcs_vetor import normalizar, definir_pontos_na_secao, distancia_2d
from src.calcs_cad import calcular_gaps_leito, obter_pontos_medida_total
from math import radians
from sympy import symbols, Eq, solve
from time import sleep
from src.logs import log_spev

x, y, b = symbols('x y b')

def desenhar_guias_leitos(handles_lcs: list, vidros_sacada: list, posicao_dos_vidros: list, folgas_leitos: list) -> list:
    """Desenha as guias dos leitos no AutoCAD."""
    acad, acad_ModelSpace = get_acad()
    acad2 = Autocad(create_if_not_exists=True)

    handles_guias_leitos = []
    for i, linha_de_centro in enumerate(handles_lcs):

        ini_linha_de_centro = linha_de_centro.StartPoint
        fim_linha_de_centro = linha_de_centro.EndPoint

        vetor_linha = (fim_linha_de_centro[0] - ini_linha_de_centro[0], fim_linha_de_centro[1] - ini_linha_de_centro[1])
        vetores_unitarios = normalizar(vetor_linha)

        for index in range(0, len(vidros_sacada[i])):
            comeco_vidro = posicao_dos_vidros[i][index][0]
            fim_vidro = posicao_dos_vidros[i][index][1]
            inicio = definir_pontos_na_secao(ini_linha_de_centro, vetores_unitarios, comeco_vidro + folgas_leitos[i][index][0])
            fim = definir_pontos_na_secao(ini_linha_de_centro, vetores_unitarios, fim_vidro - folgas_leitos[i][index][1])
            guia = acad2.model.AddLine(APoint(inicio[0], inicio[1]), APoint(fim[0], fim[1]))
            handles_guias_leitos.append(acad.HandleToObject(guia.Handle))
    return handles_guias_leitos

def folgas_leitos(vidros: list, folgas_vidros: list, angs_in: list[float], aberturas: list) -> list:
    """Calcula as folgas dos leitos para cada vidro em cada seção da sacada.

    Args:
        vidros: Lista de listas, cada sublista representa os vidros de uma seção.
        folgas_vidros: Mesma estrutura que vidros, mas com folgas esquerda/direita.
        angs_in: Lista com ângulos de entrada das seções.
        aberturas: Lista com informações das aberturas.

    Returns:
        list: Lista com as folgas dos leitos por seção e vidro.
    """
    folgas_leitos_sacada = []
    for secao in range(len(vidros)):
        folgas_leitos_secao = []
        for index in range(len(vidros[secao])):
            folgas_leitos_vidro = []
            for lado in range(2):
                if lado == 0:
                    if index == 0:
                        if folgas_vidros[secao][0] == 2:
                            folga_esq = calcular_gaps_leito(angs_in[secao-1]) + 3
                        elif folgas_vidros[secao][0] == -7:
                            folga_esq = calcular_gaps_leito(angs_in[secao-1]) - 7
                        elif folgas_vidros[secao][0] == -1:
                            if abs(angs_in[secao-1])/2 < 20:
                                folga_esq = 1.5
                            else:
                                folga_esq = 0
                        else:
                            folga_esq = 1.5
                    else:
                        folga_esq = 1.5
                    # if aberturas[2]
                    folgas_leitos_vidro.append(folga_esq)
                if lado == 1:
                    if index+1 == len(vidros[secao]):
                        if folgas_vidros[secao][1] == 2:
                            folga_dir = calcular_gaps_leito(angs_in[secao]) + 3
                        elif folgas_vidros[secao][1] == -7:
                            folga_dir = calcular_gaps_leito(angs_in[secao]) - 7
                        elif folgas_vidros[secao][1] == -1:
                            if abs(angs_in[secao-1])/2 < 20:
                                folga_dir = 1.5
                            else:
                                folga_dir = 0
                        else:
                            folga_dir = 1.5
                    else:
                        folga_dir = 1.5

                    folgas_leitos_vidro.append(folga_dir)
            folgas_leitos_secao.append(folgas_leitos_vidro)
        folgas_leitos_sacada.append(folgas_leitos_secao)
    return folgas_leitos_sacada

def converter_ordem_para_secoes(vidros: list, lista: list) -> list:
    """Converte uma lista ordenada para estrutura de seções.

    Args:
        vidros: Lista com estrutura de vidros por seção.
        lista: Lista ordenada a ser convertida.

    Returns:
        list: Lista convertida para estrutura de seções.
    """
    lista_nova = []
    cont = 0
    for secao in vidros:
        lista_secao = []
        for vidro in secao:
            lista_secao.append(lista[cont])
            cont += 1
        lista_nova.append(lista_secao)
    return lista_nova

def def_eq_reta_leitos(ponto_a: tuple[float, float], ponto_b: tuple[float, float]) -> Eq:
    """Define a equação da reta entre dois pontos para leitos.

    Define a equação da reta a ser usada para verificar se a seção intercepta a linha perpendicular.

    Args:
        ponto_a: Primeiro ponto (x, y).
        ponto_b: Segundo ponto (x, y).

    Returns:
        Eq: Equação da reta entre os pontos.
    """
    x1 = ponto_a[0]
    x2 = ponto_b[0]

    if x2 == x1:
        return Eq(x, x1)
    else:
        valor_m = (ponto_b[1] - ponto_a[1]) / (ponto_b[0] - ponto_a[0])
        y_f = ponto_b[1]
        x_f = ponto_b[0]
        eq_b = Eq(y_f, valor_m*x_f + b)
        valor_b = solve(eq_b, b)[0]

        return Eq(y, valor_m*x + valor_b)

def desenhar_leitos(handles_guias: list, vidros: list, angs: list[float], giratorios: list[int], adjacentes: list[int], sentidos: list[str]) -> tuple[dict[str, list[str]], list[tuple[float, float, float]]]:
    """Desenha os leitos no AutoCAD com todas as suas características.

    Args:
        handles_guias: Lista de handles das guias dos leitos.
        vidros: Lista com os vidros por seção.
        angs: Lista com ângulos das seções.
        giratorios: Lista com índices dos vidros giratórios.
        adjacentes: Lista com índices dos vidros adjacentes aos giratórios.
        sentidos: Lista com sentidos de abertura ('direita' ou 'esquerda').

    Returns:
        tuple: Tupla contendo:
            - Dicionário com handles dos leitos organizados por tipo
            - Lista com coordenadas dos leitos
    """
    acad2 = Autocad(create_if_not_exists=True)
    acad, acad_ModelSpace = get_acad()

    handles_leitos = {'externos': [], 'internos': [], 'lat_esq': [], 'lat_dir': []}
    coordenadas_leitos = []
    handles_guias = converter_ordem_para_secoes(vidros, handles_guias)
    medidas_leitos = []

    pos_vidro = 1
    pos_sentido = 0

    for index, secao in enumerate(handles_guias):
        for i, linha_guia in enumerate(secao):
            #Offsets
            for tentativa in range(5):
                try:
                    pythoncom.PumpWaitingMessages()
                    ext = linha_guia.Offset(14)[0]
                    handles_leitos['externos'].append(ext.Handle)
                    ext.Layer = 'Leito Externo'
                    break
                except Exception as e:
                    sleep(0.5)
                    log_spev(f'Tentativa {tentativa+1} de 5 falhou ao tentar offset nos leitos com erro: {e}')

            for tentativa in range(5):
                try:
                    pythoncom.PumpWaitingMessages()
                    int = linha_guia.Offset(-14)[0]
                    handles_leitos['internos'].append(int.Handle)
                    int.Layer = 'Leito Interno'
                    break
                except Exception as e:
                    sleep(0.5)
                    log_spev(f'Tentativa {tentativa+1} de 5 falhou ao tentar dar offset nos leitos com erro: {e}')

            #Guias
            guia_ext = linha_guia.Offset(4)[0]
            guia_int = linha_guia.Offset(-4)[0]
            coord_guia_interna_x = guia_int.StartPoint
            coord_guia_interna_y = guia_int.EndPoint
            coord_guia_externa_x = guia_ext.StartPoint
            coord_guia_externa_y = guia_ext.EndPoint

            #Laterais
            ext_ini = ext.StartPoint
            ext_fim = ext.EndPoint
            int_ini = int.StartPoint
            int_fim = int.EndPoint

            lat_esq = acad2.model.AddLine(APoint(ext_ini[0], ext_ini[1]), APoint(int_ini[0], int_ini[1]))
            lat_esq.Layer = 'Leito Interno'
            handles_leitos['lat_esq'].append(lat_esq.Handle)
            coord_lat_esq_x = lat_esq.StartPoint
            coord_lat_esq_y = lat_esq.EndPoint

            lat_dir = acad2.model.AddLine(APoint(ext_fim[0], ext_fim[1]), APoint(int_fim[0], int_fim[1]))
            lat_dir.Layer = 'Leito Interno'
            handles_leitos['lat_dir'].append(lat_dir.Handle)
            coord_lat_dir_x = lat_dir.StartPoint
            coord_lat_dir_y = lat_dir.EndPoint

            #Intersecoes para rotacao
            interseccao_esq_inf = solve((def_eq_reta_leitos(coord_guia_interna_x, coord_guia_interna_y), def_eq_reta_leitos(coord_lat_esq_x, coord_lat_esq_y)), (x, y))
            interseccao_dir_inf  = solve((def_eq_reta_leitos(coord_guia_interna_x, coord_guia_interna_y), def_eq_reta_leitos(coord_lat_dir_x, coord_lat_dir_y)), (x, y))
            interseccao_esq_sup  = solve((def_eq_reta_leitos(coord_guia_externa_x, coord_guia_externa_y), def_eq_reta_leitos(coord_lat_esq_x, coord_lat_esq_y)), (x, y))
            interseccao_dir_sup = solve((def_eq_reta_leitos(coord_guia_externa_x, coord_guia_externa_y), def_eq_reta_leitos(coord_lat_dir_x, coord_lat_dir_y)), (x, y))
            try:
            # rotacoes lado esquerdo
                if index != 0:
                    if i == 0 and not (70 < abs(angs[index-1]) < 110):
                        if angs[index-1] < 0:
                            lat_esq.Rotate(APoint(float(interseccao_esq_inf[x]), float(interseccao_esq_inf[y])), radians((angs[index-1])/2)*-1)
                        elif angs[index-1] > 0:
                            lat_esq.Rotate(APoint(float(interseccao_esq_sup[x]), float(interseccao_esq_sup[y])), radians((angs[index-1])/2))

                # rotacoes lado direito
                if index != len(handles_guias)-1:
                    if i == len(secao)-1 and angs[index] > 0 and not (70 < abs(angs[index]) < 110):
                        lat_dir.Rotate(APoint(float(interseccao_dir_sup[x]), float(interseccao_dir_sup[y])), radians((angs[index])/2)*-1)
                    elif i == len(secao)-1 and angs[index] < 0 and not (70 < abs(angs[index]) < 110):
                        lat_dir.Rotate(APoint(float(interseccao_dir_inf[x]), float(interseccao_dir_inf[y])), radians((angs[index])/2))

                # rotacoes giratorios
                if pos_vidro in giratorios:
                    if sentidos[pos_sentido] == 'direita' and i != 0:
                        lat_esq.Rotate(APoint(float(interseccao_esq_sup[x]), float(interseccao_esq_sup[y])), radians(-5))
                    elif sentidos[pos_sentido] == 'esquerda' and i != len(secao)-1:
                        lat_dir.Rotate(APoint(float(interseccao_dir_sup[x]), float(interseccao_dir_sup[y])), radians(5))
                    if pos_vidro-1 in adjacentes:
                        pos_sentido += 1

                # rotacoes vidros adjacentes aos giratorios
                if pos_vidro in adjacentes:
                    if sentidos[pos_sentido] == 'direita' and i != len(secao)-1:
                        lat_dir.Rotate(APoint(float(interseccao_dir_inf[x]), float(interseccao_dir_inf[y])), radians(-5))
                    elif sentidos[pos_sentido] == 'esquerda' and i != 0:
                        lat_esq.Rotate(APoint(float(interseccao_esq_inf[x]), float(interseccao_esq_inf[y])), radians(5))
                    if pos_vidro-1 in giratorios:
                        pos_sentido += 1
            except Exception as e:
                sleep(0.5)
                log_spev(f'Tentativa {tentativa+1} de 5 falhou ao tentar rotacionar os leitos com erro: {e}')

            for tentativa in range(5):
                try:
                    pythoncom.PumpWaitingMessages()
                    acad.SendCommand(f'(c:custom_fillet "{handles_leitos['externos'][pos_vidro-1]}" "{handles_leitos['lat_esq'][pos_vidro-1]}")\n')
                    pythoncom.PumpWaitingMessages()
                    acad.SendCommand(f'(c:custom_fillet "{handles_leitos['lat_esq'][pos_vidro-1]}" "{handles_leitos['internos'][pos_vidro-1]}")\n')
                    pythoncom.PumpWaitingMessages()
                    acad.SendCommand(f'(c:custom_fillet "{handles_leitos['internos'][pos_vidro-1]}" "{handles_leitos['lat_dir'][pos_vidro-1]}")\n')
                    pythoncom.PumpWaitingMessages()
                    acad.SendCommand(f'(c:custom_fillet "{handles_leitos['lat_dir'][pos_vidro-1]}" "{handles_leitos['externos'][pos_vidro-1]}")\n')
                    break
                except Exception as e:
                    sleep(0.5)
                    log_spev(f'Tentativa {tentativa+1} de 5 falhou ao tentar dar fillet nos leitos com erro: {e}')
            for tentativa in range(5):
                try:
                    pythoncom.PumpWaitingMessages()
                    ext_ini, ext_fim, int_ini, int_fim = ext.StartPoint, ext.EndPoint, int.StartPoint, int.EndPoint
                    coordenadas_leitos.append([ext_ini, ext_fim, int_ini, int_fim])
                    break
                except Exception as e:
                    sleep(0.5)
                    log_spev(f'Tentativa {tentativa+1} de 5 falhou ao tentar dar fillet nos leitos com erro: {e}')
            pos_vidro += 1
            _, p1, p2 = obter_pontos_medida_total([ext_ini, ext_fim, int_ini, int_fim])
            distancia = distancia_2d(p1, p2)
            medidas_leitos.append(distancia)
    return handles_leitos, coordenadas_leitos, medidas_leitos
