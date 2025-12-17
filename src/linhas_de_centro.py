from pyautocad import Autocad, APoint
from math import radians
from src.autocad_conn import get_acad

def definir_linhas_de_centro(lcs: list[int], angs_in: list[float]) -> list[list[float, float, float, float]]:
    cad, acad_ModelSpace = get_acad()
    acad = Autocad(create_if_not_exists=True)

    lista_de_LCs = lcs.copy()
    linha = acad.model.AddLine(APoint(0, 0), APoint(lcs[0], 0))
    inicio = linha.StartPoint
    final = linha.EndPoint
    angs = 0
    coord_linhas = [inicio[0], inicio[1], final[0], final[1]]
    coord_de_linhas_de_centro = []
    coord_de_linhas_de_centro.append(coord_linhas)
    linha.Delete()

    for l in range(1, len(lista_de_LCs)):
        linha = acad.model.AddLine(APoint(final[0], final[1]), APoint(final[0] + lista_de_LCs[l], final[1]))
        linha.Rotate(APoint(final[0], final[1]), radians(angs_in[l-1] + angs))
        angs += angs_in[l-1]
        inicio = linha.StartPoint
        final = linha.EndPoint

        coord_linhas = [inicio[0], inicio[1], final[0], final[1]]
        coord_de_linhas_de_centro.append(coord_linhas)
        linha.Delete()

    return coord_de_linhas_de_centro

def ordem_lcs(lcs: list, sec_princ: int) -> list[int]:
    lista = []
    lista.append(sec_princ)
    if sec_princ < len(lcs)-1:
        for c in range(sec_princ + 1, len(lcs)):
            lista.append(c)
    if sec_princ >= 1:
        lista.append(sec_princ-1)
        if sec_princ >= 1:
            for c in reversed(range(sec_princ-1)):
                lista.append(c)
    return lista

def redesenhar_linhas_de_centro(lcs: list[int], angs_in: list[float], sec_princ: int) -> tuple[list[list[float]], list]:
    """Redesenha as linhas de centro no AutoCAD a partir da seção principal."""
    cad, acad_ModelSpace = get_acad()
    acad = Autocad(create_if_not_exists=True)

    lista_de_LCs = lcs.copy()
    #desenha a seção principal a partir de (0, 0)
    linha = acad.model.AddLine(APoint(0, 0), APoint(lista_de_LCs[sec_princ], 0))
    linha.Layer = 'Linha de Centro'
    inicio = linha.StartPoint
    final = linha.EndPoint
    angs = 0
    coord_linhas = [inicio[0], inicio[1], final[0], final[1]]
    lista_de_LCs[sec_princ] = coord_linhas

    #desenha as seções depois da seção principal, SE existirem | se a seção principal for 0 e só tiver uma seção, ignora
    if sec_princ < len(lcs)-1:
        for l in range(sec_princ + 1, len(lista_de_LCs)):
            linha = acad.model.AddLine(APoint(final[0], final[1]), APoint(final[0] + lista_de_LCs[l], final[1]))
            linha.Rotate(APoint(final[0], final[1]), radians(angs_in[l-1] + angs))
            linha.Layer = 'Linha de Centro'
            angs += angs_in[l-1]
            inicio = linha.StartPoint
            final = linha.EndPoint

            coord_linhas = [inicio[0], inicio[1], final[0], final[1]]
            lista_de_LCs[l] = coord_linhas

    #desenha a primeira seção antes da seção principal, SE existirem
    if sec_princ >= 1:
        linha = acad.model.AddLine(APoint(0 - lista_de_LCs[sec_princ-1], 0), APoint(0, 0))
        linha.Rotate(APoint(0, 0), radians(angs_in[sec_princ-1] * -1))
        linha.Layer = 'Linha de Centro'
        inicio = linha.StartPoint
        final = linha.EndPoint
        angs = angs_in[sec_princ-1]
        coord_linhas = [inicio[0], inicio[1], final[0], final[1]]
        lista_de_LCs[sec_princ-1] = coord_linhas

    #desenha as seções antes da seção principal, SE existirem
        if sec_princ >= 2:
            for l in reversed(range(sec_princ-1)):
                linha = acad.model.AddLine(APoint(inicio[0] - lista_de_LCs[l], inicio[1]), APoint(inicio[0], inicio[1]))
                linha.Rotate(APoint(inicio[0], inicio[1]), radians((angs_in[l] + angs)*-1))
                linha.Layer = 'Linha de Centro'
                angs += angs_in[l]
                inicio = linha.StartPoint
                final = linha.EndPoint

                coord_linhas = [inicio[0], inicio[1], final[0], final[1]]
                lista_de_LCs[l] = coord_linhas

    novas_lcs = []
    for linha in acad_ModelSpace:
        if linha.EntityName == 'AcDbLine' and linha.Layer == 'Linha de Centro':
            novas_lcs.append(linha)

    ordem_desenho = ordem_lcs(novas_lcs, sec_princ)
    lista = novas_lcs.copy()

    for index, value in enumerate(ordem_desenho):
        lista[value] = novas_lcs[index]
    return lista_de_LCs, lista

def definir_coord_lcs(pos_lcs: list[list[float]]) -> list[tuple[float, float, float]]:
    """Define as coordenadas 3D das linhas de centro."""
    coordenadas = []
    for lcs in pos_lcs:
        coord = []

        p0 = (lcs[0], lcs[1], 0.0)
        p1 = (lcs[2], lcs[3], 0.0)
        p2 = p0
        p3 = p1

        coord.append(p0)
        coord.append(p1)
        coord.append(p2)
        coord.append(p3)
        coordenadas.append(coord)
    return coordenadas