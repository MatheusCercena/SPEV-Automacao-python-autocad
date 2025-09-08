
def calcular_quantidade_pe3(giratorios, quant_vidros):
    quantidade_pe3 = 0
    quantidade_vidros = 0
    for vidros_secao in quant_vidros:
        quantidade_vidros += vidros_secao

    if giratorios[0] == 1:
        quantidade_pe3 += 1
    else:
        quantidade_pe3 += 2

    if giratorios[-1] == quantidade_vidros:
        quantidade_pe3 += 1
    else:
        quantidade_pe3 += 2

    return quantidade_pe3
