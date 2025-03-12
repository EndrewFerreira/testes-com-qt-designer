# import mysql.connector
# from mysql.connector import Error

# try:
#     conexao = mysql.connector.connect(
#         host='localhost',      # ou o IP do seu servidor
#         user='root',     # usuário do banco de dados
#         password='#mortadela1507',   # senha do banco de dados
#         database='bd_hotel_cop'    # nome do banco de dados
#     )

#     if conexao.is_connected():
#         db_info = conexao.get_server_info()
#         print(f'Conectado ao servidor MySQL versão {db_info}')
        
#         cursor = conexao.cursor()
#         cursor.execute('SELECT DATABASE();')
#         nome_banco = cursor.fetchone()
#         print(f'Banco de dados atual: {nome_banco[0]}')

# except Error as e:
#     print(f'Erro ao conectar ao MySQL: {e}')

# finally:
#     if 'conexao' in locals() and conexao.is_connected():
#         cursor.close()
#         conexao.close()
#         print('Conexão ao MySQL foi encerrada')

import mysql.connector

try:
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='#mortadela1507',
        database='bd_teste',  # substitua pelo nome do seu banco
        auth_plugin='mysql_native_password'
    )
    if conexao.is_connected():
        print("Conexão bem-sucedida ao banco de dados!")
        conexao.close()
except mysql.connector.Error as err:
    print(f"Erro ao conectar ao MySQL: {err}")

