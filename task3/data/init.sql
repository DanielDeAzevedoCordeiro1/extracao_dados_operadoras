CREATE DATABASE IF NOT EXISTS ans_db;
USE ans_db;

CREATE TABLE IF NOT EXISTS dems_contabeis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    DATA DATE,
    REG_ANS VARCHAR(50),
    CD_CONTA_CONTABIL VARCHAR(50),
    DESCRICAO TEXT,
    VL_SALDO_INICIAL DECIMAL(20,2),
    VL_SALDO_FINAL DECIMAL(20,2)
);


CREATE TABLE IF NOT EXISTS operadoras (
    Registro_ANS VARCHAR(50) PRIMARY KEY,
    CNPJ VARCHAR(20),
    Razao_Social TEXT,
    Nome_Fantasia TEXT,
    Modalidade VARCHAR(50),
    Logradouro TEXT,
    Numero VARCHAR(20),
    Complemento TEXT,
    Bairro VARCHAR(50),
    Cidade VARCHAR(50),
    UF VARCHAR(2),
    CEP VARCHAR(10),
    DDD VARCHAR(5),
    Telefone VARCHAR(20),
    Fax VARCHAR(20),
    Endereco_eletronico TEXT,
    Representante TEXT,
    Cargo_Representante TEXT,
    Regiao_de_Comercializacao TEXT,
    Data_Registro_ANS DATE
);


