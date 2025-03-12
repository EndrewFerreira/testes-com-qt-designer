from PyQt6 import uic, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QLineEdit, QGridLayout, QPushButton
import pymysql, sys

# Conexão com o banco de dados
banco = pymysql.connect(
    host='localhost',
    user='root',
    passwd='',
    database='bd_teste'
)

# Função para cadastrar novo quarto
def cadastar_novo_quarto():
    numero_quarto = tl_quarto.linha_numero_quarto.text()
    tipo_quarto = tl_quarto.combo_tipo.currentText()
    status = tl_quarto.linha_status.text()
    preco = tl_quarto.linha_preco.text()
    capacidade = tl_quarto.linha_capacidade.text()
    descricao = tl_quarto.linha_desc.text()

    cursor = banco.cursor()
    comando_SQL = 'INSERT INTO quartos (NUMERO_QUARTO, TIPO_QUARTO, STATUS_QUARTO, VALOR_TIPO_QUARTO, CAPACIDADE_QUARTO, DESCRICAO_QUARTO) VALUES (%s,%s,%s,%s,%s,%s)'
    dados = (int(numero_quarto), str(tipo_quarto), str(status), int(preco), str(capacidade), str(descricao))
    cursor.execute(comando_SQL, dados)
    banco.commit()

    # Limpar campos após cadastro
    tl_quarto.linha_numero_quarto.clear()
    tl_quarto.linha_status.clear()
    tl_quarto.linha_preco.clear()
    tl_quarto.linha_capacidade.clear()
    tl_quarto.linha_desc.clear()

    QMessageBox.information(tl_quarto, "Sucesso", "Novo quarto registrado com sucesso!")

# Função para exibir quartos na página listar_quartos
def exibir_quartos():
    cursor = banco.cursor()
    cursor.execute('SELECT NUMERO_QUARTO, STATUS_QUARTO FROM quartos')
    dados_quartos = cursor.fetchall()

    # Configurar layout da página se necessário
    if not tl_quarto.page_listar_quartos.layout():
        grid_layout = QGridLayout()
        tl_quarto.page_listar_quartos.setLayout(grid_layout)
    else:
        grid_layout = tl_quarto.page_listar_quartos.layout()

    # Remover widgets antigos
    while grid_layout.count():
        item = grid_layout.takeAt(0)
        if item.widget():
            item.widget().deleteLater()

    # Adicionar botões de quartos
    for i, (numero, status) in enumerate(dados_quartos):
        cor = 'green' if status.lower() == 'disponível' else 'red'
        btn_quarto = QPushButton(f'Quarto {numero}')
        btn_quarto.setStyleSheet(f'background-color: {cor}; color: white; padding: 10px; border-radius: 5px;')
        btn_quarto.setFixedSize(120, 80)
        grid_layout.addWidget(btn_quarto, i // 4, i % 4)

    # Trocar para a página de listagem
    tl_quarto.stackedMenu.setCurrentWidget(tl_quarto.page_listar_quartos)

# Configurações principais
app = QtWidgets.QApplication(sys.argv)
tl_quarto = uic.loadUi("PROT_TELA_QUARTOS.ui")
tl_quarto.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
tl_quarto.showMaximized()  # Abre já maximizado


# Conectar botões às funções
tl_quarto.btn_cadastrar_quarto.clicked.connect(cadastar_novo_quarto)
tl_quarto.btn_listar_quartos.clicked.connect(exibir_quartos)
tl_quarto.btn_quartos.clicked.connect(lambda: tl_quarto.stackedMenu.setCurrentIndex(1))
tl_quarto.btn_novo_quarto.clicked.connect(lambda: tl_quarto.stackedWidget.setCurrentIndex(4))
tl_quarto.btn_voltar.clicked.connect(lambda: tl_quarto.stackedMenu.setCurrentIndex(0))

# Exibir a primeira tela
tl_quarto.show()
sys.exit(app.exec())
