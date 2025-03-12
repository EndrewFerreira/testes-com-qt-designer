from PyQt6 import QtWidgets, QtGui
import sys

class TelaQuartos(QtWidgets.QWidget):
    def __init__(self, quartos):
        super().__init__()
        self.setWindowTitle('Lista de Quartos')
        self.setGeometry(100, 100, 600, 400)
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)
        
        self.exibir_quartos(quartos)

    def exibir_quartos(self, quartos):
        for i, (numero, status) in enumerate(quartos):
            cor = 'green' if status == 'disponível' else 'red'
            btn_quarto = QtWidgets.QPushButton(f'Quarto {numero}')
            btn_quarto.setStyleSheet(f'background-color: {cor}; color: white; padding: 10px; border-radius: 5px;')
            btn_quarto.setFixedSize(120, 80)
            self.layout.addWidget(btn_quarto, i // 4, i % 4)

def abrir_tela_quartos():
    # Simulação de dados do banco: (número do quarto, status)
    dados_quartos = [
        (101, 'disponível'), (102, 'ocupado'), (103, 'disponível'), (104, 'ocupado'),
        (105, 'disponível'), (106, 'disponível'), (107, 'ocupado'), (108, 'disponível')
    ]
    tela = TelaQuartos(dados_quartos)
    tela.show()
    telas.append(tela)  # pra manter a referência e não fechar a janela

app = QtWidgets.QApplication(sys.argv)
janela = QtWidgets.QWidget()
layout = QtWidgets.QVBoxLayout(janela)

btn_listar_quartos = QtWidgets.QPushButton('Listar Quartos')
btn_listar_quartos.clicked.connect(abrir_tela_quartos)
layout.addWidget(btn_listar_quartos)

janela.setLayout(layout)
janela.show()

telas = []  # pra segurar as referências das janelas abertas
sys.exit(app.exec())
