import pandas as pd
from sqlalchemy import create_engine, types, text, MetaData, Table, Column


DB_CONFIG = {
    "username": "root",
    "password": "123",
    "hostname": "localhost",
    "database": "ans_db",
    "port": 3306
}

CSV_PATH_OPERADORAS = "./relatorio/Relatorio_cadop.csv"


def get_db_engine():
    
    connection_string = f"mysql+pymysql://{DB_CONFIG['username']}:{DB_CONFIG['password']}@{DB_CONFIG['hostname']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    return create_engine(connection_string)


def load_csv(file_path):
   
    try:
        return pd.read_csv(
            file_path,
            sep=';',
            encoding='utf-8',
            low_memory=False,
            dtype=str,
            on_bad_lines='skip'
        )
    except Exception as e:
        print(f"Erro ao ler arquivo {file_path}: {e}")
        raise


def get_dtype_mapping():

    return {
        'Registro_ANS': types.VARCHAR(50),
        'CNPJ': types.VARCHAR(20),
        'Razao_Social': types.TEXT,
        'Nome_Fantasia': types.TEXT,
        'Modalidade': types.VARCHAR(50),
        'Logradouro': types.TEXT,
        'Numero': types.VARCHAR(20),
        'Complemento': types.TEXT,
        'Bairro': types.VARCHAR(50),
        'Cidade': types.VARCHAR(50),
        'UF': types.VARCHAR(2),
        'CEP': types.VARCHAR(10),
        'DDD': types.VARCHAR(5),
        'Telefone': types.VARCHAR(20),
        'Fax': types.VARCHAR(20),
        'Endereco_eletronico': types.TEXT,
        'Representante': types.TEXT,
        'Cargo_Representante': types.TEXT,
        'Regiao_de_Comercializacao': types.INTEGER,
        'Data_Registro_ANS': types.DATE
    }


def create_table_if_not_exists(engine, table_name):

    metadata = MetaData()
    Table(
        table_name,
        metadata,
        Column('Registro_ANS', types.VARCHAR(50), primary_key=True),
        Column('CNPJ', types.VARCHAR(20)),
        Column('Razao_Social', types.TEXT),
        Column('Nome_Fantasia', types.TEXT),
        Column('Modalidade', types.VARCHAR(50)),
        Column('Logradouro', types.TEXT),
        Column('Numero', types.VARCHAR(20)),
        Column('Complemento', types.TEXT),
        Column('Bairro', types.VARCHAR(50)),
        Column('Cidade', types.VARCHAR(50)),
        Column('UF', types.VARCHAR(2)),
        Column('CEP', types.VARCHAR(10)),
        Column('DDD', types.VARCHAR(5)),
        Column('Telefone', types.VARCHAR(20)),
        Column('Fax', types.VARCHAR(20)),
        Column('Endereco_eletronico', types.TEXT),
        Column('Representante', types.TEXT),
        Column('Cargo_Representante', types.TEXT),
        Column('Regiao_de_Comercializacao', types.INTEGER),
        Column('Data_Registro_ANS', types.DATE)
    )
    metadata.create_all(engine)


def prepare_data(df):

 
    df['Data_Registro_ANS'] = pd.to_datetime(
        df['Data_Registro_ANS'],
        format='%d/%m/%Y',
        errors='coerce'
    )


    df['Registro_ANS'] = df['Registro_ANS'].astype(str).str.strip()

    return df.dropna(subset=['Registro_ANS'])


def import_to_mysql(df, table_name, engine):

    try:
        with engine.begin() as conn:
      
            if not conn.dialect.has_table(conn, table_name):
                create_table_if_not_exists(engine, table_name)
                print(f"Tabela {table_name} criada com sucesso!")

         
            conn.execute(text(f"SET FOREIGN_KEY_CHECKS = 0"))
            conn.execute(text(f"TRUNCATE TABLE {table_name}"))


        df.to_sql(
            table_name,
            con=engine,
            if_exists='append',
            index=False,
            dtype=get_dtype_mapping(),
            chunksize=5000
        )

        with engine.connect() as conn:
            conn.execute(text(f"SET FOREIGN_KEY_CHECKS = 1"))
        return True
    except Exception as e:
        print(f"Erro ao importar para {table_name}: {e}")
        return False


def verify_import(engine, table_name):

    try:
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
            count = result.scalar()
            print(f"Total de registros em {table_name}: {count}")

            result = conn.execute(text(f"SELECT * FROM {table_name} LIMIT 1"))
            print("\nExemplo de registro:")
            print(dict(result.mappings().first()))
    except Exception as e:
        print(f"Erro ao verificar importação: {e}")


def main():

    try:
        print("\n=== INICIANDO IMPORTACAO DE OPERADORAS ===")
        engine = get_db_engine()

        print("Carregando arquivo CSV...")
        df = load_csv(CSV_PATH_OPERADORAS)
        df = prepare_data(df)


        print("Importando para o banco de dados...")
        if import_to_mysql(df, "operadoras", engine):
            print("Importação concluída com sucesso!")
            verify_import(engine, "operadoras")
        else:
            print("Falha na importação!")

    except Exception as e:
        print(f"\nERRO: {str(e)}")
    finally:
        if 'engine' in locals():
            engine.dispose()


if __name__ == "__main__":
    main()