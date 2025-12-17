from pyautocad import Autocad, APoint
from src.calcs_vetor import ponto_medio, somar_pontos, multiplicar_vetor, vetor_perpendicular_unitario, angulo_do_vetor
from src.calcs_cad import obter_pontos_medida_total


def cotar_medida_total(perfis: list, tipo_cota: str = 'ISO-25', offset: int = 200) -> None:
    """Cria cotas de medida total para os perfis no AutoCAD.

    Args:
        perfis: Lista com os perfis a serem cotados.
        tipo_cota: Tipo de cota a ser utilizada. Padrão: 'ISO-25'.
        offset: Distância de offset da cota. Padrão: 200.

    Returns:
        None: Função cria cotas no AutoCAD sem retorno.
    """
    autocad = Autocad(create_if_not_exists=True)

    for perfil in perfis:
        pontos, p1, p2 = obter_pontos_medida_total(perfil)
        a1 = APoint(*p1)
        a2 = APoint(*p2)

        # Ângulo da cota (do vetor do lado interno)
        x0 = perfil[0][0]
        y0 = perfil[0][1]
        x1 = perfil[1][0]
        y1 = perfil[1][1]
        ang = angulo_do_vetor((x0, y0), (x1, y1))

        # Vetor perpendicular unitário
        v_perp = vetor_perpendicular_unitario(p1, p2)

        # se as extremidades forem negativas ele puxa a cota pra baixo
        # if pontos == '' or pontos == '':
        #     offset = offset*-1

        # Ponto médio com offset perpendicular
        meio = ponto_medio(p1, p2)
        deslocado = somar_pontos(meio, multiplicar_vetor(v_perp, offset))
        loc = APoint(*deslocado)

        # Criar a cota
        dim = autocad.model.AddDimRotated(a1, a2, loc, ang)
        dim.TextRotation = ang
        dim.StyleName = tipo_cota
        dim.TextMovement = 2
        dim.TextOutsideAlign = False
        dim.TextInsideAlign = True
