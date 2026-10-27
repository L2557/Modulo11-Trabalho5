import socket
import mysql.connector

def ligar_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="gestao_doacoes"
    )

HOST = '127.0.0.1'
PORT = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Servidor a escutar em {HOST}:{PORT}...")

while True:
    conexao_cliente, endereco = server_socket.accept()
    dados_recebidos = conexao_cliente.recv(1024).decode('utf-8').strip()
    
    if not dados_recebidos:
        conexao_cliente.close()
        continue

    partes = dados_recebidos.split(";")
    acao = partes[0]
    resposta = "ERRO;Acao invalida"

    try:
        conexao_base_dados = ligar_db()
        cursor = conexao_base_dados.cursor()

        if acao == "LOGIN":
            username = partes[1]
            password = partes[2]
            cursor.execute("SELECT id, nome, papel FROM utilizadores WHERE username = %s AND password = %s", (username, password))
            utilizador_db = cursor.fetchone()
            if utilizador_db:
                resposta = f"SUCESSO;{utilizador_db[0]};{utilizador_db[1]};{utilizador_db[2]}"
            else:
                resposta = "ERRO;Credenciais invalidas"

        elif acao == "REGISTAR":
            username = partes[1]
            password = partes[2]
            nome = partes[3]
            email = partes[4]
            papel = partes[5]
            cursor.execute("INSERT INTO utilizadores (username, password, nome, email, papel) VALUES (%s, %s, %s, %s, %s)", (username, password, nome, email, papel))
            conexao_base_dados.commit()
            resposta = "SUCESSO;Utilizador registado com sucesso"

        elif acao == "CRIAR_CAMPANHA":
            nome_campanha = partes[1]
            descricao_campanha = partes[2]
            cursor.execute("INSERT INTO campanhas (nome, descricao) VALUES (%s, %s)", (nome_campanha, descricao_campanha))
            conexao_base_dados.commit()
            resposta = "SUCESSO;Campanha criada com sucesso"

        elif acao == "REGISTAR_DOACAO":
            id_doador = partes[1]
            id_campanha = partes[2] if partes[2] != "None" and partes[2] != "" else None
            tipo_doacao = partes[3]
            descricao_item = partes[4]
            quantidade = partes[5]
            cursor.execute("INSERT INTO doacoes (id_doador, id_campanha, tipo, descricao_item, quantidade) VALUES (%s, %s, %s, %s, %s)", (id_doador, id_campanha, tipo_doacao, descricao_item, quantidade))
            conexao_base_dados.commit()
            resposta = "SUCESSO;Doacao registada com sucesso"

        cursor.close()
        conexao_base_dados.close()
    except Exception as erro:
        resposta = f"ERRO;{str(erro)}"

    conexao_cliente.send(resposta.encode('utf-8'))
    conexao_cliente.close()