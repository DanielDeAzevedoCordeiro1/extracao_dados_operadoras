import pandas as pd
import tabula
import re
from PyPDF2 import PdfReader


def extract_tables(pdf_path):
    """Extrai as tabelas de Rol de Procedimentos do PDF"""
    print(f"Extraindo tabelas de: {pdf_path}")

    with open(pdf_path, 'rb') as file:
        pdf = PdfReader(file)
        num_pages = len(pdf.pages)


    tables = tabula.read_pdf(
        pdf_path,
        pages='all',
        multiple_tables=True,
        lattice=True
    )


    rol_tables = [table for table in tables if not table.empty and 'PROCEDIMENTO' in table.columns]

    if not rol_tables:
        print("Nenhuma tabela do Rol de Procedimentos encontrada")
        return None

    return pd.concat(rol_tables, ignore_index=True)


def extract_legends(pdf_path):
    """Extrai as legendas para OD e AMB do PDF"""
    with open(pdf_path, 'rb') as file:
        pdf = PdfReader(file)
        text = " ".join([page.extract_text() for page in pdf.pages])

    legends = {
        'OD': re.search(r'OD[:\s]+([^;\n]+)', text),
        'AMB': re.search(r'AMB[:\s]+([^;\n]+)', text)
    }

    return {
        'OD': legends['OD'].group(1).strip() if legends['OD'] else "Odontologia",
        'AMB': legends['AMB'].group(1).strip() if legends['AMB'] else "Ambulatorial"
    }