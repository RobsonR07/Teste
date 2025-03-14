from config.settings import parametros
from extraction.google_sheets import extrair_dados
from transformation.clean_data import limpar_dados
from transformation.transform_data import transformar_dados
from load.database_connector import conectar_banco
from load.load_data import carregar_dados
from utils.logger import registrar_log

def executar_etl():
    dados_brutos = extrair_dados(parametros)
    dados_limpos = limpar_dados(dados_brutos)
    dados_transformados = transformar_dados(dados_limpos)
    conexao = conectar_banco(parametros)
    resultado = carregar_dados(conexao, dados_transformados)
    registrar_log("Processo ETL concluído com sucesso")
    return resultado

if __name__ == "__main__":
    executar_etl()
