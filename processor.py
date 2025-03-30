def process_data(df, legends):
    """Processa e limpa os dados da tabela"""

    for col in ['OD', 'AMB']:
        if col in df.columns:
            mask = ~df[col].isna()
            df.loc[mask, col] = legends[col]

    return df.dropna(how='all').reset_index(drop=True)