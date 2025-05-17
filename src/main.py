import streamlit as st
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import random
from datetime import date

# --- Autenticação Google Sheets ---
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

json_creds = st.secrets["google_service_account"]["json"]
creds_dict = json.loads(json_creds)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Nome da planilha que terá várias abas
SPREADSHEET_NAME = "ChoppsLeague"
spreadsheet = client.open(SPREADSHEET_NAME)

# Função para ler dados da aba, retorna dataframe
def ler_aba(nome_aba):
    try:
        worksheet = spreadsheet.worksheet(nome_aba)
        dados = worksheet.get_all_records()
        df = pd.DataFrame(dados)
        return df
    except Exception:
        # Aba não existe ou vazia
        return pd.DataFrame()

# Função para adicionar linha numa aba (cria a aba se não existir)
def adicionar_linha(nome_aba, linha):
    try:
        worksheet = spreadsheet.worksheet(nome_aba)
    except gspread.exceptions.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(title=nome_aba, rows="1000", cols="20")
        # Se quiser, pode adicionar cabeçalho manualmente aqui

    worksheet.append_row(linha)

# --- Dados fixos ---
times = ["Borrusia", "Time 2"]
jogadores = ["Matheus Moreira", "José Moreira", "Lucas", "Alex", "Gustavo",
            "Lula", "Juninho", "Jesus", "Gabriel", "Arthur",
            "Walter", "Eduardo", "Cristian", "Luciano", "Deivid"]

# Menu lateral
st.sidebar.title("Menu")
tela = st.sidebar.selectbox("Escolha a tela:",
                            ["Dashboard", "Registrar Partida", "Registrar Jogadores", "Sorteio Times"])

# --- Tela Dashboard ---
if tela == "Dashboard":
    st.title("Dashboard - Chopp's League")

    st.subheader("Estatísticas de Partidas")
    df_partidas = ler_aba("Partidas")
    if not df_partidas.empty:
        st.dataframe(df_partidas)
        # Você pode colocar gráficos aqui usando st.bar_chart, st.line_chart etc.
        placares = df_partidas[['Placar Time 1', 'Placar Time 2']]
        st.bar_chart(placares)
    else:
        st.write("Nenhuma partida registrada.")

# --- Tela Registrar Partida ---
elif tela == "Registrar Partida":
    st.title("Registrar nova partida")

    with st.form("form_partida"):
        data_partida = st.date_input("Data da partida", value=date.today())
        time_1 = st.selectbox("Time 1", times, index=0)
        placar_1 = st.number_input("Placar Time 1", min_value=0, step=1)
        time_2 = st.selectbox("Time 2", times, index=1)
        placar_2 = st.number_input("Placar Time 2", min_value=0, step=1)

        submit = st.form_submit_button("Salvar partida")

        if submit:
            nova_linha = [
                str(data_partida),
                time_1,
                placar_1,
                time_2,
                placar_2
            ]
            adicionar_linha("Partidas", nova_linha)
            st.success("Partida registrada com sucesso!")

# --- Tela Registrar Jogadores ---
elif tela == "Registrar Jogadores":
    st.title("Registrar estatísticas dos jogadores")

    df_jogadores = ler_aba("Jogadores")
    jogadores_cadastrados = df_jogadores["Nome"].tolist() if not df_jogadores.empty else []

    with st.form("form_jogadores"):
        nome = st.selectbox("Jogador", jogadores)
        if nome in jogadores_cadastrados:
            st.info(f"Já existe estatísticas para o jogador {nome}.")
        gols = st.number_input("Gols", min_value=0, step=1)
        assistencias = st.number_input("Assistências", min_value=0, step=1)
        faltas = st.number_input("Faltas", min_value=0, step=1)
