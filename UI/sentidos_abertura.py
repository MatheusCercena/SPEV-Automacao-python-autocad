from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox, QHBoxLayout, QComboBox, QDialog
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator


regex = QRegularExpression(r"^(?:[1-9]|[1-9][0-9])$")
validador = QRegularExpressionValidator(regex)

class SentidosAberturaWidget(QWidget):
    def __init__(self, parent_vaos):
        super().__init__()
        self.vidros_moveis = []
        self.parent_vaos = parent_vaos
        self.setObjectName('sentidosAberturaElementos')
        self.quant_vidros = self.definir_quant_vidros()
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(QLabel('SENTIDOS DE ABERTURA'))

        self.lbl_ini = QLabel('Vidro início')
        self.layout().addWidget(self.lbl_ini)
        self.input_ini = QLineEdit()
        self.input_ini.setPlaceholderText('Vidro início')
        self.input_ini.setValidator(validador)
        self.layout().addWidget(self.input_ini)

        self.lbl_fim = QLabel('Vidro fim')
        self.layout().addWidget(self.lbl_fim)
        self.input_fim = QLineEdit()
        self.input_fim.setPlaceholderText('Vidro fim')
        self.input_fim.setValidator(validador)
        self.layout().addWidget(self.input_fim)

        self.lbl_sentido = QLabel('Sentido')
        self.layout().addWidget(self.lbl_sentido)
        self.combo_sentido = QComboBox()
        self.combo_sentido.addItems(['direita', 'esquerda'])
        self.layout().addWidget(self.combo_sentido)

        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton('Adicionar')
        self.btn_remove = QPushButton('Remover Selecionado')
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_remove)
        self.layout().addLayout(btn_layout)

        self.list_widget = QListWidget()
        self.list_widget.setDragDropMode(QListWidget.DragDropMode.NoDragDrop)
        self.layout().addWidget(self.list_widget)

        self.btn_add.clicked.connect(self.add_sentido)
        self.btn_remove.clicked.connect(self.remove_sentido)

        self.sentidos = []
        self.sentidos_visualizacao = []
        self.update_list()

    def definir_quant_vidros(self):
        if self.parent_vaos.vaos_widget.vaos and len(self.parent_vaos.vaos_widget.vaos) > 1:
            self.quant_vidros = sum(self.parent_vaos.vaos_widget.dados_sacada['quantidade_vidros'])
        else:
            self.quant_vidros = 0

    def atualizar_quant_vidros(self, pai):
        self.quant_vidros = sum(pai.dados_sacada['quantidade_vidros']) if len(pai.dados_sacada) > 0 else [0]

    def add_sentido(self):
        try:
            self.v_ini = int(self.input_ini.text())
            self.v_fim = int(self.input_fim.text())

            validacao_ini = self.validar_v_ini()
            if validacao_ini == False:
                return
            validacao_fim = self.validar_v_fim()
            if validacao_fim == False:
                return
            self.validar_v_fim()
            sentido = self.combo_sentido.currentText()
            giratorio = int(self.v_ini if sentido == 'esquerda' else self.v_fim)
            adjacente = int(giratorio + 1 if sentido == 'esquerda' else giratorio - 1)
            [self.vidros_moveis.append(vidro) for vidro in range(self.v_ini, self.v_fim+1)]
        except ValueError:
            QMessageBox.warning(self, 'Erro', 'Todos os campos devem ser preenchidos corretamente.')
            return
        sentido = [self.v_ini, self.v_fim, giratorio, adjacente, sentido]
        self.sentidos.append(sentido)
        sentido_texto = f'Sentido de abertura {len(self.sentidos)}: começa no vidro {sentido[0]} e vai até o {sentido[1]}. Abertura para a {sentido[4]} (no vidro {sentido[2]}).'
        self.sentidos_visualizacao.append(sentido_texto)
        self.input_ini.clear()
        self.input_fim.clear()
        self.update_list()

    def remove_sentido(self):
        for item in self.list_widget.selectedItems():
            idx = self.list_widget.row(item)
            self.sentidos.pop(idx)
            self.sentidos_visualizacao.pop(idx)
        self.update_list()

    def update_list(self):
        self.list_widget.clear()
        for s in self.sentidos_visualizacao:
            self.list_widget.addItem(str(s))

    def get_sentidos(self):
        return self.sentidos

    def dialogo(self, texto):
        dialog = QDialog(self)
        dialog.setWindowTitle("Dados invalidos")
        layout = QVBoxLayout()

        layout.addWidget(QLabel(texto))

        btn_ok = QPushButton("OK")
        btn_ok.clicked.connect(dialog.accept)
        layout.addWidget(btn_ok)

        dialog.setLayout(layout)
        dialog.exec()

    def validar_v_ini(self):
        if self.v_ini > self.quant_vidros:
            self.dialogo(f'A sacada tem menos que {self.v_ini} vidros. Escolha um vidro existente na sacada.')
            return False
        elif self.v_ini < 1:
            self.dialogo(f'O vidro inicial é menor que 1.')
            return False
        elif self.v_ini in self.vidros_moveis:
            self.dialogo(f'O vidro {self.v_ini} já abre em outro lugar.')
            return False
        elif self.v_ini > self.v_fim:
            self.dialogo('O vidro inicial da abertura precisa ser menor ou igual ao final.')
            return False
        return True

    def validar_v_fim(self):
        if self.v_fim > self.quant_vidros:
            self.dialogo(f'A sacada tem menos que {self.v_fim} vidros. Escolha um vidro existente na sacada.')
            return False
        elif self.v_fim in self.vidros_moveis or self.v_fim == 0:
            self.dialogo(f'O vidro {self.v_fim} já abre em outro lugar ou é inválido.')
            return False
        elif self.v_fim < self.v_ini:
            self.dialogo('O vidro final da abertura precisa ser maior ou igua o final.')
            return False
        return True