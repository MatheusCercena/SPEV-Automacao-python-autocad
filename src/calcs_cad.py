from math import sin, cos, tan, radians, atan2

def calcular_gaps_paredes(ang: float) -> float:
    """Calcula o gap entre a linha de centro e a parede. O gap é diferente de 0 no caso de paredes anguladas."""
    cat_adj = 18
    gap_lcs = round((tan(radians(abs(ang))) * cat_adj), 0)
    return gap_lcs

def calcular_gaps_leito(ang: float) -> float:
    """Calcula o gap entre os leitos e a linha de centro. Usado quando é junção do tipo vidro-vidro."""
    cat_adj = 14
    gap_leito = round((tan(radians(abs(ang/2))) * cat_adj), 2)
    return gap_leito

def calcular_gaps_vidro(ang: float, espessura_vidro: int) -> float:
    """Calcula o gap entre o vidro e a linha de centro. Usado quando é junção do tipo vidro-vidro."""
    cat_adj = espessura_vidro/2
    gap_vidro = round((tan(radians(abs(ang/2))) * cat_adj), 2)
    return gap_vidro

def calcular_gaps_furos(ang: float) -> float:
    """Calcula o gap entre o vidro e a linha de centro. Usado quando é junção do tipo vidro-vidro."""
    cat_adj = 22
    gap_vidro = round((tan(radians(abs(ang/2))) * cat_adj), 2)
    return gap_vidro

def obter_pontos_medida_total(perfil: list[tuple[float, float, float]]) -> tuple[list[int], tuple[float, float, float], tuple[float, float, float]]:
    """Obtém os pontos para cota de medida total de um perfil.
    
    Dado um perfil com 4 pontos [(x0,y0,z0), (x1,y1,z1), (x2,y2,z2), (x3,y3,z3)] 
    ou em outras palavras [(ini_int), (fim_int), (ini_ext), (fim_ext)], retorna 
    dois pontos (x, y, z) que definem corretamente a cota entre os extremos, com 
    offset perpendicular ao vetor base e rotação compensada.
    
    Args:
        perfil: Lista com 4 pontos 3D do perfil.
    
    Returns:
        tuple: Tupla contendo:
            - Lista com índices dos pontos extremos
            - Ponto de início da cota (x, y, z)
            - Ponto de fim da cota (x, y, z)
    """
    # 1. Vetor base: ponto 0 (início interno) até ponto 1 (fim interno)
    base = perfil[0]
    direcao = perfil[1]
    dx = direcao[0] - base[0]
    dy = direcao[1] - base[1]
    theta = -atan2(dy, dx)  # rotação para alinhar com eixo X

    # 2. Rotaciona todos os pontos para normalizar
    rotacionados = []
    for i, ponto in enumerate(perfil):
        x, y = ponto[:2] 
        xt = x - base[0]
        yt = y - base[1]
        xr = xt * cos(theta) - yt * sin(theta)
        yr = xt * sin(theta) + yt * cos(theta)
        rotacionados.append((i, xr, yr))

    # 3. Identifica os extremos (menor e maior X)
    extremos = rotacionados
    extremos_sorted = sorted(extremos, key=lambda p: p[1])
    ponto_ini_idx, x_ini, y_ini = extremos_sorted[0]
    ponto_fim_idx, x_fim, y_fim = extremos_sorted[-1]

    # pontos corrigidos
    pontos = [ponto_ini_idx, ponto_fim_idx]
    x_rot_ini = x_ini * cos(-theta)
    y_rot_ini = x_ini * sin(-theta)
    ponto_inicio = (x_rot_ini + base[0], y_rot_ini + base[1], 0.0)

    x_rot_fim = x_fim * cos(-theta)
    y_rot_fim = x_fim * sin(-theta)

    ponto_fim = (x_rot_fim + base[0], y_rot_fim + base[1], 0.0)

    return pontos, ponto_inicio, ponto_fim

