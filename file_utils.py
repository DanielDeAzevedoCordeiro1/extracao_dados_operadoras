import os
import zipfile


def create_directories(directories):
    """Cria os diretórios necessários"""
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


def find_anexo_file(directory):
    """Encontra o arquivo de anexo no diretório especificado"""
    anexo_files = [f for f in os.listdir(directory)
                   if f.lower().endswith('.pdf') and 'anexo' in f.lower()]

    if not anexo_files:
        return None

    return os.path.join(directory, anexo_files[0])


def save_to_csv(df, path):
    """Salva o DataFrame em um arquivo CSV"""
    df.to_csv(path, index=False, encoding='utf-8-sig')
    return path


def create_zip(file_path, zip_path):
    """Compacta o arquivo em um ZIP"""
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(file_path, os.path.basename(file_path))
    return zip_path