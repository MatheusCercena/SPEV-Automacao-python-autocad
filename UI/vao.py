from PyQt6.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator, QRegularExpressionValidator
from PyQt6.QtCore import Qt, QRegularExpression

from UI.vao_frame_widgets import HeaderLayout, LinhaCentroLayout, QuantidadeVidrosLayout, AngulosLayout, VaoFrame, Layout_Frame, JuncoesLayout, BotaoAdicionarAlturas, PrumosLayout
from UI.elementos_main import linha_separadora

regex = QRegularExpression(r"^(?:\d{1,2}(?:\.\d)?|1[0-7]\d(?:\.\d)?|179(?:\.[0-9])?)$")
validator = QRegularExpressionValidator(regex)

ALTURA_FIXA = 40
LARGURA_FIXA = 100

class VaoWidget(QWidget):
    def __init__(self, numeracao_vao, parent_widget):
        super().__init__()
        self.numeracao_vao = numeracao_vao
        self.parent_widget = parent_widget
        self.titulo = ''
        self.alturas = []
        self.niveis = []
        self.quant_vidros = []
        self.angs = []
        self.juncoes = []
        self.linha_layouts = []
        self.prumos = []

        self.interface_vao()

    def interface_vao(self):
        self.header_layout = HeaderLayout(self.numeracao_vao, self.remover_vao)
        self.titulo = self.header_layout.titulo_vao
        self.linhas_centro_layout = LinhaCentroLayout()
        self.quant_vidos_layout = QuantidadeVidrosLayout()
        self.angulos_layout = AngulosLayout(self)
        self.juncoes_layout = JuncoesLayout(self, self.parent_widget, self.numeracao_vao)
        self.prumos_layout = PrumosLayout()

        if self.numeracao_vao == 1 and len(self.parent_widget.vaos) == 0:
            self.prumos_layout.adicionar_completo()

        if self.numeracao_vao == 1 and len(self.parent_widget.vaos) > 0:
            self.prumos_layout.adicionar_a_esquerda()

        if self.numeracao_vao == len(self.parent_widget.vaos)+1:
            self.prumos_layout.adicionar_a_direita()

        for i, vao in enumerate(self.parent_widget.vaos):
            if i == 0 and len(self.parent_widget.vaos) > 0:
                while vao.prumos_layout.count():
                    item = vao.prumos_layout.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.setParent(None)
                vao.prumos_layout.adicionar_a_esquerda()
            if i > 0 and i < len(self.parent_widget.vaos):
                vao.vao_layout.removeItem(vao.prumos_layout)
                while vao.prumos_layout.count():
                    item = vao.prumos_layout.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.setParent(None)

        if self.numeracao_vao > 1:
            angulo_direito_anterior = self.parent_widget.vaos[self.numeracao_vao-2].angulos_layout.input_ang_dir.text()
            angulo_direito_anterior = float(angulo_direito_anterior) if angulo_direito_anterior else 0.0
            self.angulos_layout.input_ang_esq.setText(str(angulo_direito_anterior))

        self.botao_add_altura = BotaoAdicionarAlturas(self.adicionar_altura)
        self.alturas_container = QVBoxLayout()

        self.frame = Layout_Frame()

        self.vao_layout = VaoFrame()
        self.vao_layout.addLayout(self.header_layout)
        self.vao_layout.addLayout(self.linhas_centro_layout)
        self.vao_layout.addLayout(self.quant_vidos_layout)
        self.vao_layout.addLayout(self.angulos_layout)
        self.vao_layout.addLayout(self.juncoes_layout)
        self.vao_layout.addWidget(self.botao_add_altura)
        self.vao_layout.addLayout(self.alturas_container)
        self.vao_layout.addLayout(self.prumos_layout)

        self.frame.setLayout(self.vao_layout)

        self.separador = linha_separadora()
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.addWidget(self.frame, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.separador)
        self.ajustar_altura_frame()

    def remover_vao(self):
        self.parent_widget.remover_vao(self.numeracao_vao-1)

        # for i, vao in enumerate(self.parent_widget.vaos):
        #     if i == 0 and len(self.parent_widget.vaos) == 0:
        #         print("1")
        #         while vao.prumos_layout.count():
        #             item = vao.prumos_layout.takeAt(0)
        #             widget = item.widget()
        #             if widget is not None:
        #                 widget.setParent(None)
        #         self.prumos_layout.adicionar_completo()

        #     if i == 0 and len(self.parent_widget.vaos) > 0:
        #         print("2")
        #         while vao.prumos_layout.count():
        #             item = vao.prumos_layout.takeAt(0)
        #             widget = item.widget()
        #             if widget is not None:
        #                 widget.setParent(None)
        #         self.prumos_layout.adicionar_a_esquerda()

        #     if self.numeracao_vao == len(self.parent_widget.vaos)+1:
        #         print("3")
        #         while vao.prumos_layout.count():
        #             item = vao.prumos_layout.takeAt(0)
        #             widget = item.widget()
        #             if widget is not None:
        #                 widget.setParent(None)
        #         self.prumos_layout.adicionar_a_direita()

        #     if i > 0 and i < len(self.parent_widget.vaos):
        #         print("4")
        #         vao.vao_layout.removeItem(vao.prumos_layout)
        #         while vao.prumos_layout.count():
        #             item = vao.prumos_layout.takeAt(0)
        #             widget = item.widget()
        #             if widget is not None:
        #                 widget.setParent(None)


    def adicionar_altura(self):
        altura_idx = len(self.alturas)

        lbl_altura = QLabel(f'Altura {altura_idx + 1}:')
        lbl_altura.setFixedWidth(LARGURA_FIXA)
        lbl_altura.setFixedHeight(ALTURA_FIXA)
        lbl_altura.setAlignment(Qt.AlignmentFlag.AlignCenter)

        input_altura = QLineEdit()
        input_altura.setPlaceholderText('Digite a altura')
        input_altura.setFixedWidth(LARGURA_FIXA*2)
        input_altura.setFixedHeight(ALTURA_FIXA)
        input_altura.setValidator(QIntValidator(0, 4000))

        lbl_nivel = QLabel('Nível:')
        lbl_nivel.setFixedWidth(LARGURA_FIXA)
        lbl_nivel.setFixedHeight(ALTURA_FIXA)
        lbl_nivel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        input_nivel = QLineEdit()
        input_nivel.setPlaceholderText('Digite o nível')
        input_nivel.setFixedWidth(LARGURA_FIXA*2)
        input_nivel.setFixedHeight(ALTURA_FIXA)
        input_nivel.setValidator(QIntValidator(0, 4000))

        btn_remove = QPushButton('×')
        btn_remove.setFixedHeight(ALTURA_FIXA)
        btn_remove.setFixedWidth(ALTURA_FIXA)
        btn_remove.setStyleSheet('''
            QPushButton {background-color: #ff4444; color: white; border: 1px solid red; border-radius: 15px; font-weight: bold;font-size: 14px;}
            QPushButton:hover {background-color: #ff6666;}''')
        btn_remove.clicked.connect(lambda: self.remover_altura(altura_idx))

        linha_layout = QHBoxLayout()
        linha_layout.setSpacing(5)
        linha_layout.setContentsMargins(2, 2, 2, 2)
        linha_layout.addWidget(lbl_altura)
        linha_layout.addWidget(input_altura)
        linha_layout.addWidget(lbl_nivel)
        linha_layout.addWidget(input_nivel)
        linha_layout.addWidget(btn_remove)

        self.alturas_container.addLayout(linha_layout)

        self.alturas.append(input_altura)
        self.niveis.append(input_nivel)
        self.linha_layouts.append((linha_layout, lbl_altura))

        self.vao_layout.removeWidget(self.botao_add_altura)
        self.vao_layout.addWidget(self.botao_add_altura)

        self.ajustar_altura_frame()

    def remover_altura(self, idx):
        if idx < len(self.linha_layouts):
            linha_layout  = self.linha_layouts[idx][0]
            while linha_layout.count() > 0:
                item = linha_layout.takeAt(0)
                if item.widget():
                    item.widget().setParent(None)

            self.alturas_container.removeItem(linha_layout)

            self.alturas.pop(idx)
            self.niveis.pop(idx)
            self.linha_layouts.pop(idx)

            for i, (layout, lbl) in enumerate(self.linha_layouts):
                lbl.setText(f'Altura {i + 1}:')

            self.ajustar_altura_frame()

    def ajustar_altura_frame(self):
        """Ajusta a altura mínima do frame baseado no conteúdo"""
        altura_base = 300
        altura_por_linha = 50
        altura_total = altura_base + (len(self.alturas) * altura_por_linha)
        if altura_total < 400:
            altura_total = 400
        self.frame.setMinimumHeight(altura_total)

    def sincronizar_angulos(self):
        ang_dir = self.angulos_layout.input_ang_dir.text()
        if self.numeracao_vao < len(self.parent_widget.vaos):
            proximo_vao = self.parent_widget.vaos[self.numeracao_vao]

            proximo_vao.angulos_layout.input_ang_esq.setText(ang_dir)
            proximo_vao.angulos_layout.input_ang_esq.setEnabled(False)

    def checar_campos_preenchidos(self) -> bool:
        """
        Verifica se todos os QLineEdit do vão foram preenchidos.
        Se algum estiver vazio, abre um QDialog informando quais campos faltam.

        Returns:
            bool: True se todos preenchidos, False se algum estiver vazio.
        """
        campos_vazios = []

        if not self.linhas_centro_layout.input_lc.text():
            campos_vazios.append(f"Linha de Centro vão {self.numeracao_vao}")

        if not self.quant_vidos_layout.input_quant_vidros.text():
            campos_vazios.append(f"Quantidade de Vidros vão {self.numeracao_vao}")

        if len(self.alturas) == 0:
            campos_vazios.append(f"Alturas vão {self.numeracao_vao}")

        if len(self.niveis) == 0:
            campos_vazios.append(f"Níveis vão {self.numeracao_vao}")

        for idx, altura in enumerate(self.alturas):
            if not altura.text():
                campos_vazios.append(f"Altura {idx+1} vão {self.numeracao_vao}")

        for idx, nivel in enumerate(self.niveis):
            if not nivel.text():
                campos_vazios.append(f"Nível {idx+1} vão {self.numeracao_vao}")

        if not self.angulos_layout.input_ang_esq.text():
            campos_vazios.append(f"Ângulo Esquerdo vão {self.numeracao_vao}")

        if self.prumos_layout and not self.prumos_layout.input_prumos.text():
            campos_vazios.append(f"Prumo {'parede esquerda.' if self.numeracao_vao == 1 else 'parede direita.'} vão {self.numeracao_vao}")

        if campos_vazios:
            dialog = QDialog(self)
            dialog.setWindowTitle("Campos não preenchidos")
            layout = QVBoxLayout()

            msg = "Os seguintes campos não foram preenchidos:\n\n" + "\n".join(campos_vazios)
            layout.addWidget(QLabel(msg))

            btn_ok = QPushButton("OK")
            btn_ok.clicked.connect(dialog.accept)
            layout.addWidget(btn_ok)

            dialog.setLayout(layout)
            dialog.exec()

            return False
        return True

    def get_dados_vao(self):
        lc = int(self.linhas_centro_layout.input_lc.text())
        qv = int(self.quant_vidos_layout.input_quant_vidros.text())
        ang_esq = float(self.angulos_layout.input_ang_esq.text())
        ang_dir = float(self.angulos_layout.input_ang_dir.text())
        angulos = [ang_esq, ang_dir]
        alturas = []
        niveis = []
        juncao_esq = self.juncoes_layout.juncao_esq.currentText()
        juncao_dir = self.juncoes_layout.juncao_dir.currentText()
        juncoes = [juncao_esq, juncao_dir]
        prumo = [0, 0]
        if self.prumos_layout:
            if self.prumos_layout.input_prumos.text() and self.prumos_layout.input_prumos_direito.text():
                prumo[0] = int(self.prumos_layout.input_prumos.text())
                prumo[1] = int(self.prumos_layout.input_prumos_direito.text())
            elif self.prumos_layout.input_prumos.text():
                prumo[0] = int(self.prumos_layout.input_prumos.text())
            else:
                prumo[1] = int(self.prumos_layout.input_prumos_direito.text())

        for altura, nivel in zip(self.alturas, self.niveis):
            if altura.text() and nivel.text():
                altura = int(altura.text())
                nivel = int(nivel.text())
                alturas.append(altura)
                niveis.append(nivel)

        return {
            'linha_centro': lc,
            'quantidade_vidros': qv,
            'alturas': alturas,
            'niveis': niveis,
            'angulos': angulos,
            'juncoes': juncoes,
            'prumos': prumo
        }