from pathlib import Path
import sys, os

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QStackedWidget, QVBoxLayout

from UI.elementos_main import linha_separadora, menu_etapas
from UI.vaos import VaosWidget
from UI.sentidos_abertura import SentidosAberturaWidget
from UI.resumo import ResumoWidget
from src.main import projetar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dados_sacada = {}

        self.setWindowTitle('SPEV - SISTEMA PARA PROJETOS DE ENVIDRAÇAMENTO VERSATEEL')
        self.setGeometry(100, 100, 900, 700)
        self.showMaximized()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout_ = QVBoxLayout(self.central_widget)

        self.menu_etapas = menu_etapas(self.ir_para_etapa)
        self.separador = linha_separadora()
        self.stack = QStackedWidget()

        self.layout_.addLayout(self.menu_etapas)
        self.layout_.addWidget(self.separador)
        self.layout_.addWidget(self.stack)

        self.etapa_atual = 0
        self.iniciar_etapas()
        self.atualizar_estados()

    def iniciar_etapas(self):
        self.vaos_widget = VaosWidget()
        self.sentidos_widget = SentidosAberturaWidget(self)
        self.resumo_widget = ResumoWidget()

        self.etapas = [self.vaos_widget, self.sentidos_widget, self.resumo_widget]

        for widget in self.etapas:
            self.stack.addWidget(widget)

        self.stack.setCurrentIndex(0)

    def atualizar_estados(self):
        self.stack.setCurrentIndex(self.etapa_atual)
        self.menu_etapas.atualizar_estado_menu_etapas(self.etapa_atual)
        self.resumo_widget.atualizar_dados(self.dados_sacada)

    def ir_para_etapa(self, etapa_idx):
        """Navega diretamente para uma etapa específica"""
        if etapa_idx == self.etapa_atual:
            return
        if self.vaos_widget.checar_existencia_vaos() is False:
            return
        for vao in self.vaos_widget.vaos:
            validacao = vao.checar_campos_preenchidos()
            if not validacao:
                return
        self.etapa_atual = etapa_idx
        self.atualizar_dados()
        self.atualizar_estados()

    def atualizar_dados(self):
        dados_vaos = self.vaos_widget.get_dados_vaos()
        sentidos_abertura = self.sentidos_widget.sentidos
        dados_finais = dict(dados_vaos)
        dados_abertura = sentidos_abertura
        dados_finais['aberturas'] = dados_abertura
        self.dados_sacada = dados_finais
        self.sentidos_widget.atualizar_quant_vidros(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # projetar({}, 'TESTE')
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(__file__)

    qss_path = os.path.join(base_path, 'UI', 'styles.qss')
    app.setStyleSheet(Path(qss_path).read_text(encoding="utf-8"))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())