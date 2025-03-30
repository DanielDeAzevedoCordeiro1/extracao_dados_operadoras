import os
from extractor import extract_tables, extract_legends
from processor import process_data
from file_utils import create_directories, find_anexo_file, save_to_csv, create_zip


def main():
  
    downloads_dir = "/home/daniel-pc/Documentos/"
    output = "./output"
    seu_nome = "Daniel" 



    create_directories([downloads_dir, output])

    pdf_path = find_anexo_file(downloads_dir)
    if not pdf_path:
        print("Nenhum arquivo de anexo encontrado.")
        return

    data = extract_tables(pdf_path)
    if data is None:
        return

    legends = extract_legends(pdf_path)
    data = process_data(data, legends)

    csv_path = os.path.join(output, "tabela_rol_procedimentos.csv")
    save_to_csv(data, csv_path)


    zip_path = os.path.join(output, f"Teste_{seu_nome}.zip")
    create_zip(csv_path, zip_path)

    print(f"Processamento concluído. Resultados salvos em: {zip_path}")


if __name__ == "__main__":
    main()