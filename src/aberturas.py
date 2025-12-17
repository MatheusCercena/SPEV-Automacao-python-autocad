def distribuir_vidros_por_lado(quant_vidros: list[int]) -> list[list[int]]:
    """Distribui os vidros por lado da sacada.

    Example:
        Entrada: [3, 5, 2]
        Saída: [[1, 2, 3], [4, 5, 6, 7, 8], [9, 10]]
    """
    todos_vidros = []
    cont = 1

    for qtd in quant_vidros:
        vidros_lado = list(range(cont, cont + qtd))
        todos_vidros.append(vidros_lado)
        cont += qtd

    return todos_vidros

def associar_aberturas_aos_lados(quant_vidros: list[int], aberturas: list) -> list:

    todos_vidros = distribuir_vidros_por_lado(quant_vidros)
    resultado = []

    for lado in todos_vidros:
        for abertura in aberturas:
            parcial = ['', 0]
            if abertura[2] in lado:  # Se o vidro giratório está neste lado
                quant = abertura[1] - abertura[0]
                if quant == 0:
                    quant = 1
                if quant > parcial[1]:
                    parcial[0] = abertura[4]
                    parcial[1] = quant
                   # 'direita' ou 'esquerda'
            else:
                parcial[0] = 0  # Não há giratório neste lado
            resultado.append(parcial[0])
    
    return resultado
