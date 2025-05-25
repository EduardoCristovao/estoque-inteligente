create schema `bancoestoque`;
use bancoestoque;

#Criando tabela de produtos
create table produtos(
id INT AUTO_INCREMENT PRIMARY KEY,
nome VARCHAR(100) NOT NULL,
preco DECIMAL(10,2) NOT NULL,
categoria varchar(50)
);
#Criando tabela estoque
create table estoque(
id INT AUTO_INCREMENT PRIMARY KEY,
id_produto INT,
quantidade INT NOT NULL,
FOREIGN KEY (id_produto) references produtos(id)
);
#Criando tabela de lotes
CREATE TABLE lotes (
    id INT AUTO_INCREMENT PRIMARY KEY, 
    id_produto INT,
    numero_lote VARCHAR(50),
    quantidade INT,
    FOREIGN KEY (id_produto) REFERENCES produtos(id)
);

#Selecionando tabela para verificar itens
select * from estoque;
select * from produtos;
select * from lotes;

#adicionando data em lotes
ALTER TABLE lotes ADD COLUMN data_lote_entrada DATE;
ALTER TABLE lotes ADD COLUMN data_lote_validade DATE;
