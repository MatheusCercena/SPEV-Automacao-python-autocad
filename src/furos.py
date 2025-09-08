"""
Módulo responsável por definir pontos de furação nos perfis U com base nas medidas dos perfis e posições dos vidros.

Este módulo interage com o AutoCAD para criar offsets nos perfis U conforme a necessidade do projeto.
"""
from src.autocad_conn import get_acad
from src.calcs_vetor import linha_paralela_com_offset, deslocar_pontos_direcao, normalizar_coordenadas, esta_entre
from src.aberturas import distribuir_vidros_por_lado
from src.calcs_cad import calcular_gaps_furos, calcular_gaps_vidro
from src.perfis_U import distribuir_perfis_U_por_lado


def definir_pontos_furos(coord_vidros: list[list[tuple[float, float, float]]], folgas_vidros: list[list[int, int]], quant_vidros: list[list[int]], angs_in: list[float], angs_paredes: list[float], espessura_v: int) -> list[list[tuple[float, float, float]]]:
    """Define os pontos para furação dos perfis U.

    Args:
        coord_vidros: Lista contendo as coordenadas dos vidros por lado.
        folgas_vidros: Lista contendo as folgas dos vidros por lado.
        quant_vidros: Lista contendo a quantidade de vidros por lado.
        angs_in: Lista contendo os ângulos internos.
        angs_paredes: Lista contendo os ângulos das paredes.
        espessura_v: Espessura do vidro em milímetros.

    Returns:
        list: Lista de listas contendo as coordenadas dos pontos de furação por lado.
    """
    acad, acad_ModelSpace = get_acad()

    folga_parede = -12
    folga_passante = 2
    folga_colante = -3-espessura_v/2
    folga_vidro_vidro = -1
    offset = 700-espessura_v/2

    quant_furos_por_lado = []
    coordenadas = []
    distribuicao = distribuir_vidros_por_lado(quant_vidros)

    coord_vidros_reorganizada = []
    for lado in distribuicao:
        vidros_lado = []
        for vidro in lado:
            vidros_lado.append(coord_vidros[vidro - 1])
        coord_vidros_reorganizada.append(vidros_lado)

    for index, lado in enumerate(coord_vidros_reorganizada):
        quant_lado = 0
        for i, vidro in enumerate(lado):
            coord = []
            coord_50 = []
            p1 = vidro[0]
            p2 = vidro[1]
            novo_p1, novo_p2 = linha_paralela_com_offset(p1, p2, offset)
            cota_de_50_p1 = ''
            cota_de_50_p2 = ''

            #lado esquerdo (desloc_p1)
            if i == 0 and folgas_vidros[index][0] == folga_parede:
                desloc_p1 = folga_parede - calcular_gaps_furos(angs_paredes[0])
            elif i == 0 and folgas_vidros[index][0] == folga_passante:
                desloc_p1 = calcular_gaps_furos(angs_in[index-1]) + folga_passante + 50
                cota_de_50_p2 = desloc_p1
            elif i == 0 and folgas_vidros[index][0] == folga_colante:
                desloc_p1 = calcular_gaps_furos(angs_in[index-1]) + folga_colante + 50
                cota_de_50_p2 = desloc_p1
            elif i == 0 and folgas_vidros[index][0] == folga_vidro_vidro:
                desloc_p1 = calcular_gaps_furos(angs_in[index-1]) - calcular_gaps_vidro(angs_in[index-1], espessura_v) + folga_vidro_vidro + 50
                cota_de_50_p2 = desloc_p1
            else:
                desloc_p1 = -1.5

            #lado direito  (desloc_p2)
            if i == len(lado)-1 and folgas_vidros[index][1] == folga_parede:
                desloc_p2 = folga_parede*-1 + calcular_gaps_furos(angs_paredes[1])
            elif i == len(lado)-1 and folgas_vidros[index][1] == folga_passante:
                desloc_p2 = calcular_gaps_furos(angs_in[index])*-1 + folga_passante - 50
                cota_de_50_p1 = desloc_p2
            elif i == len(lado)-1 and folgas_vidros[index][1] == folga_colante:
                desloc_p2 = calcular_gaps_furos(angs_in[index])*-1 + folga_colante*-1 - 50
                cota_de_50_p1 = desloc_p2
            elif i == len(lado)-1 and folgas_vidros[index][1] == folga_vidro_vidro:
                desloc_p2 = calcular_gaps_furos(angs_in[index])*-1 + calcular_gaps_vidro(angs_in[index], espessura_v) + folga_vidro_vidro*-1 - 50
                cota_de_50_p1 = desloc_p2
            else:
                desloc_p2 = 1.5

            p1_final, p2_final = deslocar_pontos_direcao(novo_p1, novo_p2, desloc_p1, desloc_p2)
            coord.append(p1_final)
            coord.append(p2_final)
            coordenadas.append(coord)
            quant_lado += 1

            if cota_de_50_p2:
                p2_50_ini = deslocar_pontos_direcao(p1_final, p2_final, -50, 0)[0]
                p2_50_fim = p1_final
                coord_50.append(p2_50_ini)
                coord_50.append(p2_50_fim)
                coordenadas.append(coord_50)
                quant_lado += 1

            if cota_de_50_p1:
                p2_50_ini = p2_final
                p2_50_fim = deslocar_pontos_direcao(p1_final, p2_final, 0, +50)[1]
                coord_50.append(p2_50_ini)
                coord_50.append(p2_50_fim)
                coordenadas.append(coord_50)
                quant_lado += 1
        quant_furos_por_lado.append(quant_lado)

    # coordenadas_finais = redefinir_pontos_furos(coordenadas, quant_furos_por_lado, medidas_perfis_u, coord_perfis_U, offset, espessura_v)
    return coordenadas

def redefinir_pontos_furos(coord_furos: list[list[tuple[float, float, float]]], quant_furos_lado: list[int], medidas_perfis_U, coord_perfis_U: list[list[tuple[float, float, float]]], offset: int, espessura_v: int) -> list[list[tuple[float, float, float]]]:

    espessura_perfil_U = 20
    offset_corrigido = offset + espessura_v - espessura_perfil_U

    coordenadas_redefinidas = []

    perfis_U = distribuir_perfis_U_por_lado(medidas_perfis_U, coord_perfis_U)
    furos = distribuir_furos_por_lado(coord_furos, quant_furos_lado)

    for lado in range(len(perfis_U)):
        coordenadas_lado_redefinidas = []

        perfis_u_lado = perfis_U[lado]
        furos_lado = furos[lado]

        perfis_U_normalizados = []
        furos_normalizados = []

        ini_secao = ''
        ini_secao = linha_paralela_com_offset(perfis_u_lado[0][0], perfis_u_lado[0][1], offset_corrigido)[0]
        for s, perfil in enumerate(perfis_u_lado):
            ini_perfil, fim_perfil = linha_paralela_com_offset(perfil[0], perfil[1], offset_corrigido)
            perfil_normalizado = normalizar_coordenadas(ini_secao, ini_perfil, fim_perfil)
            perfis_U_normalizados.append(perfil_normalizado)

        for furo in furos_lado:
            furo_normalizado = normalizar_coordenadas(furos_lado[0][0], furo[0], furo[1])
            furos_normalizados.append(furo_normalizado)

        for i, furo_norm in enumerate(furos_normalizados):
            perfil_tocado = []
            for index, perfil_normalizado in enumerate(perfis_U_normalizados):
                for ponto in range(2):
                    if esta_entre(furo_norm[ponto], perfil_normalizado[0], perfil_normalizado[1]) == True:
                        perfil_tocado.append(index)
                    else:
                        perfil_tocado.append('')

            if perfil_tocado[0] == perfil_tocado[1] and perfil_tocado[0] != '':
                coord_nova_1 = (furo[0], perfis_u_lado[perfil_tocado[0]])
                coord_nova_2 = (perfis_u_lado[perfil_tocado[1]], furo[1])
                coordenadas_lado_redefinidas.append(coord_nova_1)
                coordenadas_lado_redefinidas.append(coord_nova_2)
            else:
                coordenadas_lado_redefinidas.append(furos_lado[i])
        coordenadas_redefinidas.append(coordenadas_lado_redefinidas)
    return coordenadas_redefinidas

def distribuir_furos_por_lado(coord_furos: list[tuple[float, float, float]], quant_furos_por_lado: list[list[tuple[float, float, float]]]) -> list[list[tuple[float, float, float]]]:
    """Distribui os vidros por lado da sacada.

    Args:
        quant_vidros: Lista com a quantidade de vidros por lado.

    Returns:
        list: Lista de sublistas com números sequenciais dos vidros de cada lado.

    Example:
        Entrada: [3, 5, 2]
        Saída: [[1, 2, 3], [4, 5, 6, 7, 8], [9, 10]]
    """
    coordenadas = []
    cont = 0
    for qtd in quant_furos_por_lado:
        coord_lado = [coord_furos[c] for c in range(cont, cont + qtd)]
        coordenadas.append(coord_lado)
        cont += qtd
    return coordenadas

