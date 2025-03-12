from PyQt6 import uic, QtWidgets
from PyQt6.QtWidgets import QMessageBox
import mysql.connector

banco = mysql.connector.connect(
     host='localhost',
     user='root',
     passwd='#mortadela1507',
     database='bd_teste',
    auth_plugin='mysql_native_password'
)


# def entrar():
#     usuario = login.linha_usuario.text()
#     senha = login.linha_senha.text()
#     dados = (usuario,senha)
#     cursor = banco.cursor()
#     comando_SQL = "SELECT usuario from usuarios WHERE senha = %s"
#     cursor.execute(comando_SQL,dados)
#     banco.commit()
#     if usuario and senha == dados:
#         testeqt.show()

def entrar():
    usuario = login.linha_usuario.text()
    senha = login.linha_senha.text()

    cursor = banco.cursor()

    comando_SQL = "SELECT * FROM usuarios WHERE usuario = %s AND senha = %s"
    cursor.execute(comando_SQL, (usuario, senha))
    resultado = cursor.fetchone()  

    if resultado:  
        cadastro.show()
    else: 
        QMessageBox.warning(login, "Erro", "Usuário ou senha inválidos.")

    cursor.close()

def funcao_principal():
    linha_1 = cadastro.lineEdit.text()
    linha_2 = cadastro.lineEdit_2.text()
    linha_3 = cadastro.lineEdit_3.text()

    cursor = banco.cursor()
    comando_SQL = 'INSERT INTO clientes (nome, email, endereco) VALUES (%s, %s, %s)'
    dados = (str(linha_1), str(linha_2), str(linha_3))
    cursor.execute(comando_SQL, dados)
    banco.commit()

    cadastro.lineEdit.setText('')
    cadastro.lineEdit_2.setText('')
    cadastro.lineEdit_3.setText('')
    cadastro.show()

def listar_clientes():
    listarclientes.show()
    
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM clientes"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    listarclientes.tableWidget.setRowCount(len(dados_lidos))
    listarclientes.tableWidget.setColumnCount(4)

    for i in range(0,len(dados_lidos)):
        for j in range(0,4):
            listarclientes.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
    
def excluir_clientes():
    linha = listarclientes.tableWidget.currentRow()
    listarclientes.tableWidget.removeRow(linha)

    cursor = banco.cursor()
    cursor.execute('SELECT id_cliente FROM clientes')
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute('DELETE FROM clientes WHERE id_cliente=' + str(valor_id))
    banco.commit()

def editar_cliente():
    linha = listarclientes.tableWidget.currentRow()

    cursor = banco.cursor()
    cursor.execute('SELECT id_cliente FROM clientes')
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute('SELECT * FROM clientes WHERE id_cliente=' + str(valor_id))
    cliente = cursor.fetchall()
    editarclientes.show()

    editarclientes.linha_id.setText(str(cliente[0][0]))
    editarclientes.linha_nome.setText(str(cliente[0][1]))
    editarclientes.linha_email.setText(str(cliente[0][2]))
    editarclientes.linha_end.setText(str(cliente[0][3]))

def salvar_dados():
    id = editarclientes.linha_id.text()
    nome = editarclientes.linha_nome.text()
    email = editarclientes.linha_email.text()
    endereco = editarclientes.linha_end.text()

    cursor = banco.cursor()
    cursor.execute('UPDATE clientes SET nome = %s, email = %s, endereco = %s WHERE id_cliente = %s', (nome, email, endereco, id))
    banco.commit()

    msg = QMessageBox()
    msg.setIcon(QMessageBox.information)
    msg.setWindowTitle('SUCESSO')
    msg.setText('OS DADOS FORAM ATUALIZADOS COM SUCESSO!!!')
    msg.setStandardButtons(QMessageBox)
    msg.exec_()

    editarclientes.close()
    listarclientes.close()
    

    for i in range(0,len(dados_lidos)):
        for j in range(0,4):
            listarclientes.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

    linha = listarclientes.tableWidget.currentRow()
    if linha < 0:
        QtWidgets.QMessageBox.warning(listarclientes,'aviso, selecione um registro para editar')
        return
    
    id_cliente = listarclientes.tableWidget.item(linha, 0).text()
    nome = listarclientes.tableWidget.item(linha, 1).text()
    email = listarclientes.tableWidget.item(linha, 2).text()
    endereco = listarclientes.tableWidget.item(linha, 3).text()

    

app = QtWidgets.QApplication([])
login = uic.loadUi('TELA_LOGIN.ui')
cadastro = uic.loadUi('CADASTRO.ui')
listarclientes = uic.loadUi('LISTAR_CLIENTES.ui')
editarclientes = uic.loadUi('EDITAR_CLIENTES.ui')
cadastro.pushButton.clicked.connect(funcao_principal)
cadastro.pushButton_2.clicked.connect(listar_clientes)
listarclientes.pushButton.clicked.connect(excluir_clientes)
listarclientes.botao_editar.clicked.connect(editar_cliente)
editarclientes.botao_salvar.clicked.connect(salvar_dados)
login.botao_avancar.clicked.connect(entrar)


login.show()
app.exec()
