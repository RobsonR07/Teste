def carregar_dados(engine, dados):
    for tabela, df in dados.items():
        if not df.empty:
            df.to_sql(tabela, con=engine, if_exists="replace", index=False)
    return True
