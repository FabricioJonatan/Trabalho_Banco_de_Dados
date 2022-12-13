-- PROVEDOR

SHOW DATABASES;
CREATE DATABASE provedor;
USE provedor;


CREATE TABLE clientes(
	id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
	nome VARCHAR(45) NOT NULL,
	telefone VARCHAR(20),
	endereco VARCHAR(60) NOT NULL
);

CREATE TABLE planos(
	id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
	nome VARCHAR(45) NOT NULL,
	largura_banda INT NOT NULL,
	preco INT NOT NULL
);

CREATE TABLE clientes_tem_planos(
	id_cliente INT NOT NULL,
	id_plano INT NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id),
    FOREIGN KEY (id_plano) REFERENCES planos(id)
);

SELECT * FROM clientes;
SELECT * FROM planos;
SELECT * FROM clientes_tem_planos;

