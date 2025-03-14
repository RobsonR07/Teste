import streamlit as st
import pandas as pd
import altair as alt
from sqlalchemy import create_engine

def get_engine():
    parametros = {
        "db_host": "localhost",
        "db_port": 3306,
        "db_nome": "softex",
        "db_usuario": "root",
        "db_senha": "root"
    }
    return create_engine(
        f"mysql+pymysql://{parametros['db_usuario']}:{parametros['db_senha']}@{parametros['db_host']}:{parametros['db_port']}/{parametros['db_nome']}"
    )

@st.cache_resource
def load_data(query):
    engine = get_engine()
    return pd.read_sql(query, con=engine)

def preprocess_data(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    df["data_fim_entrega"] = pd.to_datetime(df["data_fim_entrega"], errors="coerce")
    df["deadline"] = pd.to_datetime(df["deadline"], errors="coerce")
    df["work_progress_value"] = pd.to_numeric(df["work_progress_value"], errors="coerce")
    df['block_time'] = df['block_time'].astype(str).str.replace(',', '.').astype(float).round(2)
    return df

def quantidade_entregas(df):
    df_concluidos = df[(df['work_progress_value'] == 100) & df['data_fim_entrega'].notna()]
    df_nao_iniciados = df[df['work_progress_value'] == 0]
    df_atraso = df_concluidos[(df_concluidos['data_fim_entrega'] > df_concluidos['deadline']) & df_concluidos['deadline'].notna()]
    df_em_dia = df_concluidos[(df_concluidos['data_fim_entrega'] <= df_concluidos['deadline']) & df_concluidos['deadline'].notna()]
    return len(df_atraso), len(df_em_dia), len(df_nao_iniciados)

def exibir_dashboard(df, df_boards):
    st.title("Dashboard de Entregas - Softex")
    st.header("1. Quantidade de Entregas por Status")
    
    quantidade_atraso, quantidade_em_dia, quantidade_nao_iniciadas = quantidade_entregas(df)
    df_status = pd.DataFrame({
        "Categoria": ["Em atraso", "Em dia", "Não iniciados"],
        "Quantidade": [quantidade_atraso, quantidade_em_dia, quantidade_nao_iniciadas]
    })
    st.subheader("Quantidade de Entregas")
    st.bar_chart(df_status.set_index("Categoria"))
    
    st.header("2. Quantidade de Projetos")
    num_projetos = df_boards[df_boards["board"].notnull()]["board"].nunique()
    st.metric("Número de Projetos", num_projetos)
    
    st.header("3. Bloqueios: Razões e Tempo Total Bloqueado")
    df_bloqueados = df[df["is_blocked"].astype(str).str.lower() == "yes"]
    quantidade_bloqueados = len(df_bloqueados)
    st.subheader("Quantidade de Itens Bloqueados")
    st.write(f"🔒 **Total de itens bloqueados:** {quantidade_bloqueados}")
    
    if quantidade_bloqueados > 0:
        df_bloqueados_resultado = df_bloqueados[['item_id', 'block_reason', 'block_time']]
        st.subheader("Motivos do Bloqueio")
        st.dataframe(df_bloqueados_resultado)
    else:
        st.write("✅ Nenhum item bloqueado no momento.")
    
    tempo_total_bloqueio = df['block_time'].sum()
    st.subheader("Tempo Total de Itens Bloqueados")
    st.write(f"⏳ **Tempo total de bloqueio:** {tempo_total_bloqueio:.2f} horas")
    
    st.header("4. Entregas por Natureza do Item")
    if "natureza_do_item" in df.columns:
        df_natureza = df.groupby("natureza_do_item").size().reset_index(name="quantidade")
        chart_natureza = alt.Chart(df_natureza).mark_bar().encode(
            x=alt.X("natureza_do_item:N", title="Natureza do Item"),
            y=alt.Y("quantidade:Q", title="Quantidade de Entregas")
        ).properties(width=600, height=400)
        st.altair_chart(chart_natureza)
    else:
        st.write("⚠️ Coluna 'natureza_do_item' não encontrada.")


df = preprocess_data(load_data("SELECT * FROM items"))
df_boards = load_data("SELECT * FROM board")
exibir_dashboard(df, df_boards)
