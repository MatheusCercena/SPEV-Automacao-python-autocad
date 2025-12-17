from src.calcs_vetor import maior_valor, menor_valor, interpolar_valor_em_x, ponto_medio, ponto_perpendicular_a_vetor
from src.vidros import achar_posicao_vidro
from src.comandos_cad import adicionar_texto_modelspace
from pyautocad import APoint

def definir_niveis(niveis: list[list[int]], lcs: list[int], quant_vidros: list[int], sentidos_abert: list[list[int, int, int, int, str]]):
    # Ajustando niveis para padrao de base 0
    maior_nivel = maior_valor(niveis)
    niveis_base_0 = [[nivel - maior_nivel for nivel in lado] for lado in niveis]

    # Ajustando niveis pelo giratorio
    niveis_giratorios = obter_altura_giratorios(sentidos_abert, quant_vidros, niveis_base_0, lcs)
    maior_nivel_giratorio = max(niveis_giratorios)
    niveis_base_giratorio = [[nivel + abs(maior_nivel_giratorio) for nivel in lado] for lado in niveis_base_0] # Deixa como ponto 0 o giratorio mais alto
    trilho_mais_socado = maior_valor(niveis_base_giratorio)

    # Reajustando niveis para evitar trilho socado
    if trilho_mais_socado >= 12:
        tms = trilho_mais_socado
        diferenca = tms - 12
        niveis_finais = [[nivel + diferenca if nivel != tms else tms for nivel in lado] for lado in niveis_base_giratorio] # Sobe todos os niveis o suficiente para manter o maior nivel como 12 (socado ao maximo mas ainda permitindo instalacão)
        ponto_base = diferenca
    else:
        niveis_finais = niveis_base_giratorio
        ponto_base = 0

    # Definição da sucata inferior
    maior_nivel_final = maior_valor(niveis_finais) - ponto_base
    menor_nivel_final = menor_valor(niveis_finais) + ponto_base
    if menor_nivel_final <= -12 and maior_nivel_final < 9: # se precisa de sucata e nao tem trilhos já socados/trilhos podem descer 3mm
        print(f"Diferença de nível de {abs(menor_nivel_final)}. Necessário usar sucata de trilho na parte inferior.")
        opt = input('Deseja aumentar a altura dos vidros em +3mm para embutir a contrafechadura? [s/n]').strip().lower()
        if opt == 's':
            niveis_finais = [[nivel - 3 if nivel == ponto_base else nivel for nivel in lado] for lado in niveis_finais]
            ponto_base -= 3
        elif opt == 'n':
            pass
        else:
            print('Por favor, digite apenas o caracteres "s" ou "n".')

    return niveis_finais, ponto_base

def alturas_por_nivel(alturas, niveis_finais):
    ''' Adiciona os níveis finais às alturas dos vidros. '''
    alturas_finais = [[altura + niveis_finais[i][j] for j, altura in enumerate(lado)] for i, lado in enumerate(alturas)]
    return alturas_finais

def diferenca_alturas(alturas_finais, lcs, quant_vidros, sentidos_abert):
    ''' Calcula a diferença de alturas entre os vidros e o nível, conforme o sentido de abertura.'''
    # Ajustando alturas para padrao de base 0
    menor_altura = menor_valor(alturas_finais)
    alturas_base_0 = [[altura - menor_altura for altura in lado] for lado in alturas_finais]

    # 2.1 Ajustando alturas pelo giratorio
    alturas_giratorios = obter_altura_giratorios(sentidos_abert, quant_vidros, alturas_base_0, lcs)
    altura_sistema = min(alturas_giratorios)
    diferencas_de_altura = [[altura - altura_sistema for altura in lado] for lado in alturas_base_0]
    trilho_mais_socado = menor_valor(diferencas_de_altura)

    # 2.2 Reajustando alturas para evitar trilho socado
    if trilho_mais_socado <= -12:
        tms = trilho_mais_socado
        diferenca = tms + 12 # sempre negativo
        diferencas_finais = [[altura + diferenca if altura != tms else tms for altura in lado] for lado in diferencas_de_altura]
        altura_base = diferenca
    else:
        diferencas_finais = diferencas_de_altura
        altura_base = 0

    # 2.3 Definição de sucata superior
    maior_altura_superior = maior_valor(diferencas_finais)
    menor_altura_superior = maior_valor(diferencas_finais)
    if maior_altura_superior >= 12 and menor_altura_superior > -7:
        print(f"Diferença de altura de {abs(maior_altura_superior)}. Necessário usar sucata de trilho na parte superior.")
        opt = input('Deseja usar perfil U com calha interna na parte de cima e aumentar a altura dos vidros em +5mm para embutir a molinha na calha do perfil U com calha? [s/n]').strip().lower()
        if opt == 's':
            diferencas_finais = [[altura + 5 for altura in lado] for lado in diferencas_finais]
            altura_base += 5
        elif opt == 'n':
            pass
        else:
            print('Por favor, digite apenas o caracteres "s" ou "n".')

    # return diferencas_finais
    return diferencas_finais, altura_base

def folga_altura_vidro(diferenca_superior, diferenca_inferior):
    '''Calcula a folga de altura do vidro com base nas diferenças de altura superior e inferior.'''
    if diferenca_superior <= 7 and diferenca_inferior >= -7:
        folga_vidro = int(165)
    else:
        folga_vidro = int(160)

    return folga_vidro

def obter_altura_giratorios(
    aberturas: list[list[int]],
    quant_vidros: list[int],
    fonte: list[list[int]],
    lcs: list[int]
) -> list[float]:

    posicao = achar_posicao_vidro(quant_vidros)
    resultado = []

    for abertura in aberturas:
        vidro = abertura[2]
        lado, index_local = posicao[vidro]
        total_vidros = quant_vidros[lado]
        largura_total = lcs[lado]

        # Obter coordenadas X normalizadas da medição
        n_pontos = len(fonte[lado])
        step = largura_total / (n_pontos - 1) if n_pontos > 1 else 0
        pontos_x = [i * step for i in range(n_pontos)]

        # Obter posição real do vidro no eixo X
        largura_vidro = largura_total / total_vidros
        centro_vidro = (index_local + 0.5) * largura_vidro

        altura_interpolada = interpolar_valor_em_x(pontos_x, fonte[lado], centro_vidro)
        resultado.append(altura_interpolada)

    return resultado
