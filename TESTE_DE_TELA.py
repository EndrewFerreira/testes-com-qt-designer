from PyQt6 import uic,QtWidgets
import mysql.connector

banco = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = '#mortadela1507',
    database = 'bd_teste',
    auth_plugin='mysql_native_password'  # força o uso do plugin certo
)

def entrar():
    usuario = tl_LOGIN.linha_usuario.text()
    senha = tl_LOGIN.linha_senha.text()

    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM usuarios WHERE usuario = %s AND SENHA = %s"
    cursor.execute(comando_SQL,(usuario, senha))
    login_CORRETO = cursor.fetchone()

    if login_CORRETO:
        QtWidgets.QMessageBox.information(tl_LOGIN, 'Sucesso', 'Login bem-sucedido!')
        tl_CADASTRO.show()
        tl_LOGIN.close()
    else:
        QtWidgets.QMessageBox.warning(tl_LOGIN, 'Atenção', 'Usuário ou senha Incorretos!')
    cursor.close()


def cadastrar_clientes():
    linha_nome = tl_CADASTRO.ln_nome.text()
    linha_email = tl_CADASTRO.ln_email.text()
    linha_endereco = tl_CADASTRO.ln_end.text()

    cursor = banco.cursor()
    comando_SQL = 'INSERT INTO clientes (nome, email, endereco) VALUES (%s,%s,%s)'
    dados = (str(linha_nome),str(linha_email),str(linha_endereco))
    cursor.execute(comando_SQL,dados)
    banco.commit()


    tl_CADASTRO.ln_nome.setText('')
    tl_CADASTRO.ln_email.setText('')
    tl_CADASTRO.ln_end.setText('')

    msg = QtWidgets.QMessageBox()
    msg.setWindowTitle('Sucesso')
    msg.setText('Cliente cadastrado com sucesso!')
    msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
    msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
    msg.exec()
    return

def listar_clientes():
    cursor = banco.cursor()
    comando_SQL = 'SELECT * FROM clientes' # faz consulta no banco
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    tl_LISTA_CLIENTES.tabela_dados.setRowCount(len(dados_lidos))  
    tl_LISTA_CLIENTES.tabela_dados.setColumnCount(4)

    for i in range(0,len(dados_lidos)):
        for j in range(0,len(dados_lidos[i])):
            tl_LISTA_CLIENTES.tabela_dados.setItem(i,j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j]))) # mostra na tabela
    tl_LISTA_CLIENTES.tabela_dados.clearSelection()
    tl_LISTA_CLIENTES.show()

    # Remove seleção automática e o foco da primeira linha
    tl_LISTA_CLIENTES.tabela_dados.clearSelection()
    tl_LISTA_CLIENTES.tabela_dados.setCurrentItem(None)

def deletar_cliente():
    linha_selecionada = tl_LISTA_CLIENTES.tabela_dados.currentRow()
    tl_LISTA_CLIENTES.tabela_dados.removeRow(linha_selecionada)

    cursor = banco.cursor()
    cursor.execute('SELECT id_cliente FROM clientes')
    dados_lidos = cursor.fetchall(

    )
    numero_id = dados_lidos[linha_selecionada][0]
    comando_SQL = 'DELETE FROM clientes WHERE id_cliente = %s' 
    cursor.execute(comando_SQL, (numero_id,))
    banco.commit()

# def editar_registro():
#     linha_selecionada = tl_LISTA_CLIENTES.tabela_dados.currentRow()
    
    if linha_selecionada == -1:
        msg = QtWidgets.QMessageBox(tl_LISTA_CLIENTES)
        msg.setWindowTitle('Aviso')
        msg.setText('Selecione um registro para DELETAR.')
        msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        msg.exec()
        return
#     cursor = banco.cursor()
#     cursor.execute('SELECT id_cliente FROM clientes')
#     dados_lidos = cursor.fetchall()
#     numero_id = dados_lidos[linha_selecionada][0]
#     cursor.execute('SELECT * FROM clientes WHERE id_cliente = %s', (numero_id,))
#     cliente = cursor.fetchone()

#     if cliente:
#         tl_EDITAR_CLIENTE.linha_id.setText(str(cliente[0]))
#         tl_EDITAR_CLIENTE.linha_nome.setText(cliente[1])
#         tl_EDITAR_CLIENTE.linha_email.setText(cliente[2])
#         tl_EDITAR_CLIENTE.linha_end.setText(cliente[3])

#     tl_EDITAR_CLIENTE.show()

    msg = QtWidgets.QMessageBox()
    msg.setWindowTitle('Sucesso')
    msg.setText('O registro foi DELETADO com sucesso!')
    msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
    msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
    msg.exec()
def editar_registro():
    
    linha_selecionada = tl_LISTA_CLIENTES.tabela_dados.currentRow()
    print(f'Linha selecionada: {linha_selecionada}')  # Diagnóstico
    
    if linha_selecionada == -1:
        msg = QtWidgets.QMessageBox(tl_LISTA_CLIENTES)
        msg.setWindowTitle('Aviso')
        msg.setText('Selecione um registro para EDITAR.')
        msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        msg.exec()
        return
    
    cursor = banco.cursor()
    cursor.execute('SELECT id_cliente FROM clientes')
    dados_lidos = cursor.fetchall()
    numero_id = dados_lidos[linha_selecionada][0]
    cursor.execute('SELECT * FROM clientes WHERE id_cliente = %s', (numero_id,))
    cliente = cursor.fetchone()

    if cliente:
        tl_EDITAR_CLIENTE.linha_id.setText(str(cliente[0]))
        tl_EDITAR_CLIENTE.linha_nome.setText(cliente[1])
        tl_EDITAR_CLIENTE.linha_email.setText(cliente[2])
        tl_EDITAR_CLIENTE.linha_end.setText(cliente[3])

    tl_EDITAR_CLIENTE.show()

def salvar_dados():
    linha_selecionada = tl_LISTA_CLIENTES.tabela_dados.currentRow()

    if linha_selecionada < 0:
        QtWidgets.QMessageBox.warning(tl_LISTA_CLIENTES, 'AVISO, Selecione um registro para editar')
        return
    id = tl_EDITAR_CLIENTE.linha_id.text()
    nome = tl_EDITAR_CLIENTE.linha_nome.text()
    email = tl_EDITAR_CLIENTE.linha_email.text()
    endereco = tl_EDITAR_CLIENTE.linha_end.text()

    cursor = banco.cursor()
    comando_SQL = 'UPDATE clientes SET nome = %s, email = %s, endereco = %s WHERE id_cliente = %s'
    cursor.execute(comando_SQL, (nome, email, endereco, id))

    banco.commit()
    cursor.close()

    tl_EDITAR_CLIENTE.close()
    listar_clientes()

    msg = QtWidgets.QMessageBox()
    msg.setWindowTitle('Sucesso')
    msg.setText('Os dados foram atualizados com sucesso!')
    msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
    msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
    msg.exec()

####### CARREGANDO TELAS #######
app = QtWidgets.QApplication([])
tl_LOGIN = uic.loadUi('TELA_LOGIN.ui')
tl_CADASTRO = uic.loadUi('CADASTRO.ui')
tl_LISTA_CLIENTES = uic.loadUi('LISTAR_CLIENTES.ui')
tl_EDITAR_CLIENTE = uic.loadUi('EDITAR_CLIENTES.ui')

####### FUNÇÕES DE BOTÕES #######
tl_CADASTRO.bt_cadastrar.clicked.connect(cadastrar_clientes)
tl_CADASTRO.bt_listar.clicked.connect(listar_clientes)
tl_LISTA_CLIENTES.bt_deletar.clicked.connect(deletar_cliente)
tl_LISTA_CLIENTES.botao_editar.clicked.connect(editar_registro)
tl_EDITAR_CLIENTE.botao_salvar.clicked.connect(salvar_dados)
tl_LOGIN.botao_avancar.clicked.connect(entrar)

####### CONFIGURAÇÕES DA TABELA DE CLIENTES #######
tl_LISTA_CLIENTES.tabela_dados.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
tl_LISTA_CLIENTES.tabela_dados.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
tl_LISTA_CLIENTES.tabela_dados.clearSelection()  # Garante que nada está selecionado ao abrir
# Destaca a linha inteira ao clicar
tl_LISTA_CLIENTES.tabela_dados.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
# Personaliza a cor da linha selecionada
tl_LISTA_CLIENTES.tabela_dados.setStyleSheet("""
    QTableWidget::item:selected {
        background-color: #87CEFA;  /* Azul claro */
        color: black;  /* Texto preto */
    }
""")

######### PRIMEIRA TELA DO SISTEMA #########
tl_LOGIN.show()
app.exec()