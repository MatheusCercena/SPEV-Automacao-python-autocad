from PyQt6.QtWidgets import QFrame, QLabel, QHBoxLayout, QScrollArea, QWidget, QVBoxLayout, QLineEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator, QRegularExpressionValidator
from PyQt6.QtCore import Qt, QRegularExpression

ALTURA_FIXA = 40
LARGURA_FIXA = 100

class linha_separadora(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Sunken)

class Ordem_Servico(QHBoxLayout):
    def __init__(self):
        super().__init__()
        regex = QRegularExpression(r"^\d{1,4}/\d{2}-\d{1,2}$")
        validador = QRegularExpressionValidator(regex)

        self.label = QLabel('Ordem de Serviço: ')
        self.label.setFixedWidth(LARGURA_FIXA*2)
        self.label.setFixedHeight(ALTURA_FIXA)
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.input = QLineEdit()
        self.input.setPlaceholderText('xxxx/xx-x')
        self.input.setFixedWidth(LARGURA_FIXA*2)
        self.input.setFixedHeight(ALTURA_FIXA)
        self.input.setValidator(validador)

        self.addWidget(self.label)
        self.addWidget(self.input)

class menu_etapas(QHBoxLayout):
    def __init__(self, ir_para_etapa_callback):
        super().__init__()
        etapas_nomes = ['Vãos', 'Sentidos de Abertura', 'Resumo']

        self.etapa_labels = []
        for i, nome in enumerate(etapas_nomes):
            label = QLabel(nome)
            label.setObjectName(f'etapa_{i}')
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.mousePressEvent = lambda event, idx=i: ir_para_etapa_callback(idx)
            label.setCursor(Qt.CursorShape.PointingHandCursor)
            self.etapa_labels.append(label)
            self.addWidget(label)
            if i < len(etapas_nomes) - 1:
                seta = QLabel('→')
                seta.setAlignment(Qt.AlignmentFlag.AlignCenter)
                seta.setStyleSheet('color: #888; font-size: 18px;')
                self.addWidget(seta)

    def atualizar_estado_menu_etapas(self, current_step):
        for i, label in enumerate(self.etapa_labels):
            if i == current_step:
                label.setStyleSheet('background: #d0eaff; border-radius: 6px; font-weight: bold; color: #005080; font-size: 16px; padding: 4px 8px;')
            else:
                label.setStyleSheet('color: #888; font-size: 14px; padding: 4px 8px;')

class scroll_area(QScrollArea):
    def __init__(self):
        super().__init__()
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.setWidget(self.scroll_widget)
        self.setWidgetResizable(True)

    def adicionar_item(self, vao_widget):
        self.scroll_layout.addWidget(vao_widget)

    def remover_item(self, vao_widget):
        self.scroll_layout.removeWidget(vao_widget)
        vao_widget.setParent(None)

class dados_extras(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.layout_esquerdo = QHBoxLayout()
        self.layout_central = QHBoxLayout()
        self.layout_direito = QHBoxLayout()

        self.lbl_prumos = QLabel('Prumo esquerdo:')
        self.lbl_prumos.setFixedWidth(LARGURA_FIXA)
        self.lbl_prumos.setFixedHeight(40)
        self.lbl_prumos.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.input_prumos = QLineEdit()
        self.input_prumos.setPlaceholderText('Prumo')
        self.input_prumos.setFixedWidth(LARGURA_FIXA)
        self.input_prumos.setFixedHeight(40)
        self.input_prumos.setValidator(QIntValidator(-999, 999))

        self.layout_esquerdo.addWidget(self.lbl_prumos)
        self.layout_esquerdo.addWidget(self.input_prumos)

        self.elevador = QLabel('Altura elevador:')
        self.elevador.setFixedWidth(LARGURA_FIXA*2)
        self.elevador.setFixedHeight(40)
        self.elevador.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.input_elevador = QLineEdit()
        self.input_elevador.setPlaceholderText('Elevador')
        self.input_elevador.setFixedWidth(LARGURA_FIXA)
        self.input_elevador.setFixedHeight(40)
        self.input_elevador.setValidator(QIntValidator(0, 9999))

        self.layout_central.addWidget(self.elevador)
        self.layout_central.addWidget(self.input_elevador)

        self.lbl_prumos_direito = QLabel('Prumo dir:')
        self.lbl_prumos_direito.setFixedWidth(LARGURA_FIXA)
        self.lbl_prumos_direito.setFixedHeight(40)
        self.lbl_prumos_direito.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.input_prumos_direito = QLineEdit()
        self.input_prumos_direito.setPlaceholderText('Prumo')
        self.input_prumos_direito.setFixedWidth(LARGURA_FIXA)
        self.input_prumos_direito.setFixedHeight(40)
        self.input_prumos_direito.setValidator(QIntValidator(-999, 999))

        self.layout_direito.addWidget(self.lbl_prumos_direito)
        self.layout_direito.addWidget(self.input_prumos_direito)

        self.addLayout(self.layout_esquerdo)
        self.addLayout(self.layout_central)
        self.addLayout(self.layout_direito)
