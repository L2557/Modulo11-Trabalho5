
import socket
import mysql.connector

def ligar_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="gestao_doacoes"
    )

HOST = '0.0.0.0'
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

        elif acao == "ATUALIZAR_PERFIL":
            user_id = partes[1]
            novo_nome = partes[2]
            novo_email = partes[3]
            cursor.execute("UPDATE utilizadores SET nome = %s, email = %s WHERE id = %s", (novo_nome, novo_email, user_id))
            conexao_base_dados.commit()
            resposta = "SUCESSO;Perfil atualizado com sucesso"

        elif acao == "CRIAR_CAMPANHA":
            nome_campanha = partes[1]
            descricao_campanha = partes[2]
            cursor.execute("INSERT INTO campanhas (nome, descricao) VALUES (%s, %s)", (nome_campanha, descricao_campanha))
            conexao_base_dados.commit()
            resposta = "SUCESSO;Campanha criada com sucesso"

        elif acao == "ENCERRAR_CAMPANHA":
            id_campanha = partes[1]
            cursor.execute("UPDATE campanhas SET estado = 'Encerrada' WHERE id = %s", (id_campanha,))
            conexao_base_dados.commit()
            resposta = "SUCESSO;Campanha encerrada com sucesso"

        elif acao == "EXCLUIR_CAMPANHA":
            papel_utilizador = partes[1]
            id_campanha = partes[2]
            if papel_utilizador != "Admin":
                resposta = "ERRO;Permissao negada. Apenas o administrador pode excluir campanhas."
            else:
                cursor.execute("DELETE FROM campanhas WHERE id = %s", (id_campanha,))
                conexao_base_dados.commit()
                resposta = "SUCESSO;Campanha excluida com sucesso"

        elif acao == "LISTAR_CAMPANHAS":
            cursor.execute("SELECT id, nome, descricao, estado FROM campanhas")
            campanhas = cursor.fetchall()
            lista_formatada = "|".join([f"{c[0]},{c[1]},{c[2]},{c[3]}" for c in campanhas])
            resposta = f"SUCESSO;{lista_formatada}"

        elif acao == "ASSOCIAR_VOLUNTARIO":
            id_campanha = partes[1]
            id_voluntario = partes[2]
            try:
                cursor.execute("INSERT INTO campanha_voluntarios (id_campanha, id_voluntario) VALUES (%s, %s)", (id_campanha, id_voluntario))
                conexao_base_dados.commit()
                resposta = "SUCESSO;Associado à campanha com sucesso"
            except:
                resposta = "ERRO;Ja esta associado ou campanha invalida"

        elif acao == "REGISTAR_DOACAO":
            id_doador = partes[1]
            id_campanha = partes[2] if partes[2] != "None" and partes[2] != "" else None
            tipo_doacao = partes[3]
            descricao_item = partes[4]
            quantidade = partes[5]
            cursor.execute("INSERT INTO doacoes (id_doador, id_campanha, tipo, descricao_item, quantidade) VALUES (%s, %s, %s, %s, %s)", (id_doador, id_campanha, tipo_doacao, descricao_item, quantidade))
            conexao_base_dados.commit()
            resposta = "SUCESSO;Doacao registada com sucesso"

        elif acao == "HISTORICO_DOACOES":
            id_doador = partes[1]
            cursor.execute("SELECT id, tipo, descricao_item, quantidade, estado FROM doacoes WHERE id_doador = %s", (id_doador,))
            doacoes = cursor.fetchall()
            lista_formatada = "|".join([f"{d[0]},{d[1]},{d[2]},{d[3]},{d[4]}" for d in doacoes])
            resposta = f"SUCESSO;{lista_formatada}"

        elif acao == "ATUALIZAR_ESTADO_DOACAO":
            id_doacao = partes[1]
            novo_estado = partes[2]
            cursor.execute("UPDATE doacoes SET estado = %s WHERE id = %s", (novo_estado, id_doacao))
            conexao_base_dados.commit()
            resposta = "SUCESSO;Estado da doacao atualizado"

        elif acao == "LISTAR_TAREFAS":
            id_voluntario = partes[1]
            cursor.execute("SELECT id, descricao, estado FROM tarefas WHERE id_voluntario = %s", (id_voluntario,))
            tarefas = cursor.fetchall()
            lista_formatada = "|".join([f"{t[0]},{t[1]},{t[2]}" for t in tarefas])
            resposta = f"SUCESSO;{lista_formatada}"

        elif acao == "ATUALIZAR_ESTADO_TAREFA":
            id_tarefa = partes[1]
            novo_estado = partes[2]
            cursor.execute("UPDATE tarefas SET estado = %s WHERE id = %s", (novo_estado, id_tarefa))
            conexao_base_dados.commit()
            resposta = "SUCESSO;Estado da tarefa atualizado"

        elif acao == "RELATORIOS":
            cursor.execute("SELECT COUNT(DISTINCT id_voluntario) FROM campanha_voluntarios")
            voluntarios_ativos = cursor.fetchone()[0]
           
            cursor.execute("SELECT c.nome, COUNT(d.id), SUM(d.quantidade) FROM campanhas c LEFT JOIN doacoes d ON c.id = d.id_campanha GROUP BY c.id, c.nome")
            estatisticas_campanhas = cursor.fetchall()
            texto_campanhas = ",".join([f"Campanha {e[0]} ({e[1]} doacoes, Total: {e[2] if e[2] else 0})" for e in estatisticas_campanhas])

            cursor.execute("SELECT tipo, COUNT(*) FROM doacoes GROUP BY tipo")
            distribuicao_itens = cursor.fetchall()
            texto_itens = ",".join([f"{i[0]}: {i[1]}" for i in distribuicao_itens])

            resposta = f"SUCESSO;Voluntarios ativos: {voluntarios_ativos} | Doacoes por campanha: [{texto_campanhas}] | Distribuicao por tipo: [{texto_itens}]"

        cursor.close()
        conexao_base_dados.close()
    except Exception as erro:
        resposta = f"ERRO;{str(erro)}"

    conexao_cliente.send(resposta.encode('utf-8'))
    conexao_cliente.close()
