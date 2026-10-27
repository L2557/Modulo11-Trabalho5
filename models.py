class Utilizador:
    def __init__(self, nome, email, papel):
        self.nome = nome
        self.email = email
        self.papel = papel

class Administrador(Utilizador):
    def __init__(self, nome, email):
        super().__init__(nome, email, "Admin")

class Voluntario(Utilizador):
    def __init__(self, nome, email):
        super().__init__(nome, email, "Voluntario")

class Doador(Utilizador):
    def __init__(self, nome, email):
        super().__init__(nome, email, "Doador")