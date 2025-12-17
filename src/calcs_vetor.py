"""
Módulo de funções matemáticas e geométricas auxiliares para cálculos de projetos CAD.

Inclui operações com vetores e manipulação de coordenadas para uso em outros módulos do projeto.
"""
from math import sqrt, atan2

def contar_entre_numeros(a: int, b: int) -> int:
    return max(0, abs(b - a) + 1)

def maior_valor(lista):
    return max(max(sublista) for sublista in lista)

def menor_valor(lista):
    return min(min(sublista) for sublista in lista)

def vetor_entre_pontos(p1: tuple[float, float, float], p2: tuple[float, float, float]) -> tuple[float, float, float]:
    return (p2[0] - p1[0], p2[1] - p1[1], 0.0)

def normalizar(vetor: tuple[float, float]) -> tuple[float, float, float]:
    norma = sqrt(vetor[0]**2 + vetor[1]**2)
    return (vetor[0]/norma, vetor[1]/norma, 0.0)

def distancia_2d(p1: tuple[float, float, float], p2: tuple[float, float, float]) -> float:
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def multiplicar_vetor(vetor: tuple[float, float, float], escalar: float) -> tuple[float, float, float]:
    return (vetor[0] * escalar, vetor[1] * escalar, 0.0)

def somar_pontos(p1: tuple[float, float, float], p2: tuple[float, float, float]) -> tuple[float, float, float]:
    return (p1[0] + p2[0], p1[1] + p2[1], 0.0)

def ponto_medio(p1: tuple[float, float, float], p2: tuple[float, float, float]) -> tuple[float, float, float]:
    return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2, 0.0)

def angulo_do_vetor(p1: tuple[float, float, float], p2: tuple[float, float, float]) -> float:
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return atan2(dy, dx)

def normalizar_coordenadas(ponto_inicial: tuple[float, float, float], p1: tuple[float, float, float], p2: tuple[float, float, float]) -> tuple[float, float]:
    novo_p1 = distancia_2d(ponto_inicial, p1)
    novo_p2 = distancia_2d(ponto_inicial, p2)
    return novo_p1, novo_p2

def esta_entre(a: float, x: float, y: float) -> bool:
    if a >= min(x, y) and a <= max(x, y):
        return True
    else:
        return False

def vetor_perpendicular_unitario(p1: tuple[float, float, float], p2: tuple[float, float, float]) -> tuple[float, float, float]:
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    mod = sqrt(dx**2 + dy**2)
    return (-dy / mod, dx / mod, 0.0)

def ponto_perpendicular_a_vetor(ponto_base: tuple[float, float, float], p1: tuple[float, float, float], p2: tuple[float, float, float], comprimento: float) -> tuple[float, float, float]:
    perp = vetor_perpendicular_unitario(p1, p2)
    ponto_final = somar_pontos(ponto_base, multiplicar_vetor(perp, comprimento))
    return ponto_final

def linha_paralela_com_offset(p1: tuple[float, float, float], p2: tuple[float, float, float], offset: float) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
    vetor_perp = vetor_perpendicular_unitario(p1, p2)
    deslocamento = multiplicar_vetor(vetor_perp, offset)

    novo_p1 = somar_pontos(p1, deslocamento)
    novo_p2 = somar_pontos(p2, deslocamento)

    return novo_p1, novo_p2

def interpolar_valor_em_x(pontos: list[float], valores: list[float], x: float) -> float:
    if len(pontos) == 1:
        return valores[0]

    for i in range(len(pontos) - 1):
        x0, x1 = pontos[i], pontos[i + 1]
        y0, y1 = valores[i], valores[i + 1]
        if x0 <= x <= x1:
            # Interpolação linear
            t = (x - x0) / (x1 - x0)
            return y0 + t * (y1 - y0)

    # Fora da faixa → extrapola no final
    if x <= pontos[0]:
        return valores[0]
    return valores[-1]

def obter_dados_intervalo(dados: list, valor_inicial: int, valor_final: int):
    """
    Retorna os dados entre valor_inicial e valor_final (inclusive).
    Assume que o valor 1 está no índice 0 da lista.

    Exemplo:
    medidas_vidros = [1000, 1010, 1020, 1030, 1040]
    obter_medidas_intervalo(medidas_vidros, 2, 4) -> [1010, 1020, 1030]
    """
    dados = [dado for sublista in dados for dado in sublista]
    inicio = valor_inicial - 1
    fim = valor_final

    return dados[inicio:fim]

def deslocar_pontos_direcao(
    p1: tuple[float, float, float],
    p2: tuple[float, float, float],
    desloc_p1: float,
    desloc_p2: float,
    a_partir_de_p1: bool = False
) -> tuple[tuple[float, float, float], tuple[float, float, float]]:

    vetor = vetor_entre_pontos(p1, p2)
    vetor_unitario = normalizar(vetor)

    if a_partir_de_p1:
        base_ponto_2 = p1
    else:
        base_ponto_2 = p2

    novo_p1 = somar_pontos(p1, multiplicar_vetor(vetor_unitario, desloc_p1))
    novo_p2 = somar_pontos(base_ponto_2, multiplicar_vetor(vetor_unitario, desloc_p2))

    return novo_p1, novo_p2

def definir_pontos_na_secao(inicio_secao: tuple[float, float, float], vetor_unitario: tuple[float, float, float], distancia: float) -> tuple[float, float, float]:
    return (
        inicio_secao[0] + vetor_unitario[0] * distancia,
        inicio_secao[1] + vetor_unitario[1] * distancia,
        0.0
    )

def dentro_do_intervalo(valor: float, minimo: float, maximo: float, tol: float = 1e-6) -> bool:
    """Verifica se um valor está dentro de um intervalo fechado."""

    limite_inferior = min(minimo, maximo)
    limite_superior = max(minimo, maximo)

    return (limite_inferior - tol) <= valor <= (limite_superior + tol)

