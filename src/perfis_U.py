from copy import deepcopy
from src.autocad_conn import get_acad
from src.calcs_vetor import distancia_2d, normalizar, definir_pontos_na_secao, vetor_entre_pontos
from src.calcs_cad import obter_pontos_medida_total
import pythoncom
from time import sleep
from src.logs import log_spev

def offset_perfis_U(handles_lcs: list) -> dict[str, list[str]]:
    offset_ext = 20
    offset_int = 32

    handles = {'externos': [], 'internos': []}
    for linha in handles_lcs:
        for tentativa in range(5):
            try:
                pythoncom.PumpWaitingMessages()
                linha_ext = linha.Offset(offset_ext)#.Offset retorna uma tupla
                linha_ext[0].Layer = 'Perfil U Externo'
                handles['externos'].append(linha_ext[0].Handle)

                linha_int = linha.Offset(-offset_int)
                linha_int[0].Layer = 'Perfil U Interno'
                handles['internos'].append(linha_int[0].Handle)
                break
            except Exception as e:
                sleep(0.5)
                log_spev(f'Tentativa {tentativa+1} de 5 falhou ao tentar offset nos perfis U com erro: {e}')
    return handles

def fillet_perfis_U(handles: dict[str, list[str]]) -> None:
    acad, acad_ModelSpace = get_acad()

    linhas_externas = deepcopy(handles['externos'])
    linhas_internas = deepcopy(handles['internos'])

    for index in range(0, len(linhas_externas)-1):
        for tentativa in range(5):
            try:
                pythoncom.PumpWaitingMessages()
                acad.SendCommand(f'(c:custom_fillet "{linhas_externas[index]}" "{linhas_externas[index+1]}")\n')
                acad.SendCommand(f'(c:custom_fillet "{linhas_internas[index]}" "{linhas_internas[index+1]}")\n')
                break
            except Exception as e:
                sleep(0.5)
                log_spev(f'Tentativa {tentativa+1} de 5 falhou ao tentar offset nos perfis U com erro: {e}')

def definir_coord_perfis_U(handles: dict[str, list[str]]) -> list[list[tuple[float, float, float]]]:
    acad, acad_ModelSpace = get_acad()

    linhas_externas = deepcopy(handles['externos'])
    linhas_internas = deepcopy(handles['internos'])
    coordenadas = []

    for linha in range(len(linhas_externas)):
        coord = []
        for tentativa in range(5):
            try:
                pythoncom.PumpWaitingMessages()
                linha_ext = acad.HandleToObject(linhas_externas[linha])
                coord.append(linha_ext.StartPoint)
                coord.append(linha_ext.EndPoint)

                linha_int = acad.HandleToObject(linhas_internas[linha])
                coord.append(linha_int.StartPoint)
                coord.append(linha_int.EndPoint)
                break
            except Exception as e:
                sleep(0.5)
                log_spev(f'Tentativa {tentativa+1} de 5 falhou ao tentar offset nos perfis U com erro: {e}')
        coordenadas.append(coord)
    return coordenadas

def distribuir_perfis_U_por_lado(medidas: list[list[tuple[float, float, float]]], coord_perfis_U: list[tuple[float, float, float]]) -> list[list[tuple[float, float, float]]]:
    """Distribui os vidros por lado da sacada.

    Example:
        Entrada: [3, 5, 2]
        Saída: [[1, 2, 3], [4, 5, 6, 7, 8], [9, 10]]
    """

    quant_secoes = []
    for lado in medidas:
        quant_secoes.append(len(lado))

    coordenadas = []
    cont = 0
    for qtd in quant_secoes:
        coord_lado = [coord_perfis_U[c] for c in range(cont, cont + qtd)]
        coordenadas.append(coord_lado)
        cont += qtd
    return coordenadas

def redefinir_coord_perfis_U(coord_perfis_U: list[list[tuple[float, float, float]]], aberturas_por_lado: list, elevador: int) -> tuple[list[list[float]], list[list[tuple[float, float, float]]]]:
    """Redefine as coordenadas dos perfis U considerando aberturas e elevador.

    Returns:
        tuple:
            - Lista de listas com medidas dos perfis por seção
            - Lista com coordenadas dos perfis redefinidos
    """
    medidas = []
    coordenadas = []
    for i, lado in enumerate(coord_perfis_U):
        pontos = obter_pontos_medida_total(lado)
        p1 = pontos[1]
        p2 = pontos[2]

        comprimento_perfil = distancia_2d(p1, p2)
        comprimento_restante = comprimento_perfil

        perfis_secao = []
        while True:
            if elevador < comprimento_restante > 2800:
                secao_nova = 1980
                perfis_secao.append(secao_nova)
                comprimento_restante -= secao_nova
            elif elevador < comprimento_restante <= 2800:
                secao_nova = comprimento_restante/2
                perfis_secao.append(secao_nova)
                comprimento_restante -= secao_nova
            else:#comprimento_restante < elevador
                if aberturas_por_lado[i] == 'esquerda':
                    if comprimento_restante > 1980:
                        perfis_secao.append(comprimento_restante)
                    else:
                        perfis_secao.insert(0, comprimento_restante)
                elif aberturas_por_lado[i] == 'direita':
                    if comprimento_restante > 1980:
                        perfis_secao.insert(0, comprimento_restante)
                    else:
                        perfis_secao.append(comprimento_restante)
                else:
                    perfis_secao.insert(0, comprimento_restante)
                    #mais tarde fazer funcao pra levar em conta o angulo da sacada.
                break
        medidas.append(perfis_secao)
        vetor = vetor_entre_pontos(p1, p2)
        vetor_unitario = normalizar(vetor)
        ini_perfil = p1
        distancia = 0
        for perfil in perfis_secao:
            distancia += perfil
            coord_perfil = []
            coord_perfil.append(tuple(ini_perfil))

            fim_perfil = definir_pontos_na_secao(p1, vetor_unitario, distancia)
            coord_perfil.append(tuple(fim_perfil))

            ini_perfil = fim_perfil
            coordenadas.append(coord_perfil)
    return medidas, coordenadas
