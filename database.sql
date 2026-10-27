CREATE DATABASE IF NOT EXISTS gestao_doacoes;
USE gestao_doacoes;

CREATE TABLE IF NOT EXISTS utilizadores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    papel ENUM('Admin', 'Voluntario', 'Doador') NOT NULL
);

CREATE TABLE IF NOT EXISTS campanhas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    estado ENUM('Ativa', 'Encerrada') DEFAULT 'Ativa'
);

CREATE TABLE IF NOT EXISTS doacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_doador INT NOT NULL,
    id_campanha INT,
    tipo ENUM('Monetario', 'Material') NOT NULL,
    descricao_item VARCHAR(100),
    quantidade DECIMAL(10,2) NOT NULL,
    estado ENUM('pendente', 'entregue', 'distribuida') DEFAULT 'pendente',
    FOREIGN KEY (id_doador) REFERENCES utilizadores(id) ON DELETE CASCADE,
    FOREIGN KEY (id_campanha) REFERENCES campanhas(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS campanha_voluntarios (
    id_campanha INT NOT NULL,
    id_voluntario INT NOT NULL,
    PRIMARY KEY (id_campanha, id_voluntario),
    FOREIGN KEY (id_campanha) REFERENCES campanhas(id) ON DELETE CASCADE,
    FOREIGN KEY (id_voluntario) REFERENCES utilizadores(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tarefas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_voluntario INT NOT NULL,
    descricao VARCHAR(255) NOT NULL,
    estado ENUM('pendente', 'em_andamento', 'concluida') DEFAULT 'pendente',
    FOREIGN KEY (id_voluntario) REFERENCES utilizadores(id) ON DELETE CASCADE
);