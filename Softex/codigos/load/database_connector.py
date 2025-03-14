from sqlalchemy import create_engine

def conectar_banco(parametros):
    db_host = parametros["db_host"]
    db_port = parametros["db_port"]
    db_nome = parametros["db_nome"]
    db_usuario = parametros["db_usuario"]
    db_senha = parametros["db_senha"]
    engine = create_engine(
        f"mysql+pymysql://{db_usuario}:{db_senha}@{db_host}:{db_port}/{db_nome}",
        echo=False
    )
    return engine
