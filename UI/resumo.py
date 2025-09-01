from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QFileDialog, QMessageBox
import json

from src.logs import criar_alfanumerico
from src.main import projetar

class ResumoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(QLabel('RESUMO FINAL'))

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.layout().addWidget(self.text_edit)

        self.btn_export = QPushButton('Projetar')
        self.layout().addWidget(self.btn_export)
        self.btn_export.clicked.connect(self.exportar_json)

        self.dados = {}

    def atualizar_dados(self, dados):
        self.dados = dados
        dados_finais = json.dumps(dados, indent=4, ensure_ascii=False)

        texto_vaos = []
        quant_vaos = len(self.dados['linha_centro']) if 'linha_centro' in self.dados else 0

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
        for juncao in range(quant_vaos-1):
            texto_juncao = f'''
Junção entre vão {juncao + 1} e vão {juncao + 2}:
junção esquerda = {self.dados['juncao_esquerda'][juncao] if 'juncao_esquerda' in self.dados else 0} ;
junção direita = {self.dados['juncao_direita'][juncao]  if 'juncao_direita' in self.dados else 0};
{" - " *20}
'''
            texto_juncoes.append(texto_juncao)

        texto_angulos = []
        for angulo in range(len(self.dados['angulos_internos']) if 'angulos_internos' in self.dados else 0):
            texto_angulo = f'''
Ângulo entre vão {angulo + 1} e vão {angulo + 2}:
{" - " *20}
'''
            texto_angulos.append(texto_angulo)

        texto_angulos = []
        for angulo in range(len(self.dados['angulos_internos']) if 'angulos_internos' in self.dados else 0):
            texto_angulo = f'''
Ângulo entre vão {angulo + 1} e vão {angulo + 2}:
{" - " *20}
'''
            texto_angulos.append(texto_angulo)

        texto_aberturas = []
        for abertura in range(len(self.dados['aberturas']) if 'aberturas' in self.dados else 0):
            sentido = self.dados['aberturas'][abertura] if 'aberturas' in self.dados else [0, 0, 0, 0, 0]
            sentido_texto = f'''
Sentido de abertura {abertura+1}: começa no vidro {sentido[0]} e vai até o {sentido[1]}. Abertura para a {sentido[4]} (no vidro {sentido[2]}).\n
'''

            texto_aberturas.append(sentido_texto)

        texto = f'''
Dados Finais:

Vãos:
{''.join(texto_vaos)}

Angulo parede esquerda: {self.dados['angulos_paredes'][0] if 'angulos_paredes' in self.dados else 0}º;
Angulo parede direita: {self.dados['angulos_paredes'][1] if 'angulos_paredes' in self.dados else 0}º;

Angulos:
{''.join(texto_angulos)}

Juncoes:
{''.join(texto_juncoes)}

Prumo esquerdo = {self.dados['prumos'][0] if 'prumos' in self.dados else 0};
Prumo direito = {self.dados['prumos'][1] if 'prumos' in self.dados else 0};

Aberturas:
{''.join(texto_aberturas)}
'''
        self.text_edit.setText(texto)

    def exportar_json(self):
        codigo_projeto = criar_alfanumerico()
        if not self.dados:
            QMessageBox.warning(self, 'Erro', 'Nenhum dado para exportar.')
            return
        file_path = f'exportacoes\\projeto_{codigo_projeto}.json'
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.dados, f, indent=4, ensure_ascii=False)
            QMessageBox.information(self, 'Sucesso', f'Dados exportados para {file_path}')

        # projetar(file_path, codigo_projeto)