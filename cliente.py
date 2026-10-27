import socket

HOST = '127.0.0.1'
PORT = 5000

def enviar_servidor(mensagem):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    client_socket.send(mensagem.encode('utf-8'))
    resposta = client_socket.recv(4096).decode('utf-8')
    client_socket.close()
    return resposta

utilizador_atual = None

while True:
    if not utilizador_atual:
        print("\n1. Login")
        print("2. Registar Utilizador")
        print("0. Sair")
        opcao_menu = input("Escolha uma opcao: ")

        if opcao_menu == "0":
            break
        elif opcao_menu == "1":
            username_input = input("Username: ")
            password_input = input("Password: ")
            resposta_servidor = enviar_servidor(f"LOGIN;{username_input};{password_input}")
            dados_resposta = resposta_servidor.split(";")
            if dados_resposta[0] == "SUCESSO":
                utilizador_atual = {"id": dados_resposta[1], "nome": dados_resposta[2], "papel": dados_resposta[3]}
                print(f"\nLogin efetuado com sucesso! Bem-vindo {utilizador_atual['nome']} ({utilizador_atual['papel']})")
            else:
                print(f"\nErro: {dados_resposta[1]}")
        elif opcao_menu == "2":
            username_input = input("Username: ")
            password_input = input("Password: ")
            nome_input = input("Nome: ")
            email_input = input("Email: ")
            print("1. Admin | 2. Voluntario | 3. Doador")
            opcao_papel = input("Papel: ")
            mapa_papeis = {"1": "Admin", "2": "Voluntario", "3": "Doador"}
            papel_escolhido = mapa_papeis.get(opcao_papel, "Doador")
            resposta_servidor = enviar_servidor(f"REGISTAR;{username_input};{password_input};{nome_input};{email_input};{papel_escolhido}")
            print(resposta_servidor.split(";")[1])
    else:
        print(f"\n--- MENU [{utilizador_atual['papel'].upper()}] ---")
        print("1. Consultar Campanhas Ativas e Inativas")
        print("2. Fazer Doacao")
        print("3. Consultar Historico de Doacoes")
        print("4. Atualizar Perfil")

        if utilizador_atual['papel'] == "Voluntario":
            print("5. Associar-se a Campanha")
            print("6. Ver Minhas Tarefas")
            print("7. Atualizar Estado de Tarefa")

        if utilizador_atual['papel'] == "Admin":
            print("8. Criar Campanha")
            print("9. Encerrar Campanha")
            print("10. Excluir Campanha")
            print("11. Relatorios e Estatisticas")
            print("12. Atualizar Estado de Doacao")

        print("0. Logout")
        opcao_menu = input("Escolha uma opcao: ")

        if opcao_menu == "0":
            utilizador_atual = None
        elif opcao_menu == "1":
            resposta_servidor = enviar_servidor("LISTAR_CAMPANHAS")
            dados_resposta = resposta_servidor.split(";")
            if dados_resposta[0] == "SUCESSO" and len(dados_resposta) > 1 and dados_resposta[1] != "":
                print("\n--- LISTA DE CAMPANHAS ---")
                for item in dados_resposta[1].split("|"):
                    partes_campanha = item.split(",")
                    print(f"ID: {partes_campanha[0]} | Nome: {partes_campanha[1]} | Descricao: {partes_campanha[2]} | Estado: {partes_campanha[3]}")
            else:
                print("\nNenhuma campanha encontrada.")
        elif opcao_menu == "2":
            id_campanha_input = input("ID da Campanha (ou deixe vazio): ")
            tipo_opcao = input("Tipo (1-Monetario / 2-Material): ")
            tipo_doacao = "Monetario" if tipo_opcao == "1" else "Material"
            descricao_item = input("Descricao do item: ") if tipo_doacao == "Material" else "Dinheiro"
            quantidade_input = input("Quantidade / Valor: ")
            resposta_servidor = enviar_servidor(f"REGISTAR_DOACAO;{utilizador_atual['id']};{id_campanha_input};{tipo_doacao};{descricao_item};{quantidade_input}")
            print(resposta_servidor.split(";")[1])
        elif opcao_menu == "3":
            resposta_servidor = enviar_servidor(f"HISTORICO_DOACOES;{utilizador_atual['id']}")
            dados_resposta = resposta_servidor.split(";")
            if dados_resposta[0] == "SUCESSO" and len(dados_resposta) > 1 and dados_resposta[1] != "":
                print("\n--- HISTORICO DE DOACOES ---")
                for item in dados_resposta[1].split("|"):
                    partes_doacao = item.split(",")
                    print(f"ID: {partes_doacao[0]} | Tipo: {partes_doacao[1]} | Item: {partes_doacao[2]} | Qtd: {partes_doacao[3]} | Estado: {partes_doacao[4]}")
            else:
                print("\nSem doacoes registadas.")
        elif opcao_menu == "4":
            novo_nome = input("Novo Nome: ")
            novo_email = input("Novo Email: ")
            resposta_servidor = enviar_servidor(f"ATUALIZAR_PERFIL;{utilizador_atual['id']};{novo_nome};{novo_email}")
            print(resposta_servidor.split(";")[1])
            if resposta_servidor.split(";")[0] == "SUCESSO":
                utilizador_atual['nome'] = novo_nome
        elif opcao_menu == "5" and utilizador_atual['papel'] == "Voluntario":
            id_campanha_input = input("ID da Campanha: ")
            resposta_servidor = enviar_servidor(f"ASSOCIAR_VOLUNTARIO;{id_campanha_input};{utilizador_atual['id']}")
            print(resposta_servidor.split(";")[1])
        elif opcao_menu == "6" and utilizador_atual['papel'] == "Voluntario":
            resposta_servidor = enviar_servidor(f"LISTAR_TAREFAS;{utilizador_atual['id']}")
            dados_resposta = resposta_servidor.split(";")
            if dados_resposta[0] == "SUCESSO" and len(dados_resposta) > 1 and dados_resposta[1] != "":
                print("\n--- MINHAS TAREFAS ---")
                for item in dados_resposta[1].split("|"):
                    partes_tarefa = item.split(",")
                    print(f"ID: {partes_tarefa[0]} | Descricao: {partes_tarefa[1]} | Estado: {partes_tarefa[2]}")
            else:
                print("\nSem tarefas atribuídas.")
        elif opcao_menu == "7" and utilizador_atual['papel'] == "Voluntario":
            id_tarefa_input = input("ID da Tarefa: ")
            print("1. pendente | 2. em_andamento | 3. concluida")
            escolha_estado = input("Escolha o novo estado: ")
            mapa_estados = {"1": "pendente", "2": "em_andamento", "3": "concluida"}
            novo_estado = mapa_estados.get(escolha_estado, "pendente")
            resposta_servidor = enviar_servidor(f"ATUALIZAR_ESTADO_TAREFA;{id_tarefa_input};{novo_estado}")
            print(resposta_servidor.split(";")[1])
        elif opcao_menu == "8" and utilizador_atual['papel'] == "Admin":
            nome_campanha_input = input("Nome da Campanha: ")
            descricao_campanha_input = input("Descricao da Campanha: ")
            resposta_servidor = enviar_servidor(f"CRIAR_CAMPANHA;{nome_campanha_input};{descricao_campanha_input}")
            print(resposta_servidor.split(";")[1])
        elif opcao_menu == "9" and utilizador_atual['papel'] == "Admin":
            id_campanha_input = input("ID da Campanha a encerrar: ")
            resposta_servidor = enviar_servidor(f"ENCERRAR_CAMPANHA;{id_campanha_input}")
            print(resposta_servidor.split(";")[1])
        elif opcao_menu == "10" and utilizador_atual['papel'] == "Admin":
            id_campanha_input = input("ID da Campanha a excluir: ")
            resposta_servidor = enviar_servidor(f"EXCLUIR_CAMPANHA;{utilizador_atual['papel']};{id_campanha_input}")
            print(resposta_servidor.split(";")[1])
        elif opcao_menu == "11" and utilizador_atual['papel'] == "Admin":
            resposta_servidor = enviar_servidor("RELATORIOS")
            print(f"\n--- RELATORIOS E ESTATISTICAS ---\n{resposta_servidor.split(';')[1]}")
        elif opcao_menu == "12" and utilizador_atual['papel'] == "Admin":
            id_doacao_input = input("ID da Doacao: ")
            print("1. pendente | 2. entregue | 3. distribuida")
            escolha_estado = input("Escolha o novo estado: ")
            mapa_estados = {"1": "pendente", "2": "entregue", "3": "distribuida"}
            novo_estado = mapa_estados.get(escolha_estado, "pendente")
            resposta_servidor = enviar_servidor(f"ATUALIZAR_ESTADO_DOACAO;{id_doacao_input};{novo_estado}")
            print(resposta_servidor.split(";")[1])
