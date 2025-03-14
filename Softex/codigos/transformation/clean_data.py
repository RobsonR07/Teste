import re
import pandas as pd

def limpar_dados(dados):
    cabecalho = dados[0]
    linhas_processadas = []
    for linha in dados[1:]:
        if len(linha) < len(cabecalho):
            linha = linha + [None] * (len(cabecalho) - len(linha))
        elif len(linha) > len(cabecalho):
            linha = linha[:len(cabecalho)]
        linhas_processadas.append(linha)
    df = pd.DataFrame(linhas_processadas, columns=cabecalho)
    colunas_remover = ["created_at", "last_modified", "last_moved", "start_date", "end_date"]
    df = df.drop(columns=colunas_remover, errors="ignore")
    emoji_pattern = re.compile("[" 
                               u"\U0001F600-\U0001F64F"
                               u"\U0001F300-\U0001F5FF"
                               u"\U0001F680-\U0001F6FF"
                               u"\U0001F1E0-\U0001F1FF"
                               u"\u2600-\u26FF"
                               u"\u2700-\u27BF"
                               "]+", flags=re.UNICODE)
    if "workflow" in df.columns:
        df["workflow"] = df["workflow"].astype(str).apply(lambda x: emoji_pattern.sub("", x))
    if "lane" in df.columns:
        df["lane"] = df["lane"].astype(str).apply(lambda x: emoji_pattern.sub("", x))
    
    # Remover linhas onde "item_id" é NULL, None ou uma string vazia
    if "item_id" in df.columns:
        df = df[df["item_id"].notna() & (df["item_id"].astype(str).str.strip() != "")]
    
    return df

