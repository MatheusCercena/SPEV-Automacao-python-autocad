from src.aberturas import associar_aberturas_aos_lados
from src.adicionar_informacoes import posicionar_alturas, posicionar_pivos, posicionar_angulos
from src.alturas_niveis import definir_niveis, alturas_por_nivel, diferenca_alturas, folga_altura_vidro
from src.achar_secao_principal import descobrir_secao_principal
from src.bocas import definir_aberturas, desenhar_bocas, desenhar_pivos_individuais
from src.calcs_vetor import menor_valor, maior_valor
from src.cant_ajustes_angulo import necessidade_cant_ajuste, infos_cant_ajuste
from src.comandos_cad import carregar_comandos, remover_guias, adicionar_texto_modelspace
from src.cotas import cotar_medida_total
from src.drenos import definir_coord_drenos
from src.ferragens import calcular_lista_ferragens
from src.furos import definir_pontos_furos
from src.leitos import folgas_leitos, desenhar_guias_leitos, desenhar_leitos
from src.limpar import limpar_tudo
from src.linhas_de_centro import definir_linhas_de_centro, redesenhar_linhas_de_centro, definir_coord_lcs
from src.logs import log_spev
from src.paredes import fazer_parede_esq, fazer_parede_dir, fillet_paredes
from src.perfis import calcular_lista_perfis_rolo
from src.perfis_U import offset_perfis_U, fillet_perfis_U, definir_coord_perfis_U, redefinir_coord_perfis_U
from src.perfis_extras import calcular_quantidade_pe3
from src.pivos import definir_pivos
from src.recebimento_da_medicao import pedir_linhas_de_centro, pedir_quant_vidros, pedir_angSecoes, pedir_angParedes, pedir_prumos, definir_juncoes, solicitar_sentido_abertura, pedir_elevador, pedir_alturas, pedir_niveis, converter_juncoes_valor
from src.sucata import necessidade_de_sucata, definir_diferencas
from src.scrapper.cadastrar_sacada import cadastrar_sacada
from src.vidros import offset_vidros, medida_dos_vidros, definir_folgas_vidros, pontos_dos_vidros, desenhar_guias_vidros

import traceback
from PyQt6.QtWidgets import QMessageBox


def projetar(dados, codigo_projeto):
# if __name__ == "__main__":
    try:
        id = codigo_projeto
        log_spev(f'Inicio da execução ID: {id}')

        limpar_tudo()

        # EXEMPLO 1
        # lcs = [590, 2505]
        # alturas = [[1137, 1138], [1138, 1141]]
        # niveis = [[5, 0], [0, -5]]
        # quant_vidros = [2, 5]
        # angs_in = [-90]
        # sentidos_abert = [[1, 12, 1, 2, 'esquerda']]
        # juncoes = [[0, 2], [1, 0]]

        # # EXEMPLO 2
        # ordem_servico = '1508/25-1'
        # lcs = [1000, 3000]
        # alturas = [[1000], [1000]]
        # niveis = [[0], [0]]
        # quant_vidros = [3, 6]
        # angs_in = [-90.0]
        # sentidos_abert = [[1, 3, 1, 2, 'esquerda'], [4, 9, 9, 8, 'direita']]
        # juncoes = [[0, 2], [1, 0]]
        # angs_paredes = [0.0, 0.0]
        # prumos = [0, 0]
        # elevador = 2600

        # INSERCAO MANUAL DOS DADOS
        # lcs = pedir_linhas_de_centro()
        # alturas = pedir_alturas(lcs)
        # niveis = pedir_niveis(alturas)
        # quant_vidros = pedir_quant_vidros(lcs)
        # sentidos_abert, fixos = solicitar_sentido_abertura(quant_vidros)
        # angs_in = pedir_angSecoes(lcs)
        # angs_paredes = pedir_angParedes()
        # prumos = pedir_prumos()
        # juncoes = definir_juncoes(lcs, angs_in)
        # elevador = pedir_elevador()

        # PEGA DADOS DA INTERFACE
        ordem_servico = dados['ordem_servico']
        lcs = dados['linhas_centro']
        alturas = dados['alturas']
        niveis = dados['niveis']
        quant_vidros = dados['quantidade_vidros']
        sentidos_abert = dados['aberturas']
        angs_in = [angulo for angulo in dados['angulos_internos']]
        angs_paredes = [angulo for angulo in dados['angulos_paredes']]
        prumos = dados['prumos']
        juncoes = converter_juncoes_valor(dados['juncoes'])
        elevador = dados['elevador']

        # print(f'OS: {ordem_servico}')
        # print(f'LCS: {lcs}')
        # print(f'Alturas: {alturas}')
        # print(f'Níveis: {niveis}')
        # print(f'Quantidade de Vidros: {quant_vidros}')
        # print(f'Sentidos de Abertura: {sentidos_abert}')
        # print(f'Ângulos Internos: {angs_in}')
        # print(f'Ângulos de Paredes: {angs_paredes}')
        # print(f'Prumos: {prumos}')
        # print(f'Junções: {juncoes}')
        # print(f'Elevador: {elevador}')

        giratorios = [sentido[2] for sentido in sentidos_abert]
        adjacentes = [sentido[3] for sentido in sentidos_abert]
        sentidos = [sentido[4] for sentido in sentidos_abert]

        espessura_vidro = int(8)
        espessura_ext_perfil_U = int(20)
        carregar_comandos()

        # Linhas de centro
        pos_lcs = definir_linhas_de_centro(lcs, angs_in)
        sec_princ = descobrir_secao_principal(pos_lcs)
        pos_lcs, handles_lcs = redesenhar_linhas_de_centro(lcs, angs_in, sec_princ)
        coord_lcs = definir_coord_lcs(pos_lcs)
        # Início perfis U
        handles_perfis_U = offset_perfis_U(handles_lcs)
        fillet_perfis_U(handles_perfis_U)

        # Paredes
        parede_esq = fazer_parede_esq(pos_lcs[0], handles_perfis_U['externos'][0], handles_perfis_U['internos'][0], angs_paredes[0])
        fillet_paredes(handles_perfis_U['externos'][0], handles_perfis_U['internos'][0], parede_esq)

        parede_dir = fazer_parede_dir(pos_lcs[-1], handles_perfis_U['externos'][-1], handles_perfis_U['internos'][-1], angs_paredes[1])
        fillet_paredes(handles_perfis_U['externos'][-1], handles_perfis_U['internos'][-1], parede_dir)

        # Reajustando perfis U
        coord_perfis_U = definir_coord_perfis_U(handles_perfis_U)
        aberturas_por_lado = associar_aberturas_aos_lados(quant_vidros, sentidos_abert)
        medidas_perfis_U, coord_perfis_U = redefinir_coord_perfis_U(coord_perfis_U, aberturas_por_lado, elevador)

        # Ajustes de angulos de paredes
        gap_lcs_parede_esq, gap_cant_esq, necessidade_cant_esq = necessidade_cant_ajuste(angs_paredes[0], True)
        gap_lcs_parede_dir, gap_cant_dir, necessidade_cant_dir = necessidade_cant_ajuste(angs_paredes[1], False)

        gaps_lcs = [gap_lcs_parede_esq, gap_lcs_parede_dir]
        if necessidade_cant_esq is True:
            info_cant_esq = infos_cant_ajuste(gap_cant_esq)
            print(f'Info cant esq: {info_cant_esq}')
        if necessidade_cant_dir is True:
            info_cant_dir = infos_cant_ajuste(gap_cant_dir)
            print(f'Info cant dir: {info_cant_dir}')

        # Vidros
        folgas_vidros = definir_folgas_vidros(juncoes, gaps_lcs, angs_in, espessura_vidro)
        vidros = medida_dos_vidros(lcs, quant_vidros, folgas_vidros)
        pontos_vidros = pontos_dos_vidros(vidros, folgas_vidros)
        desenhar_guias_vidros(handles_lcs, vidros, pontos_vidros)
        handles_vidros, coord_vidros = offset_vidros(espessura_vidro)
        remover_guias()

        # Leitos
        folga_leitos = folgas_leitos(vidros, folgas_vidros, angs_in, sentidos_abert)
        handles_guias_leitos = desenhar_guias_leitos(handles_lcs, vidros, pontos_vidros, folga_leitos)
        handle_leitos, coord_leitos, medidas_leitos = desenhar_leitos(handles_guias_leitos, vidros, angs_in, giratorios, adjacentes, sentidos)
        remover_guias()

        # Furos
        coord_furos = definir_pontos_furos(coord_vidros, folgas_vidros, quant_vidros, angs_in, angs_paredes, espessura_vidro)

        # Drenos
        coord_drenos_por_lado, coord_drenos = definir_coord_drenos(coord_perfis_U, medidas_perfis_U, espessura_ext_perfil_U)

        #Cotas
        cotar_medida_total(coord_vidros, 'Vidro', 246)
        cotar_medida_total(coord_leitos, 'Leito', 386)
        cotar_medida_total(coord_lcs, 'Linha de centro', 550)
        cotar_medida_total(coord_perfis_U, 'Perfis U', 680)
        cotar_medida_total(coord_furos, 'Furos', 150)
        cotar_medida_total(coord_drenos, 'Drenos', 150)

        # Alturas
        dif_niveis, nivel_base = definir_niveis(niveis, lcs, quant_vidros, sentidos_abert)
        alturas_finais = alturas_por_nivel(alturas, dif_niveis)
        dif_altura, altura_base = diferenca_alturas(alturas_finais, lcs, quant_vidros, sentidos_abert)
        altura_vao = int(round(menor_valor(alturas_finais), 0) + altura_base - nivel_base)
        maior_altura = maior_valor(alturas)
        menor_altura = menor_valor(alturas)
        dif_superior, dif_inferior = definir_diferencas(dif_niveis, nivel_base, dif_altura, altura_base)
        folga_vidro = folga_altura_vidro(dif_superior, dif_inferior)
        altura_vidro = altura_vao - folga_vidro
        altura_painel = altura_vidro + 33
        altura_pe3 = altura_painel + 98

        # Definir sucata
        sucata_pedacos_inferior, sucata_inteira_inferior = necessidade_de_sucata(dif_niveis, lcs, 'nivel', nivel_base)
        sucata_pedacos_superior, sucata_inteira_superior = necessidade_de_sucata(dif_altura, lcs, 'altura', altura_base)
        sucata_pedacos = sucata_pedacos_inferior + sucata_pedacos_superior
        sucata_inteira = sucata_inteira_inferior + sucata_inteira_superior

        # print(f'{' - '*10}SUCATA{' - '*10}')
        # if sucata_pedacos > 0:
        #     print(f'A quantidade de sucata em pedaços necessária é {sucata_pedacos}, sendo {sucata_pedacos_inferior} para a parte inferior e {sucata_pedacos_superior} para a parte superior.')
        # else:
        #     print('Não é necessário sucata em pedaços.')
        # if sucata_inteira > 0:
        #     print(f'A quantidade de sucata inteira necessária é {sucata_inteira}, sendo {sucata_inteira_inferior} para a parte inferior e {sucata_inteira_superior} para a parte superior.')
        # else:
        #     print('Não é necessário sucata inteira.')
        # Pivos
        pivos = definir_pivos(quant_vidros, sentidos_abert, juncoes, medidas_perfis_U, pontos_vidros)
        print(f'Pivos: {pivos}')

        # Bocas
        medidas_bocas, quant_vidro_por_boca, pivos_individuais = definir_aberturas(sentidos_abert, vidros, pontos_vidros, pivos, quant_vidros, lcs)

        desenhar_pivos_individuais(pivos_individuais, pos_lcs, quant_vidros, sentidos_abert)

        desenhar_bocas(medidas_bocas, quant_vidro_por_boca, pos_lcs, quant_vidros, sentidos_abert)

        # Informacoes
        posicionar_alturas(pos_lcs, sec_princ, maior_altura, menor_altura, altura_vidro)
        posicionar_pivos(pos_lcs, sec_princ, pivos, giratorios)
        posicionar_angulos(coord_lcs, angs_in)

        # Perfis_extras
        quantidade_pe3 = calcular_quantidade_pe3(giratorios, quant_vidros)

        # Lista de ferragens e perfis_rolo
        dados_ferragens_perfis_rolo = {
            'juncoes': juncoes,
            'aberturas': sentidos_abert,
            'medidas_bocas': medidas_bocas,
            'giratorios': giratorios,
            'quantidade_vidros': quant_vidros,
            'medidas_perfis_U': medidas_perfis_U,
            'comprimento_pe3': altura_pe3,
            'quantidade_pe3' : quantidade_pe3,
            'vidros': vidros,
            'altura_vidros': altura_vidro,
            'medidas_leitos': medidas_leitos,
            'altura_pe3': altura_pe3
        }

        lista_ferragens = calcular_lista_ferragens(dados_ferragens_perfis_rolo)
        lista_perfis_rolo = calcular_lista_perfis_rolo(dados_ferragens_perfis_rolo, prumos)

        # print(f'Lista de ferragens: {lista_ferragens}')
        # print(f'Listagem de perfis: {lista_perfis_rolo}')

        dados_sacada = {
            'ordem_servico': ordem_servico,
            'aberturas': sentidos_abert,
            'giratorios': giratorios,
            'altura_vao': altura_vao,
            'altura_vidro': altura_vidro,
            'altura_painel': altura_painel,
            'altura_pe3': altura_pe3,
            'quantidade_vidros': sum(quant_vidros),
            'quantidade_pe3': quantidade_pe3,
            'sucata_pedacos': sucata_pedacos,
            'sucata_inteira': sucata_inteira,
        }

        cadastrar_sacada(dados_sacada, lista_ferragens, lista_perfis_rolo, vidros, altura_vidro)
        log_spev(f'Fim da execução ID: {id}')
        QMessageBox.information(None, "Finalizado", "A sacada foi desenhada no AutoCAD. Clique em OK para fechar esta janela.")

    except Exception as e:
        print(f'Erro: {e}')
        log_spev(f'Erro: {e} não rastreado - {traceback.format_exc()}')
        log_spev(f'Fim da execução ID: {id}')
        QMessageBox.critical(None, "Erro", "Ocorreu um erro. Feche esta janela para continuar.")

