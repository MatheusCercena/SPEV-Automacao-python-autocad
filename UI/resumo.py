from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QMessageBox
import json
from datetime import datetime

from src.logs import criar_alfanumerico
from src.main import projetar

class ResumoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.dados = {}

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(QLabel('RESUMO FINAL'))

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.layout().addWidget(self.text_edit)

        self.btn_export = QPushButton('Projetar')
        self.layout().addWidget(self.btn_export)
        self.btn_export.clicked.connect(self.exportar_json)

    def exportar_json(self):
        import os
        try:
            codigo_projeto = criar_alfanumerico()
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

            pasta_export = 'exportacoes'
            if not os.path.exists(pasta_export):
                os.makedirs(pasta_export)

            file_path = os.path.join(pasta_export, f'projeto_{codigo_projeto}_{timestamp}.json')

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.dados, f, indent=4, ensure_ascii=False)
            QMessageBox.information(self, 'Sucesso', f'Dados exportados para {file_path}')
        except Exception as e:
            print(f'Erro: {e}')
            QMessageBox.critical(self, 'Erro', f'Erro ao exportar dados: {e}')
            return
        projetar(self.dados, codigo_projeto)

    def atualizar_dados(self, dados):
        self.dados = dados
        dados_finais = json.dumps(dados, indent=4, ensure_ascii=False)

        texto_vaos = []
        quant_vaos = len(self.dados['linhas_centro']) if 'linhas_centro' in self.dados else 0

        for vao in range(quant_vaos):
            alturas_vao = self.dados['alturas'][vao] if 'alturas' in self.dados else []
            niveis_vao = self.dados['niveis'][vao] if 'niveis' in self.dados else []
            texto_vao = f'''
Vão {vao + 1}:
Linha de centro: {self.dados['linhas_centro'][vao] if 'linhas_centro' in self.dados else 0};
Quantidade de vidros: {self.dados['quantidade_vidros'][vao] if 'quantidade_vidros' in self.dados else 0};
Alturas: {alturas_vao};
Niveis: {niveis_vao};
{" - " *20}
'''
            texto_vaos.append(texto_vao)

        texto_juncoes = []
        for i in range(quant_vaos-1):
            texto_juncao = f'''
Junção entre vão {i + 1} e vão {i + 2}:
junção esquerda = {self.dados['juncoes'][i][1]};
junção direita = {self.dados['juncoes'][i + 1][0]};
{" - " *20}
'''
            texto_juncoes.append(texto_juncao)

        texto_angulos = []
        for i in range(len(self.dados['angulos_internos']) if 'angulos_internos' in self.dados else 0):
            texto_angulo = f'''
Ângulo entre vão {i + 1} e vão {i + 2}: {self.dados['angulos_internos'][i]}º
{" - " *20}
'''
            texto_angulos.append(texto_angulo)

        texto_aberturas = []
        for abertura in range(len(self.dados['aberturas']) if 'aberturas' in self.dados else 0):
            sentido = self.dados['aberturas'][abertura] if 'aberturas' in self.dados else [0, 0, 0, 0, 0]
            sentido_texto = f'''
Sentido de abertura {abertura+1}: começa no vidro {sentido[0]} e vai até o {sentido[1]}. Abertura para a {sentido[4]} (no vidro {sentido[2]}).
'''

            texto_aberturas.append(sentido_texto)

        texto = f'''
Dados Finais:

ORDEM DE SERVIÇO:
{self.dados['ordem_servico'] if 'ordem_servico' in self.dados else 'NÃO INFORMADO'}

VÃOS:
{''.join(texto_vaos)}

{f'''ANGULOS INTERNOS
 {''.join(texto_angulos)}
 ''' if quant_vaos > 1 else 'NENHUM ÂNGULO INTERNO'}

{f'''JUNCÕES ENTRE VÃOS
 {''.join(texto_juncoes)}
 ''' if quant_vaos > 1 else 'NENHUMA JUNÇÃO ENTRE VÃOS'}

ABERTURAS:
{''.join(texto_aberturas)}

ÂNGULOS PAREDES:
Ângulo parede esquerda: {self.dados['angulos_paredes'][0] if 'angulos_paredes' in self.dados else 0}º;
Ângulo parede direita: {self.dados['angulos_paredes'][1] if 'angulos_paredes' in self.dados else 0}º;

PRUMOS:
Prumo esquerdo: {self.dados['prumos'][0] if 'prumos' in self.dados else 0} mm;
Prumo direito: {self.dados['prumos'][1] if 'prumos' in self.dados else 0} mm;

ELEVADOR:
{self.dados['elevador'] if 'elevador' in self.dados else 0} mm

'''
        self.text_edit.setText(texto)
