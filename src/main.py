from src.aberturas import associar_aberturas_aos_lados
from src.adicionar_informacoes import posicionar_alturas, posicionar_pivos, posicionar_angulos
from src.alturas_niveis import definir_niveis, alturas_por_nivel, diferenca_alturas, folga_altura_vidro
from src.achar_secao_principal import descobrir_secao_principal
from src.bocas import definir_aberturas, desenhar_bocas, desenhar_pivos_individuais
from src.calcs_vetor import menor_valor, maior_valor
from src.cant_ajustes_angulo import necessidade_cant_ajuste, infos_cant_ajuste
from src.comandos_cad import carregar_comandos, remover_guias, adicionar_texto_modelspace, garantir_layer_ativa
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
from src.pivos import definir_pivos
from src.recebimento_da_medicao import pedir_linhas_de_centro, pedir_quant_vidros, pedir_angSecoes, pedir_angParedes, pedir_prumos, definir_juncoes, solicitar_sentido_abertura, pedir_elevador, pedir_alturas, pedir_niveis, converter_juncoes_valor
from src.sucata import necessidade_de_sucata, definir_diferencas
from src.scrapper.cadastrar_sacada import cadastrar_sacada
from src.vidros import offset_vidros, medida_dos_vidros, definir_folgas_vidros, pontos_dos_vidros, desenhar_guias_vidros

import traceback
from PyQt6.QtWidgets import QMessageBox

def projetar(dados, codigo_projeto):
    try:
        id = codigo_projeto
        log_spev(f'Inicio da execução ID: {id}')

        limpar_tudo()
        garantir_layer_ativa()

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

        # Definir sucata
        sucata_pedacos_inferior, sucata_inteira_inferior = necessidade_de_sucata(dif_niveis, lcs, 'nivel', nivel_base)
        sucata_pedacos_superior, sucata_inteira_superior = necessidade_de_sucata(dif_altura, lcs, 'altura', altura_base)
        sucata_pedacos = sucata_pedacos_inferior + sucata_pedacos_superior
        sucata_inteira = sucata_inteira_inferior + sucata_inteira_superior

        # Pivos
        pivos = definir_pivos(quant_vidros, sentidos_abert, juncoes, medidas_perfis_U, pontos_vidros)

        # Bocas
        medidas_bocas, quant_vidro_por_boca, pivos_individuais = definir_aberturas(sentidos_abert, vidros, pontos_vidros, pivos, quant_vidros, lcs)
        desenhar_pivos_individuais(pivos_individuais, pos_lcs, quant_vidros, sentidos_abert)
        desenhar_bocas(medidas_bocas, quant_vidro_por_boca, pos_lcs, quant_vidros, sentidos_abert)

        # Informacoes
        posicionar_alturas(pos_lcs, sec_princ, maior_altura, menor_altura, altura_vidro)
        posicionar_pivos(pos_lcs, sec_princ, pivos, giratorios)
        posicionar_angulos(coord_lcs, angs_in)

        # Lista de ferragens e perfis_rolo
        dados_ferragens_perfis_rolo = {
            'aberturas': sentidos_abert,
            'medidas_bocas': medidas_bocas,
            'giratorios': giratorios,
            'quantidade_vidros': quant_vidros,
            'medidas_perfis_U': medidas_perfis_U,
            'vidros': vidros,
            'altura_vidros': altura_vidro,
            'medidas_leitos': medidas_leitos,
            'angulos_internos' : angs_in
        }

        lista_ferragens = calcular_lista_ferragens(dados_ferragens_perfis_rolo)
        lista_perfis_rolo = calcular_lista_perfis_rolo(dados_ferragens_perfis_rolo, prumos)

        dados_sacada = {
            'ordem_servico': ordem_servico,
            'aberturas': sentidos_abert,
            'giratorios': giratorios,
            'altura_vao': altura_vao,
            'altura_vidro': altura_vidro,
            'altura_painel': altura_painel,
            'quantidade_vidros': sum(quant_vidros),
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
