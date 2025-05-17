import streamlit as st
import pandas as pd
import os

# Arquivos CSV para armazenar dados
PARTIDAS_CSV = "partidas.csv"
ESTATISTICAS_CSV = "estatisticas_jogadores.csv"

# Times e jogadores fixos
TIMES = ["Borrusia", "Inter"]
JOGADORES = [
    "Matheus Moreira", "José Moreira", "Lucas", "Alex", "Gustavo", "Lula",
    "Juninho", "Jesus", "Gabriel", "Arthur", "Walter", "Eduardo", "Cristian",
    "Luciano", "Deivid"
]

# --- Função para carregar CSV (cria vazio se não existir) ---
def carregar_csv(nome_arquivo, colunas):
    if os.path.exists(nome_arquivo):
        return pd.read_csv(nome_arquivo)
    else:
        return pd.DataFrame(columns=colunas)

# --- Carregar bases ---
df_partidas = carregar_csv(PARTIDAS_CSV, ["ID", "Rodada", "Data", "Time 1", "Gols T1", "Time 2", "Gols T2", "Local"])
df_estats = carregar_csv(ESTATISTICAS_CSV, ["Partida ID", "Jogador", "Time", "Gols", "Assistências", "Cartões", "Presente"])

st.title("📊 Chopp's League - Registro de Partidas e Estatísticas")

# ------------------------
# Registrar nova partida
# ------------------------
st.header("➕ Registrar nova partida")

with st.form("form_partida"):
    rodada = st.number_input("Rodada", min_value=1, step=1)
    data = st.date_input("Data da partida")
    time1 = st.selectbox("Time 1", TIMES)
    time2 = st.selectbox("Time 2", [t for t in TIMES if t != time1])
    gols_t1 = st.number_input(f"Gols {time1}", min_value=0, step=1)
    gols_t2 = st.number_input(f"Gols {time2}", min_value=0, step=1)
    local = st.text_input("Local da partida")
    enviar_partida = st.form_submit_button("Salvar partida")

if enviar_partida:
    nova_id = 1 if df_partidas.empty else df_partidas["ID"].max() + 1
    nova_partida = {
        "ID": nova_id,
        "Rodada": rodada,
        "Data": data,
        "Time 1": time1,
        "Gols T1": gols_t1,
        "Time 2": time2,
        "Gols T2": gols_t2,
        "Local": local
    }
    df_partidas = pd.concat([df_partidas, pd.DataFrame([nova_partida])], ignore_index=True)
    df_partidas.to_csv(PARTIDAS_CSV, index=False)
    st.success(f"Partida {nova_id} registrada com sucesso! Agora registre as estatísticas dos jogadores abaixo.")
else:
    nova_id = None

# ------------------------
# Registrar estatísticas dos jogadores para a última partida inserida
# ------------------------
if nova_id is None and not df_partidas.empty:
    # Se não foi enviada agora, pegar a última partida registrada
    nova_id = df_partidas["ID"].max()

st.header("📝 Registrar estatísticas dos jogadores")

if nova_id is None:
    st.info("Cadastre uma partida para começar a inserir estatísticas dos jogadores.")
else:
    st.write(f"Registrando estatísticas da partida ID: {nova_id}")

    # Selecionar jogadores do time 1 e 2 para facilitar
    partida = df_partidas.loc[df_partidas["ID"] == nova_id].iloc[0]
    time1 = partida["Time 1"]
    time2 = partida["Time 2"]

    jogadores_time1 = st.multiselect(f"Jogadores do {time1} (selecione presentes)", JOGADORES, key="time1")
    jogadores_time2 = st.multiselect(f"Jogadores do {time2} (selecione presentes)", JOGADORES, key="time2")

    def registrar_stats(time, jogadores_selecionados):
        stats_list = []
        st.write(f"**Estatísticas para jogadores do {time}**")
        for jogador in jogadores_selecionados:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                gols = st.number_input(f"Gols - {jogador}", min_value=0, step=1, key=f"gols_{jogador}")
            with col2:
                assists = st.number_input(f"Assistências - {jogador}", min_value=0, step=1, key=f"assists_{jogador}")
            with col3:
                cartoes = st.number_input(f"Cartões - {jogador}", min_value=0, step=1, key=f"cartoes_{jogador}")
            with col4:
                presente = True  # já que o jogador foi selecionado
            stats_list.append({
                "Partida ID": nova_id,
                "Jogador": jogador,
                "Time": time,
                "Gols": gols,
                "Assistências": assists,
                "Cartões": cartoes,
                "Presente": presente
            })
        return stats_list

    if st.button("Salvar estatísticas dos jogadores"):
        stats_time1 = registrar_stats(time1, jogadores_time1)
        stats_time2 = registrar_stats(time2, jogadores_time2)
        novas_stats = stats_time1 + stats_time2

        # Remover estatísticas antigas dessa partida (se houver)
        df_estats = df_estats[df_estats["Partida ID"] != nova_id]
        # Acrescentar as novas
        df_estats = pd.concat([df_estats, pd.DataFrame(novas_stats)], ignore_index=True)
        df_estats.to_csv(ESTATISTICAS_CSV, index=False)
        st.success("Estatísticas salvas com sucesso!")

# ------------------------
# Visualizar dados já cadastrados
# ------------------------
st.header("📋 Histórico de partidas")
st.dataframe(df_partidas.sort_values(by=["Rodada", "Data"]), use_container_width=True)

st.header("📋 Estatísticas dos jogadores")
if not df_estats.empty:
    st.dataframe(df_estats, use_container_width=True)
else:
    st.info("Ainda não há estatísticas registradas.")

# ------------------------
# Estatísticas resumidas simples
# ------------------------
st.header("🏆 Ranking de artilheiros (gols acumulados)")

if not df_estats.empty:
    resumo_gols = df_estats.groupby("Jogador")["Gols"].sum().sort_values(ascending=False).reset_index()
    st.table(resumo_gols)
else:
    st.info("Registre algumas estatísticas para ver o ranking.")