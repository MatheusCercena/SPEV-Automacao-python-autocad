from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QDialog

from UI.elementos_main import scroll_area, dados_extras, Ordem_Servico
from UI.vao import VaoWidget

class VaosWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.vaos = []
        self.interface_vaos()

    def interface_vaos(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(4)
        layout.setContentsMargins(5, 5, 5, 5)

        self.ordem_servico = Ordem_Servico()

        self.titulo = QLabel('VÃOS')
        self.titulo.setStyleSheet('font-weight: bold; font-size: 18px; margin: 5px 0;')

        self.scroll_area = scroll_area()

        self.botao_adicionar_vao = QPushButton('Adicionar Vão')
        self.botao_adicionar_vao.clicked.connect(self.adicionar_vao)

        self.prumos_elevador = dados_extras()

        layout.addLayout(self.ordem_servico)
        layout.addWidget(self.titulo)
        layout.addWidget(self.scroll_area)
        layout.addWidget(self.botao_adicionar_vao)
        layout.addLayout(self.prumos_elevador)

        self.adicionar_vao()

    def adicionar_vao(self):
        numeracao_vao = len(self.vaos) + 1
        vao_widget = VaoWidget(numeracao_vao, self)
        self.vaos.append(vao_widget)
        self.scroll_area.adicionar_item(vao_widget)
        for i, vao in enumerate(self.vaos):
            if i < len(self.vaos) - 1:
                vao.juncoes_layout.juncao_dir.setEnabled(True)

    def remover_vao(self, numeracao_vao):
        for i, vao in enumerate(self.vaos):
            if i == numeracao_vao:
                self.scroll_area.remover_item(vao)
                self.vaos.pop(i)
                self.renomear_vaos()
                break

    def renomear_vaos(self):
        for i, vao_restante in enumerate(self.vaos):
            vao_restante.numeracao_vao = i + 1
            vao_restante.titulo.setText(f'VÃO {i + 1}')

    def checar_existencia_vaos(self):
        if len(self.vaos) == 0:
            dialog = QDialog(self)
            dialog.setWindowTitle("Campos não preenchidos")
            layout = QVBoxLayout()

            msg = "Adicione e prencha os dados de um vao antes de continuar."
            layout.addWidget(QLabel(msg))

            btn_ok = QPushButton("OK")
            btn_ok.clicked.connect(dialog.accept)
            layout.addWidget(btn_ok)

            dialog.setLayout(layout)
            dialog.exec()
            return False
        return True

    def get_dados_vaos(self):
        def get_ordem_servico():
            return self.ordem_servico.input.text() if self.ordem_servico.input.text() else None

        def get_linhas_centro():
            lcs = []
            for vao in self.vaos:
                dados_vao = vao.get_dados_vao()
                lcs.append(dados_vao['linha_centro'])
            return lcs

        def get_alturas():
            alturas = []
            for vao in self.vaos:
                dados_vao = vao.get_dados_vao()
                alturas.append(dados_vao['alturas'])
            return alturas

        def get_niveis():
            niveis = []
            for vao in self.vaos:
                dados_vao = vao.get_dados_vao()
                niveis.append(dados_vao['niveis'])
            return niveis

        def get_quantidade_vidros():
            quant_vidros = []
            for vao in self.vaos:
                dados_vao = vao.get_dados_vao()
                quant_vidros.append(dados_vao['quantidade_vidros'])
            return quant_vidros

        def get_angulos():
            angs_in = []
            angs_paredes = []

            for i, vao in enumerate(self.vaos):
                dados_vao = vao.get_dados_vao()
                if i == 0:
                    angs_paredes.append(90 - dados_vao['angulos'][0])
                if i < len(self.vaos) - 1 and len(self.vaos) > 0:
                    angs_in.append((180 - dados_vao['angulos'][1])*-1)
                if i == len(self.vaos) - 1:
                    angs_paredes.append(90 - dados_vao['angulos'][1])

            return angs_paredes, angs_in

        def get_juncoes():
            juncoes = []
            for vao in self.vaos:
                dados_vao = vao.get_dados_vao()
                juncoes.append(dados_vao['juncoes'])
            return juncoes

        def get_prumos():
            prumos = [0, 0]

            prumos[0] = int(self.prumos_elevador.input_prumos.text())
            prumos[1] = int(self.prumos_elevador.input_prumos_direito.text())

            return prumos

        def get_elevador():
            elevador = int(self.prumos_elevador.input_elevador.text())
            return elevador

        ordem_servico = get_ordem_servico()
        linhas_centro = get_linhas_centro()
        alturas = get_alturas()
        niveis = get_niveis()
        quant_vidros = get_quantidade_vidros()
        angulos_paredes, angulos_internos = get_angulos()
        juncoes = get_juncoes()
        prumos = get_prumos()
        elevador = get_elevador()

        dados = {
            'ordem_servico': ordem_servico,
            'linhas_centro': linhas_centro,
            'alturas': alturas,
            'niveis': niveis,
            'quantidade_vidros': quant_vidros,
            'angulos_paredes': angulos_paredes,
            'angulos_internos': angulos_internos,
            'juncoes': juncoes,
            'prumos': prumos,
            'elevador': elevador,
            'aberturas': ''
        }
        for dado in dados.values():
            if dado == None:
                return None

        return dados