







import pandas as pd
from sqlalchemy import create_engine, types, text
import os
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial


DB_CONFIG = {
    "username": "root",
    "password": "123",
    "hostname": "localhost",
    "database": "ans_db",
    "port": 3306
}

CSV_DIRECTORY = "/home/daniel-pc/PycharmProjects/task-3-definitiva/data/"
TABLE_NAME = "dems_contabeis"
CHUNKSIZE = 10_000
MAX_WORKERS = 4 


def get_db_engine(pool_size=5):
    """Cria conexão com o MySQL com pool de conexões"""
    connection_string = f"mysql+pymysql://{DB_CONFIG['username']}:{DB_CONFIG['password']}@{DB_CONFIG['hostname']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    return create_engine(
        connection_string,
        pool_size=pool_size,
        max_overflow=10,
        pool_pre_ping=True
    )


def get_csv_files(directory):
    
    files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    if not files:
        raise FileNotFoundError(f"Nenhum arquivo CSV encontrado em {directory}")
    return [os.path.join(directory, f) for f in sorted(files)]


def load_csv(file_path):
 
    try:
        print(f"Processando: {os.path.basename(file_path)}")
        return pd.read_csv(
            file_path,
            sep=';',
            encoding='utf-8',
            low_memory=False,
            dtype={'REG_ANS': str, 'CD_CONTA_CONTABIL': str},
            parse_dates=['DATA'],
            dayfirst=True
        )
    except Exception as e:
        print(f"Erro ao ler {file_path}: {e}")
        raise


def get_dtype_mapping():

    return {
        'DATA': types.DATE,
        'REG_ANS': types.VARCHAR(50),
        'CD_CONTA_CONTABIL': types.VARCHAR(50),
        'DESCRICAO': types.TEXT,
        'VL_SALDO_INICIAL': types.DECIMAL(20, 2),
        'VL_SALDO_FINAL': types.DECIMAL(20, 2)
    }


def process_data(df):

    # Converter valores numéricos
    num_cols = ['VL_SALDO_INICIAL', 'VL_SALDO_FINAL']
    for col in num_cols:
        df[col] = (
            df[col].astype(str)
            .str.replace('.', '', regex=False)
            .str.replace(',', '.')
            .astype(float)
        )

    # Validar dados
    df = df.dropna(subset=['REG_ANS', 'CD_CONTA_CONTABIL'])
    df['REG_ANS'] = df['REG_ANS'].astype(str).str.strip()

    return df


def process_chunk(chunk, engine):

    try:
        chunk.to_sql(
            TABLE_NAME,
            con=engine,
            if_exists='append',
            index=False,
            dtype=get_dtype_mapping()
        )
        return len(chunk)
    except Exception as e:
        print(f"Erro ao importar chunk: {e}")
        return 0


def import_to_mysql(df, engine):

    try:
        with engine.connect() as conn:
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))  # Desabilita chaves estrangeiras
            conn.commit()

        # Dividir o DataFrame em chunks
        chunks = [df[i:i + CHUNKSIZE] for i in range(0, len(df), CHUNKSIZE)]
        total_imported = 0

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [executor.submit(process_chunk, chunk, engine) for chunk in chunks]
            for future in as_completed(futures):
                total_imported += future.result()

        with engine.connect() as conn:
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))  # Reabilita chaves estrangeiras
            conn.commit()

        return total_imported

    except Exception as e:
        print(f"Erro na importação paralela: {e}")
        raise




def process_file(file, engine):

    try:
        df = load_csv(file)
        df = process_data(df)
        count = import_to_mysql(df, engine)
        print(f"Importados {count} registros de {os.path.basename(file)}")
        return count
    except Exception as e:
        print(f"Erro no arquivo {file}: {e}")
        print(traceback.format_exc())
        return 0


def main():

    try:
        print("\n=== INICIANDO IMPORTACAO DE DEMONSTRATIVOS ===")
        engine = get_db_engine()
        csv_files = get_csv_files(CSV_DIRECTORY)

        total_imported = 0

        # Processar arquivos em paralelo
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {executor.submit(process_file, file, engine): file for file in csv_files}

            for future in as_completed(futures):
                total_imported += future.result()

        print(f"\nTotal de registros importados: {total_imported}")

        # Verificação final
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {TABLE_NAME}"))
            print(f"\nTotal no banco de dados: {result.scalar()}")

    except Exception as e:
        print(f"\nERRO: {str(e)}")
    finally:
        if 'engine' in locals():
            engine.dispose()


if __name__ == "__main__":
    main()