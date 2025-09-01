from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QFrame, QSizePolicy, QComboBox
from PyQt6.QtCore import Qt, QRegularExpression
from PyQt6.QtGui import QIntValidator, QRegularExpressionValidator, QStandardItemModel, QStandardItem

regex = QRegularExpression(r"^-?(?:[0-9]{1,2}|[1-2][0-9]{2}|3[0-5][0-9]|360)(?:\\.[0-9])?$")
validator = QRegularExpressionValidator(regex)

ALTURA_FIXA = 40
LARGURA_FIXA = 100

class HeaderLayout(QHBoxLayout):
    def __init__(self, numeracao_vao, funcao_remover):
        super().__init__()
        self.titulo_vao = QLabel(f'VÃO {numeracao_vao}')
        self.titulo_vao.setObjectName("TituloVao")
        self.titulo_vao.setFixedHeight(ALTURA_FIXA)

        botao_remover_vao = QPushButton('×')
        botao_remover_vao.setFixedHeight(ALTURA_FIXA)
        botao_remover_vao.setFixedWidth(ALTURA_FIXA)
        botao_remover_vao.setObjectName("btnRemoveVao")
        botao_remover_vao.clicked.connect(funcao_remover)

        self.addWidget(self.titulo_vao)
        self.addWidget(botao_remover_vao)

class LinhaCentroLayout(QHBoxLayout):
    def __init__(self):
        super().__init__()
        lbl_lc = QLabel('Linha de Centro:')
        lbl_lc.setFixedWidth(LARGURA_FIXA*3)
        lbl_lc.setFixedHeight(40)
        lbl_lc.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.input_lc = QLineEdit()
        self.input_lc.setPlaceholderText('Digite a linha de centro')
        self.input_lc.setFixedWidth(LARGURA_FIXA*3)
        self.input_lc.setFixedHeight(40)
        self.input_lc.setValidator(QIntValidator(0, 99999))

        self.addWidget(lbl_lc)
        self.addWidget(self.input_lc)

class QuantidadeVidrosLayout(QHBoxLayout):
    def __init__(self):
        super().__init__()
        lbl_quant_vidros = QLabel('Quantidade de Vidros:')
        lbl_quant_vidros.setFixedWidth(LARGURA_FIXA*3)
        lbl_quant_vidros.setFixedHeight(40)
        lbl_quant_vidros.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.input_quant_vidros = QLineEdit()
        self.input_quant_vidros.setPlaceholderText('Digite a quantidade de vidros')
        self.input_quant_vidros.setFixedWidth(LARGURA_FIXA*3)
        self.input_quant_vidros.setFixedHeight(40)
        self.input_quant_vidros.setValidator(QIntValidator(0, 99))

        self.addWidget(lbl_quant_vidros)
        self.addWidget(self.input_quant_vidros)

class AngulosLayout(QHBoxLayout):
    def __init__(self, vao_widget):
        super().__init__()
        lbl_ang_esq = QLabel('Ângulo esquerdo:')
        lbl_ang_esq.setFixedWidth(LARGURA_FIXA*2)
        lbl_ang_esq.setFixedHeight(40)
        lbl_ang_esq.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.input_ang_esq = QLineEdit()
        self.input_ang_esq.setPlaceholderText('Ângulo')
        self.input_ang_esq.setFixedWidth(LARGURA_FIXA*2)
        self.input_ang_esq.setFixedHeight(40)
        self.input_ang_esq.setValidator(validator)

        lbl_ang_dir = QLabel('Ângulo direito:')
        lbl_ang_dir.setFixedWidth(LARGURA_FIXA*2)
        lbl_ang_dir.setFixedHeight(40)
        lbl_ang_dir.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.input_ang_dir = QLineEdit()
        self.input_ang_dir.setPlaceholderText('Ângulo')
        self.input_ang_dir.setFixedWidth(LARGURA_FIXA*2)
        self.input_ang_dir.setFixedHeight(40)
        self.input_ang_dir.setValidator(validator)
        self.input_ang_dir.textChanged.connect(vao_widget.sincronizar_angulos)

        self.addWidget(lbl_ang_esq)
        self.addWidget(self.input_ang_esq)
        self.addWidget(lbl_ang_dir)
        self.addWidget(self.input_ang_dir)

class ComboSemScroll(QComboBox):
    def wheelEvent(self, event):
        event.ignore()

class JuncoesLayout(QHBoxLayout):
    def __init__(self, vao_widget, vaos_widget, vao_num):
        super().__init__()
        self.vaos_widget = vaos_widget
        self.vao_widget = vao_widget
        self.vao_num = vao_num

        opcoes_juncoes = ['Vidro/Parede', 'Vidro/Vidro', 'Passante', 'Colante']

        self.juncao_esq = ComboSemScroll()
        self.juncao_esq.setFixedWidth(LARGURA_FIXA*2)
        self.juncao_esq.setFixedHeight(40)
        self.juncao_esq.addItems(opcoes_juncoes)
        self.juncao_esq.currentIndexChanged.connect(self.alterar_juncao_dir)

        self.juncao_dir = ComboSemScroll()
        self.juncao_dir.setFixedWidth(LARGURA_FIXA*2)
        self.juncao_dir.setFixedHeight(40)
        self.juncao_dir.addItems(opcoes_juncoes)
        self.juncao_dir.currentIndexChanged.connect(self.alterar_juncao_esq)

        self.addWidget(self.juncao_esq)
        self.addWidget(self.juncao_dir)

    def alterar_juncao_esq(self):
        index_direito = self.juncao_dir.currentIndex()
        if len(self.vaos_widget.vaos) > 1 and self.vao_num < len(self.vaos_widget.vaos) :
            if index_direito == 2:
                self.vaos_widget.vaos[self.vao_num].juncoes_layout.juncao_esq.setCurrentIndex(3)
            elif index_direito == 3:
                self.vaos_widget.vaos[self.vao_num].juncoes_layout.juncao_esq.setCurrentIndex(2)
            else:
                self.vaos_widget.vaos[self.vao_num].juncoes_layout.juncao_esq.setCurrentIndex(index_direito)

    def alterar_juncao_dir(self):
        index_esquerdo = self.juncao_esq.currentIndex()
        if len(self.vaos_widget.vaos) > 1:
            if index_esquerdo == 2:
                self.vaos_widget.vaos[self.vao_num-2].juncoes_layout.juncao_dir.setCurrentIndex(3)
            elif index_esquerdo == 3:
                self.vaos_widget.vaos[self.vao_num-2].juncoes_layout.juncao_dir.setCurrentIndex(2)
            else:
                self.vaos_widget.vaos[self.vao_num-2].juncoes_layout.juncao_dir.setCurrentIndex(index_esquerdo)

class Layout_Frame(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameStyle(QFrame.Shape.Box)
        self.setStyleSheet('border: 1px solid #ddd; border-radius: 4px; padding: 5px; margin: 2px;')
        self.setMinimumHeight(300)
        self.setFixedWidth(850)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

class VaoFrame(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.setSpacing(4)
        self.setContentsMargins(5, 5, 5, 5)

class BotaoAdicionarAlturas(QPushButton):
    def __init__(self, funcao_adicionar_altura):
        super().__init__('Adicionar altura')
        self.clicked.connect(funcao_adicionar_altura)

class PrumosLayout(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.lbl_prumos = QLabel('Prumo:')
        self.lbl_prumos.setFixedWidth(LARGURA_FIXA)
        self.lbl_prumos.setFixedHeight(40)
        self.lbl_prumos.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.input_prumos = QLineEdit()
        self.input_prumos.setPlaceholderText('Prumo')
        self.input_prumos.setFixedWidth(LARGURA_FIXA)
        self.input_prumos.setFixedHeight(40)
        self.input_prumos.setValidator(QIntValidator(0, 999))

        self.lbl_prumos_direito = QLabel('Prumo:')
        self.lbl_prumos_direito.setFixedWidth(LARGURA_FIXA)
        self.lbl_prumos_direito.setFixedHeight(40)
        self.lbl_prumos_direito.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.input_prumos_direito = QLineEdit()
        self.input_prumos_direito.setPlaceholderText('Prumo')
        self.input_prumos_direito.setFixedWidth(LARGURA_FIXA)
        self.input_prumos_direito.setFixedHeight(40)
        self.input_prumos_direito.setValidator(QIntValidator(0, 999))

    def adicionar_a_esquerda(self):
        self.addWidget(self.lbl_prumos)
        self.addWidget(self.input_prumos)
        self.addStretch()

    def adicionar_a_direita(self):
        self.addStretch()
        self.addWidget(self.lbl_prumos_direito)
        self.addWidget(self.input_prumos_direito)

    def adicionar_completo(self):
        self.addWidget(self.lbl_prumos)
        self.addWidget(self.input_prumos)
        self.addWidget(self.lbl_prumos_direito)
        self.addWidget(self.input_prumos_direito)
