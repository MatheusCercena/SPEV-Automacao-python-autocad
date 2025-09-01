from PyQt6.QtWidgets import QFrame, QLabel, QHBoxLayout, QScrollArea, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt

class linha_separadora(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Sunken)

class menu_etapas(QHBoxLayout):
    def __init__(self, etapas_nomes, ir_para_etapa_callback):
        super().__init__()
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
