CREATE DATABASE estoque_discos;

CREATE TABLE produtos (
	id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    artista VARCHAR(150),
    genero VARCHAR(150),
    quantidade INT NOT NULL DEFAULT 0,
	preco DECIMAL(10, 2) NOT NULL,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE movimentacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    produto_id INT,
    tipo ENUM('entrada', 'saida') NOT NULL,
    quantidade INT NOT NULL,
    data_movimentacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (produto_id) REFERENCES produtos(id)
);

INSERT INTO produtos (nome, artista, genero, quantidade, preco)
VALUES 
('Master of Puppets', 'Metallica', 'Thrash Metal', 10, 59.90),
('The Number of the Beast', 'Iron Maiden', 'Heavy Metal', 8, 49.90),
('Rust in Peace', 'Megadeth', 'Thrash Metal', 5, 54.90);

INSERT INTO produtos (nome, artista, genero, quantidade, preco)
VALUES 
('With Ears To See And Eyes To Hear', 'Sleeping With Sirens', 'Post-hardcore', 13, 89.90),
('If You Cant Hang', 'Sleeping With Sirens', 'Post-hardcore', 8, 59.90),
('Nikki', 'Forever The Sickest Kids', 'Pop punk', 10, 46.90);

ALTER TABLE produtos CHANGE id id_produto INT AUTO_INCREMENT;
ALTER TABLE movimentacoes
MODIFY produto_id INT NOT NULL;

CREATE TABLE categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

ALTER TABLE produtos
ADD COLUMN categoria_id INT,
ADD CONSTRAINT fk_categoria
FOREIGN KEY (categoria_id) REFERENCES categorias(id);

INSERT INTO categorias (nome) VALUES ('Rock'), ('Pop'), ('Metal');
