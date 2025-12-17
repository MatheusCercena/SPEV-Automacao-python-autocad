"""
Funções para pedir os dados principais das medições para serem usadas pelas funções de desenho.
"""

def pedir_linhas_de_centro() -> list[int]:
    linhas_de_centro = []

    print(f'''
{' - '*10}LINHAS DE CENTRO{' - '*10}
''')

    cont = 1
    while True:
        try:
            lc_secoes = int(input(f'Digite a linha de centro da S{cont}: '))
            if not 30 <= lc_secoes <= 30000:
                raise ValueError
        except ValueError:
            print(f'[ERRO] Medida inválida: o valor deve ser um número inteiro entre 30 e 30000.')
            continue
        except:
            print(f'[ERRO] O campo "linha de centro" precisa conter apenas numeros inteiros: ')
            continue
        linhas_de_centro.append(lc_secoes)
        cont +=1
        res = input('Deseja digitar outra linha de centro? Digite enter para sim ou qualquer tecla para não:')
        if res != '':
            break
    return linhas_de_centro

def pedir_alturas(lcs):
    """Solicita ao usuário as alturas de cada lado da sacada.

    Returns:
        list: Lista com sublistas contendo as alturas das seções por lado.
    """
    alturas_da_sacada = []

    print(f'''
{' - '*10}ALTURAS{' - '*10}
''')

    for lado in range(len(lcs)):
        alturas_lado = []
        cont = 1
        while True:
            try:
                altura = int(input(f'Digite a {cont}ª altura no vão {lado+1}: '))
                alturas_lado.append(altura)
                cont +=1
            except:
                print(f'[ERRO] O campo "alturas" precisa conter apenas numeros inteiros: ')
                continue
            res = input('Deseja digitar outra altura para este vão? Digite enter para sim ou qualquer tecla para não: \n')
            if res != '':
                break
        alturas_da_sacada.append(alturas_lado)

    return alturas_da_sacada

def pedir_niveis(alturas):
    """Solicita ao usuário as alturas de cada lado da sacada.

    Returns:
        list: Lista com sublistas contendo as alturas das seções por lado.
    """
    print(f'''
{' - '*10}NIVEIS{' - '*10}

Como o nível está informado na medição?:
    [1] Nível ok (ou não informado)
    [2] Nível Variável (adicionar manualmente)
    [3] Desnível inferior (sem medidas)
''')

    niveis_da_sacada = []

    opt = int(input(f'Digite a opção correspondente ao nível da sacada: '))
    if opt == 1:
        for lado in alturas:
            niveis_lado = []
            for altura in lado:
                niveis_lado.append(0)
            niveis_da_sacada.append(niveis_lado)
    elif opt == 2:
        for index, lado in enumerate(alturas):
            niveis_lado = []
            for i, altura in enumerate(lado):
                while True:
                    cont = 1
                    try:
                        nivel = int(input(f'Digite o nível para a altura de {altura}, a {i+cont}ª do vão {index+cont}: '))
                        niveis_lado.append(nivel)
                        cont += 1
                        break
                    except:
                        print(f'[ERRO] O campo "niveis" precisa conter apenas numeros inteiros: ')
                        continue
            niveis_da_sacada.append(niveis_lado)
    else:
        todas_alturas = [altura for lado in alturas for altura in lado]
        menor_altura = min(todas_alturas)
        for lado in alturas:
            niveis_lado = []
            for altura in lado:
                nivel = menor_altura - altura
                niveis_lado.append(nivel)
            niveis_da_sacada.append(niveis_lado)

    return niveis_da_sacada

def pedir_quant_vidros(lcs: list[int]) -> list[int]:
    quant_vidros = []
    print(f'''
{' - '*10}QUANTIDADE DE VIDROS{' - '*10}
''')

    for c in range(0, len(lcs)):
        while True:
            try:
                quant = int(input(f'Digite a quantidade de vidros da S{c+1}: '))
                quant_vidros.append(quant)
                break
            except:
                print(f'[ERRO] O campo "quantidade de vidros" precisa conter apenas numeros inteiros: ')
                continue
    return quant_vidros

def pedir_angSecoes(lcs: list[int]) -> list[float]:
    """Solicita ao usuário os ângulos internos entre as seções.

    Args:
        lcs: Lista com as linhas de centro das seções.

    Returns:
        list: Lista com os ângulos internos no formato: [ang_1, ang_2, ..., ang_n].
    """
    angs_in = []
    print(f'''
{' - '*10}ANGULOS DAS SEÇÕES{' - '*10}

Inserir o angulo medido no transferidor, sem conversão.
''')

    for c in range(0, len(lcs)-1):
        while True:
            try:
                ang_sec = float(input(f'Qual o angulo entre a S{c+1} e a S{c+2}: ').replace(',', '.'))
                if not 40 <= ang_sec <= 320:
                    print('[ERRO] Angulo inadequado, o valor digitado deve estar entre 40 e 320. ')
                    break
                break
            except:
                print(f'[ERRO] O campo "angulo" precisa conter apenas numeros: ')
        ang_sec = 180-ang_sec
        angs_in.append(ang_sec*-1)
    return angs_in

def pedir_angParedes() -> list[float]:
    """Solicita ao usuário os ângulos das paredes extremas.

    Returns:
        list: Lista com os ângulos externos no formato: [ang_esq, ang_dir].
    """
    angs_ex = []
    print(f'''
{' - '*10}ANGULOS DAS PAREDES{' - '*10}

Inserir o angulo medido no transferidor, sem conversão
''')

    while True:
        try:
            ang_esq = float(input(f'Digite o angulo da extremidade esquerda: '))
            if not  20 < ang_esq < 160:
                print('[ERRO] Angulo inadequado, o valor digitado deve estar entre 40 e 320. ')
                break
            ang_esq_final = 90 - ang_esq
            break
        except:
            print(f'[ERRO] O campo "angulo parede esquerda" precisa conter apenas numeros: ')
    while True:
        try:
            ang_dir = float(input(f'Digite o angulo da extremidade direita: '))
            if not  20 < ang_dir < 160:
                print('[ERRO] Angulo muito pequeno (< 30) ou muito grande (> 160). ')
                break
            ang_dir_final = 90 - ang_dir
            break
        except:
            print(f'[ERRO] O campo "angulo parede direita" precisa conter apenas numeros e ter 2 dígitos: ')
    angs_ex.append(ang_esq_final)
    angs_ex.append(ang_dir_final)
    return angs_ex

def pedir_prumos() -> list[float]:
    prumos = []
    print(f'''
{' - '*10}PRUMOS{' - '*10}
''')

    while True:
        try:
            prumo_esq = float(input(f'Digite o angulo da extremidade esquerda: '))
            break
        except:
            print(f'[ERRO] O campo "prumo esquerdo" precisa conter apenas numeros: ')
    while True:
        try:
            prumo_dir = float(input(f'Digite o angulo da extremidade direita: '))
            break
        except:
            print(f'[ERRO] O campo "prumo direita" precisa conter apenas numeros: ')
    prumos.append(prumo_esq)
    prumos.append(prumo_dir)
    return prumos

def definir_juncoes(lcs: list[int], angs_in: list[float]) -> list[list[int]]:
    """Define os tipos de junção para cada seção.

    Args:
        lcs: Lista com as linhas de centro das seções.
        angs_in: Lista com os ângulos internos entre as seções.

    Returns:
        list: Lista em que cada elemento representa uma seção e cada seção tem 2 elementos:
            - Elemento 0: tipo de junção do lado esquerdo da seção
            - Elemento 1: tipo de junção do lado direito da seção

            Tipos de junção:
            - 0: vidro-parede
            - 1: passante
            - 2: colante
            - 3: vidro-vidro
    """
    print(f'''
{' - '*10}DEFINIR PASSANTES / COLANTES.{' - '*10}
''')

    juncoes = []
    for index in range(0, len(lcs)):
        esq_dir = []
        for lado in range(0, 2):
            if index == 0 and lado == 0: #parede esquerda
                esq_dir.append(0)
            elif lado == 0 and juncoes[-1][1] == 1: #se ultimo é passante, este é colante
                esq_dir.append(2)
            elif lado == 0 and juncoes[-1][1] == 2: #se ultimo é colante, este é passante
                esq_dir.append(1)
            elif lado == 0 and juncoes[-1][1] == 3: #se ultimo é vidro-vidro, este é vidro-vidro
                esq_dir.append(3)
            elif len(angs_in) != 0 and index < len(angs_in):
                if 70 < (abs(angs_in[index])) < 110: #passante-colante
                    res = input(f'A juncão entre os vidros do lado {index} e {index+1} será passante e colante, qual deseja que seja o passante? Digite "e" para o vidro do lado {index} ou "d" para o vidro do lado {index + 1}: ')
                    while res not in ['e', 'd']:
                        res = input(f'A juncão entre os vidros do lado {index} e {index+1} será passante e colante, qual deseja que seja o passante? Digite "e" para o vidro do lado {index} ou "d" para o vidro do lado {index + 1}: ')
                    if res == 'e': #se esquerda é passante, este é passante
                        esq_dir.append(1)
                    if res == 'd': #se direita é passante, este é colante
                        esq_dir.append(2)
                else: #vidro-vidro
                    esq_dir.append(3)
            else: #parede direita
                esq_dir.append(0)
        juncoes.append(esq_dir)

    return juncoes

def solicitar_sentido_abertura(quant_vidros: list[int]) -> tuple[list, list[int]]:
    sentidos = []
    moveis = []
    v_ini = ''
    v_fin = ''
    giratorio = ''
    adjacente = ''
    print(f'''
{' - '*10}SENTIDOS DE ABERTURA{' - '*10}
''')
    cont = 1
    while True:
        if len(moveis) > 0 and max(moveis) >= sum(quant_vidros):
            break
        while True:
            try:
                v_ini = int(input(f'Digite o vidro onde começa a {cont}ª abertura: '))
                if v_ini > sum(quant_vidros):
                    print(f'A sacada tem menos que {v_ini} vidros. Escolha um vidro existente na sacada')
                    continue
                elif v_ini not in moveis and v_ini != 0:
                    break
                else:
                    print('Esse vidro já abre em outro lugar.')
                    continue
            except:
                print(f'[ERRO] O vidro precisa ser numérico.')
        while True:
            try:
                v_fin = int(input(f'Digite o vidro onde termina a {cont}ª abertura: '))
                if v_fin > sum(quant_vidros):
                    print(f'A sacada tem menos que {v_fin} vidros. Escolha um vidro existente na sacada')
                    continue
                elif v_fin not in moveis and v_fin != 0:
                    break
                else:
                    print('Esse vidro já abre em outro lugar.')
                    continue
            except:
                print(f'[ERRO] O vidro precisa ser numérico.')
        while True:
            try:
                giratorio = int(input(f'O vidro giratório da abertura será no {v_ini} ou no {v_fin}? '))
                if giratorio in [v_ini, v_fin]:
                    break
                else:
                    print(f'O vidro giratório precisa ser o {v_ini} ou o {v_fin}.')
                    continue
            except:
                print(f'[ERRO] O vidro giratório precisa ser numérico.')
        [moveis.append(vidro) for vidro in range(v_ini, v_fin+1)]
        sentido = 'direita' if giratorio == v_fin else 'esquerda'
        vidros_na_abertura = [n for n in range(v_ini, v_fin+1)]
        adjacente = (giratorio-1 if sentido == 'direita' else giratorio+1) if len(vidros_na_abertura) >= 2 else 0
        print(f'Certo, os vidros da {cont}ª abertura irao abrir para a {sentido}.')
        abertura = [v_ini, v_fin, giratorio, adjacente, sentido]
        sentidos.append(abertura)
        cont += 1

        res = ''

        while res not in ['s', 'n'] and max(moveis) != sum(quant_vidros):
            res = input(f'Deseja informar outra abertura? [s/n]').strip().lower()
            if res not in ['s', 'n']:
                print('A resposta precisa ser "s" ou "n".')
        if res == 'n' or max(moveis) == sum(quant_vidros):
            fixos = []
            for vidro in range(1, sum(quant_vidros)+1):
                if vidro not in moveis:
                    fixos.append(vidro)
            return sentidos, fixos
        if res == 's':
            continue

def pedir_elevador() -> int:
    """Solicita ao usuário a altura máxima do elevador.

    Returns:
        int: Altura máxima do elevador em milímetros.
    """
    print(f'''
{' - '*10}ALTURA ELEVADOR{' - '*10}
''')

    while True:
        try:
            elevador = input(f'Digite a medida segura do elevador: ')
            if len(elevador) != 4  or not elevador.isdigit():
                raise ValueError
            elevador = int(elevador)
            break
        except:
            print(f'[ERRO] O campo "elevador" precisa conter apenas numeros inteiros e ter 4 dígitos.')
    return elevador

def converter_juncoes_valor(juncoes):
    juncoes_finais = juncoes
    for juncao in juncoes_finais:
        if juncao[0] == 'Vidro/Parede':
            juncao[0] = 0
        elif juncao[0] == 'Passante':
            juncao[0] = 1
        elif juncao[0] == 'Colante':
            juncao[0] = 2
        elif juncao[0] == 'Vidro/Vidro':
            juncao[0] = 3

        if juncao[1] == 'Vidro/Parede':
            juncao[1] = 0
        elif juncao[1] == 'Passante':
            juncao[1] = 1
        elif juncao[1] == 'Colante':
            juncao[1] = 2
        elif juncao[1] == 'Vidro/Vidro':
            juncao[1] = 3

    return juncoes_finais