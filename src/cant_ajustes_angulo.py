"""
Módulo para cálculo e definição de cantoneiras de ajuste de ângulo.

Fornece funções para determinar a necessidade, modelo e medidas de cantoneiras de acordo com o ângulo e folgas do projeto.
"""
from src.calcs_cad import calcular_gaps_paredes
    
def necessidade_cant_ajuste(ang: float, abre_ali: bool) -> tuple[float, float, bool]:
    if abre_ali == True:
        quant_cant = 1
    else:
        quant_cant = 2

    gap_lcs = calcular_gaps_paredes(ang)

    if ang > 0: #espaco vazio pra fora
        if quant_cant == 1:
            gap_cant = gap_lcs
            necessidade = False
        if quant_cant == 2:
            gap_cant = gap_lcs*2
            if gap_cant <= 7:
                necessidade = False
            else:
                necessidade = True
    elif ang < 0: #espaco vazio pra dentro
        if quant_cant == 1:
            gap_cant = gap_lcs
            if gap_cant <= 7:
                necessidade = False
            else:
                necessidade = True
        if quant_cant == 2:
            gap_cant = gap_lcs*2
            if gap_cant <= 7:
                necessidade = False
            else:
                necessidade = True
    else: #90 graus, reto, ang 0
        gap_cant = 0
        necessidade = False

    if necessidade == True:
        gap_lcs = gap_lcs + 2
    else:
        gap_lcs = gap_lcs

    return gap_lcs, gap_cant, necessidade

def infos_cant_ajuste(gap_cant: float) -> tuple[str | None, bool | None, int | None, float | None]:
    """Retorna informações da cantoneira necessária baseada no gap.

    Returns:
        tuple: Tupla contendo:
            - Modelo da cantoneira (str ou None)
            - Se precisa ser refilada (bool ou None)
            - Medida interna da cantoneira (int ou None)
            - Medida externa da cantoneira (float ou None)
    """
    if 7 < gap_cant < 15:
        mod = 'ct-005'
        refilada = True
        medida_int = 15
        medida_ext = gap_cant - 2
    elif gap_cant == 15:
        mod = 'ct-005'
        refilada = False
        medida_int = 15
        medida_ext = 15
    elif 15 < gap_cant < 25:
        mod = 'ct-025'
        refilada = True
        medida_int = 25
        medida_ext = gap_cant - 2
    elif gap_cant == 25:
        mod = 'ct-025'
        refilada = False
        medida_int = 25
        medida_ext = 25
    elif 25 < gap_cant < 38:
        mod = 'ct-026'
        refilada = True
        medida_int = 38
        medida_ext = gap_cant - 2
    elif gap_cant == 38:
        mod = 'ct-026'
        refilada = False
        medida_int = 38
        medida_ext = 38
    elif 38 < gap_cant < 50:
        mod = 'ct-050'
        refilada = True
        medida_int = 38 #nao cabe mais no perfil U
        medida_ext = gap_cant - 2
    elif gap_cant == 50:
        mod = 'ct-050'
        refilada = False
        medida_int = 38 #nao cabe mais no perfil U
        medida_ext = 50
    else:
        mod = None
        refilada = None
        medida_int = None
        medida_ext = None

    return mod, refilada, medida_int, medida_ext
