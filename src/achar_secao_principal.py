from src.calcs_vetor import normalizar, ponto_medio, somar_pontos, multiplicar_vetor
from sympy import symbols, Eq, solve
from src.calcs_vetor import dentro_do_intervalo

x, y, b = symbols('x y b')

def definir_linha_perpendicular(pos_lcs: list) -> tuple[float, float, float, float]:
    """Define uma linha perpendicular às linhas de centro.

    A partir das posições das linhas de centro, define dois pontos (C1 e C2) sobre uma reta
    perpendicular à reta formada entre o início da primeira e o final da última seção.

    Args:
        pos_lcs: Lista com as posições das linhas de centro.

    Returns:
        tuple: Coordenadas dos pontos C1 e C2 (x1, y1, x2, y2).
    """
    ponto_ini = (pos_lcs[0][0], pos_lcs[0][1])
    ponto_fim = (pos_lcs[-1][2], pos_lcs[-1][3])
    ponto_base = ponto_medio(ponto_ini, ponto_fim)
    vetor_AB = (ponto_fim[0] - ponto_ini[0], ponto_fim[1] - ponto_ini[1])

    # Vetores perpendiculares a AB
    vetor_perp1 = (-vetor_AB[1], vetor_AB[0])   # 90 graus
    vetor_perp2 = (vetor_AB[1], -vetor_AB[0])   # -90 graus

    # Comprimento do segmento perpendicular desejado
    comprimento = 50000

    # Normaliza e escala os vetores
    deslocamento1 = multiplicar_vetor(normalizar(vetor_perp1), comprimento)
    deslocamento2 = multiplicar_vetor(normalizar(vetor_perp2), comprimento)

    # Pontos C1 e C2 sobre a perpendicular
    coord_c1 = somar_pontos(ponto_base, deslocamento1)
    coord_c2 = somar_pontos(ponto_base, deslocamento2)

    return coord_c1[0], coord_c1[1], coord_c2[0], coord_c2[1]

def def_eq_reta(secao: list) -> Eq:
    """Define a equação da reta de uma seção.

    Define a equação da reta a ser usada para verificar se a seção intercepta a linha perpendicular.

    Args:
        secao: Lista com as coordenadas da seção [x1, y1, x2, y2].

    Returns:
        Eq: Equação da reta da seção.
    """
    valor_m = (secao[3] - secao[1]) / (secao[2] - secao[0])
    y_f = secao[3]
    x_f = secao[2]
    eq_b = Eq(y_f, valor_m*x_f + b)
    valor_b = solve(eq_b, b)[0]

    return Eq(y, valor_m*x + valor_b)

def verificar_se_intercepta(secao: list, interseccao: dict) -> bool:
    """Verifica se uma seção intercepta a linha guia."""

    intervalo_x = sorted([secao[0], secao[2]])
    intervalo_y = sorted([secao[1], secao[3]])

    condicao1 = dentro_do_intervalo(interseccao[x], intervalo_x[0], intervalo_x[1])
    condicao2 = dentro_do_intervalo(interseccao[y], intervalo_y[0], intervalo_y[1])

    if (condicao1 == True) and (condicao2 == True):
        return True
    else:
        return False

def descobrir_secao_principal(pos_lcs: list) -> int:
    if len(pos_lcs) == 1:
        return 0
    else:
        coord_c = definir_linha_perpendicular(pos_lcs)
        for secao in range(0, len(pos_lcs)):
            interseccao = solve((def_eq_reta(pos_lcs[secao]), def_eq_reta(coord_c)), (x, y))
            # verificar se intercepta / solve ou def eq reta esta dando problema, verificar
            verificacao = verificar_se_intercepta(pos_lcs[secao], interseccao)
            if verificacao == True:
                return int(secao)
            else:
                continue