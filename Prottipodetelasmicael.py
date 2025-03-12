from PyQt6 import uic, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QLineEdit
import pymysql, sys

banco = pymysql.connect(
    host = "localhost",
    user = "root",
    passwd = "",
    database = "bd_teste"
)


def visibilidade_senha():
    if login_cadstro.lineEdit_passwrd.echoMode() == QLineEdit.EchoMode.Password or login_cadstro.lineEdit_passwrd_2.echoMode() == QLineEdit.EchoMode.Password:
        login_cadstro.lineEdit_passwrd.setEchoMode(QLineEdit.EchoMode.Normal)
        login_cadstro.passButton_view.setText("O")

        login_cadstro.lineEdit_passwrd_confirm.setEchoMode(QLineEdit.EchoMode.Normal)
        login_cadstro.lineEdit_passwrd_2.setEchoMode(QLineEdit.EchoMode.Normal)
        login_cadstro.passButton_view_2.setText("O")
    else:
        login_cadstro.lineEdit_passwrd.setEchoMode(QLineEdit.EchoMode.Password)
        login_cadstro.passButton_view.setText("-")

        login_cadstro.lineEdit_passwrd_confirm.setEchoMode(QLineEdit.EchoMode.Password)
        login_cadstro.lineEdit_passwrd_2.setEchoMode(QLineEdit.EchoMode.Password)
        login_cadstro.passButton_view_2.setText("-") 

def trocar_telas ():
    if login_cadstro.frame_login.isVisible():
        login_cadstro.frame_login.hide()
        login_cadstro.frame_cadstr.show()
    else: 
        login_cadstro.frame_login.show()
        login_cadstro.frame_cadstr.hide()


def entrar():
    user = login_cadstro.lineEdit_user.text()
    passwrd = login_cadstro.lineEdit_passwrd.text()

    cursor = banco.cursor()
    comando_SQL = "SELECT Senha FROM usuarios WHERE Usuario = %s"
    cursor.execute(comando_SQL, (user,))
    resultado = cursor.fetchone()

    if resultado:
        senha_bd = resultado[0]

        if passwrd == senha_bd:
            QMessageBox.information(login_cadstro, "Sucesso", "Login realizado com sucesso!")
            
            menu_principal.show()  
                        
            login_cadstro.hide()  # Apenas escondendo a tela de login
        else:
            QMessageBox.warning(login_cadstro, "Erro", "Senha incorreta!")
    else:
        QMessageBox.warning(login_cadstro, "Erro", "Usuário não encontrado!")


def novo_Cadstr ():
    name = login_cadstro.lineEdit_name.text()
    user = login_cadstro.lineEdit_user_2.text()
    email = login_cadstro.lineEdit_email.text()
    passwrd = login_cadstro.lineEdit_passwrd_2.text()
    passwrd_conf = login_cadstro.lineEdit_passwrd_confirm.text()

    if not name or not user or not email or not passwrd or not passwrd_conf:
        QMessageBox.warning(login_cadstro, "Erro", "Todos os campos devem ser preenchidos!")
        return

    # Verifica se o usuário já existe no banco de dados
    cursor = banco.cursor()
    comando_SQL = "SELECT usuario FROM usuarios WHERE usuario = %s"
    cursor.execute(comando_SQL, (user,))
    resultado = cursor.fetchone()

    if resultado:
        QMessageBox.warning(login_cadstro, "Erro", "Usuário já existente!")
        return
    
    # Verifica se o e-mail já existe no banco de dados
    cursor = banco.cursor()
    comando_SQL = "SELECT email FROM usuarios WHERE email = %s"
    cursor.execute(comando_SQL, (email,))
    resultado = cursor.fetchone()

    if resultado:
        QMessageBox.warning(login_cadstro, "Erro", "E-mail já existente!")
        return

    # Verifica se as senhas são iguais
    if passwrd != passwrd_conf:
        QMessageBox.warning(login_cadstro, "Erro", "As senhas não coincidem!")
        return

    # Inserção no banco de dados
    comando_SQL = "INSERT INTO usuarios (nome, usuario, email, senha) VALUES (%s, %s, %s, %s)"
    dados = (str(name), str(user), str(email), str(passwrd))
    cursor.execute(comando_SQL, dados)
    banco.commit()

    QMessageBox.information(login_cadstro, "Sucesso", "Cadastro realizado com sucesso!")

    # Reset da lines após cadastro 
    login_cadstro.lineEdit_name.setText("")
    login_cadstro.lineEdit_user_2.setText("")
    login_cadstro.lineEdit_email.setText("")
    login_cadstro.lineEdit_passwrd_2.setText("")
    login_cadstro.lineEdit_passwrd_confirm.setText("")

    #===========================================================( Menu Principal )=======================================================================================

def esconder_menu ():
    if menu_principal.stackedMenu.isVisible():
        menu_principal.stackedMenu.hide()
        menu_principal.open_closeButton.setText(">>")
    else: 
        menu_principal.stackedMenu.show()
        menu_principal.open_closeButton.setText("<<")


def cliente_menu ():
    menu_principal.stackedMenu.setCurrentIndex(1)
def usuario_menu ():
    menu_principal.stackedMenu.setCurrentIndex(2)
def voltar_menu ():
    menu_principal.stackedMenu.setCurrentIndex(0) 


def abrir_cadstr_clientes ():
    if menu_principal.stackedWidget.isVisible():
        menu_principal.stackedWidget.setCurrentIndex(3)
    else:
        menu_principal.stackedWidget.setCurrentIndex(3)
        menu_principal.stackedWidget.show()

def cadstr_clientes ():
    name = menu_principal.lineEdit_name.text()
    cpf = menu_principal.lineEdit_cpf.text()
    email = menu_principal.lineEdit_email.text()
    telefone = menu_principal.lineEdit_phone.text()
    endereco = menu_principal.lineEdit_endereco.text()



    cursor = banco.cursor()
    comando_SQL = "INSERT INTO clientes (Nome, CPF, Email, Telefone, Endereco) VALUES (%s, %s, %s, %s, %s)"
    dados = (str(name), str(cpf), str(email), str(telefone), str(endereco))
    cursor.execute(comando_SQL,dados)
    banco.commit()
    QMessageBox.warning(menu_principal, "Sucesso", "Cadastro realizado com Sucesso!")

    # Reset da lines após cadastro 
    menu_principal.lineEdit_name.setText("")
    menu_principal.lineEdit_cpf.setText("")
    menu_principal.lineEdit_email.setText("")
    menu_principal.lineEdit_phone.setText("")
    menu_principal.lineEdit_endereco.setText("")


def abrir_lista_clientes ():
    menu_principal.stackedWidget.show()
    if menu_principal.stackedWidget.isVisible():
        menu_principal.stackedWidget.setCurrentIndex(2)
    else:
        menu_principal.stackedWidget.setCurrentIndex(2)

    cursor = banco.cursor()
    cursor.execute("SELECT * FROM clientes")
    dados_lidos = cursor.fetchall()

    menu_principal.tableWidget.setRowCount(len(dados_lidos))
    menu_principal.tableWidget.setColumnCount(6)

    for i, linha in enumerate(dados_lidos):
        for j, valor in enumerate(linha):
            menu_principal.tableWidget.setItem(i,j, QtWidgets.QTableWidgetItem(str(valor)))

    #===============================( Ajuste da Tabela Clientes )=====================================================
    menu_principal.tableWidget.resizeColumnsToContents()


def deletar_clientes():
    linha = menu_principal.tableWidget.currentRow()
    if linha == -1:
        QMessageBox.warning(menu_principal, "Erro", "Selecione um cliente para deletar.")
        return
    
    cursor = banco.cursor()
    cursor.execute("SELECT ID_Cliente FROM clientes")
    dados_lidos = cursor.fetchall()
    
    valor_id = dados_lidos[linha][0]
    cursor.execute("DELETE FROM clientes WHERE ID_Cliente = %s", (valor_id,))
    banco.commit()
    
    menu_principal.tableWidget.removeRow(linha)
    QMessageBox.information(menu_principal, "Sucesso", "Cliente deletado com sucesso!")

def editar_clientes ():
    tela_editar.stackedWidget.setCurrentIndex(0)
    
    linha = menu_principal.tableWidget.currentRow()
    if linha == -1:
        QMessageBox.warning(menu_principal, "Erro", "Selecione um cliente para editar.")
        return
    
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM clientes")
    dados_lidos = cursor.fetchall()
    
    clientes = dados_lidos[linha]
    tela_editar.show()
    menu_principal.hide()
    
    tela_editar.lineEdit_id_2.setText(str(clientes[0]))
    tela_editar.lineEdit_cpf.setText(str(clientes[1]))
    tela_editar.lineEdit_name_2.setText(str(clientes[2]))
    tela_editar.lineEdit_email_2.setText(str(clientes[3]))
    tela_editar.lineEdit_phone.setText(str(clientes[4]))
    tela_editar.lineEdit_endereco.setText(str(clientes[5]))

def salvar_clienteEdit():
    id = tela_editar.lineEdit_id_2.text()
    cpf = tela_editar.lineEdit_cpf.text()
    nome = tela_editar.lineEdit_name_2.text()
    email = tela_editar.lineEdit_email_2.text()
    telefone = tela_editar.lineEdit_phone.text()
    endereco = tela_editar.lineEdit_endereco.text()

    if not id or not cpf or not nome or not email or not telefone or not endereco:
        QMessageBox.warning(tela_editar, "Erro", "Todos os campos devem ser preenchidos!")
        return
        
    cursor = banco.cursor()
    cursor.execute("UPDATE clientes SET Nome = %s, CPF = %s, Email = %s, Telefone = %s, Endereco = %s WHERE ID_Cliente = %s", (nome, cpf, email, telefone, endereco, id))
    banco.commit()

    
    QMessageBox.information(tela_editar, "Sucesso", "Os dados foram alterados com sucesso!")
    tela_editar.close()
    
    abrir_lista_clientes()
    menu_principal.show()

def fechar_listas ():
    if menu_principal.stackedWidget.isVisible():
        menu_principal.stackedWidget.hide()

def abrir_cadstr_usuarios ():
    if menu_principal.stackedWidget.isVisible():
        menu_principal.stackedWidget.setCurrentIndex(1)
    else:
        menu_principal.stackedWidget.setCurrentIndex(1)
        menu_principal.stackedWidget.show()

def cadstr_user ():
    name = menu_principal.lineEdit_name_2.text()
    user = menu_principal.lineEdit_user.text()
    email = menu_principal.lineEdit_email_2.text()
    passwrd = menu_principal.lineEdit_passwrd.text()
    passwrd_conf = menu_principal.lineEdit_passwrd_confirm.text()

    if not name or not user or not email or not passwrd or not passwrd_conf:
        QMessageBox.warning(menu_principal, "Erro", "Todos os campos devem ser preenchidos!")
        return

    # Verifica se o usuário já existe no banco de dados
    cursor = banco.cursor()
    comando_SQL = "SELECT usuario FROM usuarios WHERE usuario = %s"
    cursor.execute(comando_SQL, (user,))
    resultado = cursor.fetchone()

    if resultado:
        QMessageBox.warning(menu_principal, "Erro", "Usuário já existente!")
        return
    
    # Verifica se o e-mail já existe no banco de dados
    cursor = banco.cursor()
    comando_SQL = "SELECT email FROM usuarios WHERE email = %s"
    cursor.execute(comando_SQL, (email,))
    resultado = cursor.fetchone()

    if resultado:
        QMessageBox.warning(menu_principal, "Erro", "E-mail já existente!")
        return

    # Verifica se as senhas são iguais
    if passwrd != passwrd_conf:
        QMessageBox.warning(menu_principal, "Erro", "As senhas não coincidem!")
        return

    # Inserção no banco de dados
    comando_SQL = "INSERT INTO usuarios (nome, usuario, email, senha) VALUES (%s, %s, %s, %s)"
    dados = (str(name), str(user), str(email), str(passwrd))
    cursor.execute(comando_SQL, dados)
    banco.commit()

    QMessageBox.information(menu_principal, "Sucesso", "Cadastro realizado com sucesso!")

    # Reset da lines após cadastro 
    menu_principal.lineEdit_name_2.setText("")
    menu_principal.lineEdit_user.setText("")
    menu_principal.lineEdit_email_2.setText("")
    menu_principal.lineEdit_passwrd.setText("")
    menu_principal.lineEdit_passwrd_confirm.setText("")


def abrir_lista_usuarios ():
    menu_principal.stackedWidget.show()
    if menu_principal.stackedWidget.isVisible():
        menu_principal.stackedWidget.setCurrentIndex(0)
    else:
        menu_principal.stackedWidget.setCurrentIndex(0)

    cursor = banco.cursor()
    cursor.execute("SELECT * FROM usuarios")
    dados_lidos = cursor.fetchall()

    menu_principal.tableWidget_2.setRowCount(len(dados_lidos))
    menu_principal.tableWidget_2.setColumnCount(5)

    for i, linha in enumerate(dados_lidos):
        for j, valor in enumerate(linha):
            menu_principal.tableWidget_2.setItem(i,j, QtWidgets.QTableWidgetItem(str(valor)))

    #===============================( Ajuste da Tabela Usuários )=====================================================
    menu_principal.tableWidget_2.resizeColumnsToContents()


def deletar_user():
    linha = menu_principal.tableWidget_2.currentRow()
    if linha == -1:
        QMessageBox.warning(menu_principal, "Erro", "Selecione um Usuário para deletar.")
        return
    
    cursor = banco.cursor()
    cursor.execute("SELECT ID_usuario FROM usuarios")
    dados_lidos = cursor.fetchall()
    
    valor_id = dados_lidos[linha][0]
    cursor.execute("DELETE FROM usuarios WHERE ID_usuario = %s", (valor_id,))
    banco.commit()
    
    menu_principal.tableWidget_2.removeRow(linha)
    QMessageBox.information(menu_principal, "Sucesso", "Usuário deletado com sucesso!")

def editar_user ():
    tela_editar.stackedWidget.setCurrentIndex(1)
    

    linha = menu_principal.tableWidget_2.currentRow()
    if linha == -1:
        QMessageBox.warning(menu_principal, "Erro", "Selecione um usuário para editar.")
        return
    
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM usuarios")
    dados_lidos = cursor.fetchall()
    
    user = dados_lidos[linha]
    tela_editar.show()
    menu_principal.hide()
    
    tela_editar.lineEdit_id.setText(str(user[0]))
    tela_editar.lineEdit_name.setText(str(user[1]))
    tela_editar.lineEdit_user.setText(str(user[2]))
    tela_editar.lineEdit_email.setText(str(user[3]))
    tela_editar.lineEdit_passwrd.setText(str(user[4]))

def salvar_userEdit():    
    id = tela_editar.lineEdit_id.text()
    nome = tela_editar.lineEdit_name.text()
    user = tela_editar.lineEdit_user.text()
    email = tela_editar.lineEdit_email.text()
    senha = tela_editar.lineEdit_passwrd.text()

    if not id or not nome or not user or not email or not senha:
        QMessageBox.warning(tela_editar, "Erro", "Todos os campos devem ser preenchidos!")
        return
        
    cursor = banco.cursor()
    cursor.execute("UPDATE usuarios SET Nome = %s, Usuario = %s, Email = %s, Senha = %s WHERE ID_Usuario = %s", (nome, user, email, senha, id))
    banco.commit()

    
    QMessageBox.information(tela_editar, "Sucesso", "Os dados foram alterados com sucesso!")
    tela_editar.close()
    
    abrir_lista_usuarios()
    menu_principal.show()

def cancelar_edit():
    if tela_editar.isVisible():
        tela_editar.close()
        menu_principal.show()



app = QtWidgets.QApplication(sys.argv)
#===========================( Login/ Cadastro )============================================= 
login_cadstro = uic.loadUi("telas manuais/tela_login_cadstro.ui")
login_cadstro.passButton_view.clicked.connect(visibilidade_senha)
login_cadstro.passButton_view_2.clicked.connect(visibilidade_senha)
login_cadstro.novo_cadstrButton.clicked.connect(trocar_telas)
login_cadstro.pushButton_back.clicked.connect(trocar_telas)
login_cadstro.frame_cadstr.hide()

login_cadstro.lineEdit_passwrd.setEchoMode(QLineEdit.EchoMode.Password)
login_cadstro.passButton_view.setText("-")

login_cadstro.lineEdit_passwrd_confirm.setEchoMode(QLineEdit.EchoMode.Password)
login_cadstro.lineEdit_passwrd_2.setEchoMode(QLineEdit.EchoMode.Password)
login_cadstro.passButton_view_2.setText("-")

#===========================( Funções das telas Login/ Cadastro )===========================
login_cadstro.pushButton.clicked.connect(entrar)
login_cadstro.pushButton_2.clicked.connect(novo_Cadstr)



#===========================( Menu Principal )==============================================
menu_principal = uic.loadUi("telas manuais/tela_menuprinc.ui")
menu_principal.open_closeButton.clicked.connect(esconder_menu)
menu_principal.open_closeButton.setText("<<")

menu_principal.clienteButton.clicked.connect(cliente_menu)
menu_principal.userButton.clicked.connect(usuario_menu)
menu_principal.clienteButton_back.clicked.connect(voltar_menu)
menu_principal.userButton_back.clicked.connect(voltar_menu)
menu_principal.stackedWidget.hide()
menu_principal.stackedMenu.setCurrentIndex(0)

#===========================( Funções das telas Clientes/ Usuários )========================
menu_principal.closeButton.clicked.connect(fechar_listas)
menu_principal.closeButton_2.clicked.connect(fechar_listas)
menu_principal.closeButton_3.clicked.connect(fechar_listas)
menu_principal.closeButton_4.clicked.connect(fechar_listas)

#===========================( Tela Clientes )===============================================
menu_principal.client_cadstrButton.clicked.connect(abrir_cadstr_clientes)
menu_principal.Button_cadstr.clicked.connect(cadstr_clientes)

menu_principal.cliente_listarButton.clicked.connect(abrir_lista_clientes)
menu_principal.dellButton.clicked.connect(deletar_clientes)
menu_principal.editButton.clicked.connect(editar_clientes)

#===========================( Tela Usuários )===============================================
menu_principal.user_cadstrButton.clicked.connect(abrir_cadstr_usuarios)
menu_principal.Button_cadstr_2.clicked.connect(cadstr_user)

menu_principal.user_listarButton.clicked.connect(abrir_lista_usuarios)
menu_principal.dellButton_2.clicked.connect(deletar_user)
menu_principal.editButton_2.clicked.connect(editar_user)

#===========================( Tela Editar )=================================================
tela_editar = uic.loadUi("telas manuais/tela_editar.ui")
#tela_editar.editButton.clicked.connect(salvar_edit)
tela_editar.editButton.clicked.connect(salvar_clienteEdit)
tela_editar.editButton_2.clicked.connect(salvar_userEdit)

tela_editar.cancelButton.clicked.connect(cancelar_edit)
tela_editar.cancelButton_2.clicked.connect(cancelar_edit)

tela_editar.lineEdit_id.setReadOnly(True)
tela_editar.lineEdit_id.setEnabled(False)
tela_editar.lineEdit_id_2.setReadOnly(True)
tela_editar.lineEdit_id_2.setEnabled(False)




login_cadstro.show()
sys.exit(app.exec())