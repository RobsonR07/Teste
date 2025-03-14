import pandas as pd
from datetime import datetime

def converter_data_extenso_manual(data_str):
    if pd.isnull(data_str):
        return None
    data_str = str(data_str).strip()

    if ',' in data_str:
        partes = data_str.split(',')
        if len(partes) > 1:
            data_str = partes[1].strip()
    partes_data = data_str.split(" de ")
    if len(partes_data) != 3:
        return None
    dia = partes_data[0].strip()
    mes_texto = partes_data[1].strip().lower()
    ano = partes_data[2].strip()
    meses = {
        "janeiro": "01",
        "fevereiro": "02",
        "março": "03",
        "marco": "03",
        "abril": "04",
        "maio": "05",
        "junho": "06",
        "julho": "07",
        "agosto": "08",
        "setembro": "09",
        "outubro": "10",
        "novembro": "11",
        "dezembro": "12"
    }
    mes_num = meses.get(mes_texto)
    if not mes_num:
        return None
    return f"{ano}-{mes_num}-{dia.zfill(2)}"

def transformar_dados(df):

    if "Data_inicio_entrega" in df.columns:
        df["Data_inicio_entrega"] = pd.to_datetime(
            df["Data_inicio_entrega"], errors="coerce", dayfirst=True
        ).dt.strftime("%Y-%m-%d")
    if "Data_Fim_Entrega" in df.columns:
        df["Data_Fim_Entrega"] = pd.to_datetime(
            df["Data_Fim_Entrega"], format="%d/%m/%Y %H:%M:%S", errors="coerce"
        ).dt.strftime("%Y-%m-%d %H:%M:%S")
    for coluna in ["planned_start_date", "planned_end_date", "deadline", "target_date"]:
        if coluna in df.columns:
            df[coluna] = df[coluna].apply(lambda x: converter_data_extenso_manual(x) if isinstance(x, str) else x)

    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    df_items = df.copy()
    
    if "board" in df_items.columns:
        df_items["board"] = df_items["board"].astype(str)
        df_board = df_items[["board"]].drop_duplicates().reset_index(drop=True)
        df_board["board_id"] = df_board.index + 1
        df_items = df_items.merge(df_board, on="board", how="left")
        df_items["board_id"] = df_items["board_id"].fillna(0).astype(int)
    else:
        df_board = pd.DataFrame()
    
    if "lane" in df_items.columns:
        df_items["lane"] = df_items["lane"].astype(str)
        df_lane = df_items[["lane"]].drop_duplicates().reset_index(drop=True)
        df_lane["lane_id"] = df_lane.index + 1
        df_items = df_items.merge(df_lane, on="lane", how="left")
        df_items["lane_id"] = df_items["lane_id"].fillna(0).astype(int)
    else:
        df_lane = pd.DataFrame()
    
    if "workflow" in df_items.columns:
        df_items["workflow"] = df_items["workflow"].astype(str)
        df_workflow = df_items[["workflow"]].drop_duplicates().reset_index(drop=True)
        df_workflow = df_workflow[~df_workflow["workflow"].str.lower().eq("none")].reset_index(drop=True)
        df_workflow["workflow_id"] = df_workflow.index + 1
        df_items = df_items.merge(df_workflow, on="workflow", how="left")
        df_items["workflow_id"] = df_items["workflow_id"].fillna(0).astype(int)
    else:
        df_workflow = pd.DataFrame()
    
    df_items.drop(columns=["board", "lane", "workflow", "Quadro"], errors="ignore", inplace=True)
    
    return {"items": df_items, "board": df_board, "lane": df_lane, "workflow": df_workflow}
