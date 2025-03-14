from google.oauth2 import service_account
from googleapiclient.discovery import build

def extrair_dados(parametros):
    id_planilha = parametros['id_planilha']
    intervalo = parametros['intervalo']
    caminho_credenciais = parametros['caminho_credenciais']
    escopos = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    credenciais = service_account.Credentials.from_service_account_file(caminho_credenciais, scopes=escopos)
    servico = build('sheets', 'v4', credentials=credenciais)
    resultado = servico.spreadsheets().values().get(spreadsheetId=id_planilha, range=intervalo).execute()
    dados = resultado.get('values', [])
    return dados
