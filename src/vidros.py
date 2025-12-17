"""
Módulo para desenho, cálculo e manipulação de vidros no AutoCAD.

Inclui funções para desenhar guias, calcular folgas, medidas e posicionamento dos vidros, além de interagir com o AutoCAD para criar entidades relacionadas aos vidros.
"""


import pythoncom
from pyautocad import Autocad, APoint
from src.autocad_conn import get_acad
from src.calcs_vetor import normalizar, definir_pontos_na_secao
from src.calcs_cad import calcular_gaps_vidro
from copy import deepcopy
from math import floor
from time import sleep

def desenhar_guias_vidros(handles_lcs: list, vidros_sacada: list, posicao_dos_vidros: list) -> None:
    acad2 = Autocad(create_if_not_exists=True)

    for i, linha_de_centro in enumerate(handles_lcs):
        for _ in range(5):
            try:
                pythoncom.PumpWaitingMessages()
                ini_linha_de_centro = linha_de_centro.StartPoint
                fim_linha_de_centro = linha_de_centro.EndPoint
                break
            except:
                sleep(0.5)
        vetor_linha = (fim_linha_de_centro[0] - ini_linha_de_centro[0], fim_linha_de_centro[1] - ini_linha_de_centro[1])
        vetores_unitarios = normalizar(vetor_linha)

        for index in range(0, len(vidros_sacada[i])):
            comeco_vidro = posicao_dos_vidros[i][index][0]
            fim_vidro = posicao_dos_vidros[i][index][1]
            inicio = definir_pontos_na_secao(ini_linha_de_centro, vetores_unitarios, comeco_vidro)
            fim = definir_pontos_na_secao(ini_linha_de_centro, vetores_unitarios, fim_vidro)
            acad2.model.AddLine(APoint(inicio[0], inicio[1]), APoint(fim[0], fim[1]))

def definir_folgas_vidros(juncoes: list, gaps_lcs: list, angs_in: list, espessura_vidro: int) -> list[list[int, int]]:
    """Define as folgas dos vidros para cada seção da sacada.

    Returns:
        list: Lista com as folgas de cada seção da sacada, onde cada elemento é uma lista com 4 elementos:
            - Folga parede esquerdo
            - Folga parede direito
            - Folga ajuste de ângulo esquerdo
            - Folga ajuste de ângulo direito
    """
    folga_parede = -12
    folga_passante = 2
    folga_colante = -3-espessura_vidro/2
    folga_vidro_vidro = -1
    juncoes_secoes = deepcopy(juncoes)
    folgas_secoes = []
    for index, secao in enumerate(juncoes_secoes):
        folgas_secao = []
        for lado in range(0, 2):
            if secao[lado] == 0:
                folgas_secao.append(folga_parede)
            elif secao[lado] == 1:
                folgas_secao.append(folga_passante)
            elif secao[lado] == 2:
                folgas_secao.append(folga_colante)
            else:
                folgas_secao.append(folga_vidro_vidro)
        for lado in range(0, 2):
            if secao[lado] == 0 and lado == 0: #parede esq
                folgas_secao.append(gaps_lcs[0])
            elif secao[lado] == 0 and lado == 1: #parede dir
                folgas_secao.append(gaps_lcs[1])
            elif secao[lado] == 1 or secao[lado] == 2:
                folgas_secao.append(0)
            elif secao[lado] == 3 and lado == 0:
                folgas_secao.append(calcular_gaps_vidro(angs_in[index-1], espessura_vidro))
            elif secao[lado] == 3 and lado == 1:
                folgas_secao.append(calcular_gaps_vidro(angs_in[index], espessura_vidro))
        folgas_secoes.append(folgas_secao)
    return folgas_secoes

def medida_dos_vidros(lcs: list, quant_vidros: list, folgas: list) -> list[int]:
    """Calcula as medidas dos vidros individuais.

    Returns:
        list: Lista com as medidas dos vidros por seção.
    """
    folga_vep = float(3)
    vidros_totais = []

    for i, linha_de_centro in enumerate(lcs):
        folga_esq = folgas[i][0]
        folga_dir = folgas[i][1]
        folga_ajuste_angulo_esq = folgas[i][2]
        folga_ajuste_angulo_dir = folgas[i][3]
        vidros_secao = []

        medida_com_vidro = linha_de_centro + folga_esq + folga_dir - folga_ajuste_angulo_esq - folga_ajuste_angulo_dir
        medida_com_vidro -= folga_vep*(quant_vidros[i]-1)
        vidros_individuais = floor(medida_com_vidro/quant_vidros[i])
        if quant_vidros[i] > 1:
            medida_ultimo_vidro = int(round((medida_com_vidro - (vidros_individuais*(quant_vidros[i]-1))), 0))
            for vidro in range(quant_vidros[i]-1):
                vidros_secao.append(vidros_individuais)
            vidros_secao.append(medida_ultimo_vidro)
        else:
            vidros_secao.append(vidros_individuais)
        vidros_totais.append(vidros_secao)

    return vidros_totais

def pontos_dos_vidros(medidas_vidros: list[int], folgas: list[list[int, int]]) -> list[list[float, float]]:
    """Calcula os pontos de posicionamento dos vidros tendo como referencia o inicio da linha de centro.

    Returns:
        list: Lista com os pontos de posicionamento dos vidros.
    """
    folga_vep = float(3)
    todos_pontos = []
    for i, linha_de_centro in enumerate(medidas_vidros):
        pos_acumulada = 0
        pontos_linha_de_centro = []
        for index, vidro in enumerate(linha_de_centro):
            pontos = []
            if index == 0:
                pos_inicial = folgas[i][0]*-1 + folgas[i][2] #aqui pode ser necessario nao multiplicar por -1 um dos fatores
            if index > 0:
                pos_inicial = pos_acumulada
            pos_final = pos_inicial + vidro
            pos_acumulada = pos_final + folga_vep
            pontos.append(pos_inicial)
            pontos.append(pos_final)
            pontos_linha_de_centro.append(pontos)
        todos_pontos.append(pontos_linha_de_centro)
    return todos_pontos

def offset_vidros(espessura_vidro: int) -> tuple[list[str], list[tuple[float, float, float]]]:
    acad, acad_ModelSpace = get_acad()
    acad2 = Autocad(create_if_not_exists=True)

    handles_vidros = []
    coord_vidros = []
    for linha in acad_ModelSpace:
        if linha.EntityName == 'AcDbLine' and linha.Layer == '0':
            ext = linha.Offset(espessura_vidro/2)[0]
            handles_vidros.append(ext.Handle)
            ext.Layer = 'Vidro Externo'
            int = linha.Offset(-1*espessura_vidro/2)[0]
            ext_ini = ext.StartPoint
            int_ini = int.StartPoint
            lat_esq = acad2.model.AddLine(APoint(ext_ini[0], ext_ini[1]), APoint(int_ini[0], int_ini[1]))
            ext_fim = ext.EndPoint
            int_fim = int.EndPoint
            coord_vidros.append([ext_ini, ext_fim])
            lat_dir = acad2.model.AddLine(APoint(ext_fim[0], ext_fim[1]), APoint(int_fim[0], int_fim[1]))
            int.Layer = lat_esq.Layer = lat_dir.Layer = 'Vidro Interno'

    return handles_vidros, coord_vidros

def achar_posicao_vidro(quant_vidros: list[int]) -> dict[int, tuple[int, int]]:
    """Mapeia o número absoluto do vidro para (lado, índice local)."""
    mapa = {}
    contador = 1
    for lado, qtd in enumerate(quant_vidros):
        for i in range(qtd):
            mapa[contador] = (lado, i)
            contador += 1
    return mapa

