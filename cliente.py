import socket

HOST = '127.0.0.1'
PORT = 5000

def enviar_servidor(mensagem):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    client_socket.send(mensagem.encode('utf-8'))
    resposta = client_socket.recv(1024).decode('utf-8')
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
        print("1. Fazer Doacao")
        if utilizador_atual['papel'] == "Admin":
            print("2. Criar Campanha")
        print("0. Logout")
        opcao_menu = input("Escolha uma opcao: ")

        if opcao_menu == "0":
            utilizador_atual = None
        elif opcao_menu == "1":
            id_campanha_input = input("ID da Campanha (ou deixe vazio): ")
            tipo_opcao = input("Tipo (1-Monetario / 2-Material): ")
            tipo_doacao = "Monetario" if tipo_opcao == "1" else "Material"
            descricao_item = input("Descricao do item: ") if tipo_doacao == "Material" else "Dinheiro"
            quantidade_input = input("Quantidade / Valor: ")
            resposta_servidor = enviar_servidor(f"REGISTAR_DOACAO;{utilizador_atual['id']};{id_campanha_input};{tipo_doacao};{descricao_item};{quantidade_input}")
            print(resposta_servidor.split(";")[1])
        elif opcao_menu == "2" and utilizador_atual['papel'] == "Admin":
            nome_campanha_input = input("Nome da Campanha: ")
            descricao_campanha_input = input("Descricao da Campanha: ")
            resposta_servidor = enviar_servidor(f"CRIAR_CAMPANHA;{nome_campanha_input};{descricao_campanha_input}")
            print(resposta_servidor.split(";")[1])