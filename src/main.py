import streamlit as st
import requests
from io import BytesIO
from PIL import Image
import pandas as pd
import random
import os

# Arquivos CSV para armazenar dados localmente
FILE_PARTIDAS = "partidas.csv"
FILE_JOGADORES = "jogadores.csv"

# Inicializa os dados ou cria arquivos vazios se não existirem
def init_data():
    if not os.path.exists(FILE_PARTIDAS):
        df = pd.DataFrame(columns=[
            "Data", "Time 1", "Time 2", "Placar Time 1", "Placar Time 2", "Local"
        ])
        df.to_csv(FILE_PARTIDAS, index=False)

    if not os.path.exists(FILE_JOGADORES):
        df = pd.DataFrame(columns=[
            "Nome", "Time", "Gols", "Assistências", "Faltas", "Cartões Amarelos", "Cartões Vermelhos"
        ])
        df.to_csv(FILE_JOGADORES, index=False)

# Função para carregar dados
def load_data():
    partidas = pd.read_csv(FILE_PARTIDAS)
    jogadores = pd.read_csv(FILE_JOGADORES)
    return partidas, jogadores

# Função para salvar dados
def save_data(partidas, jogadores):
    partidas.to_csv(FILE_PARTIDAS, index=False)
    jogadores.to_csv(FILE_JOGADORES, index=False)

#Tela Principal com gráficos simples e indicadores
def tela_principal(partidas, jogadores):
    st.title("Chopp's League")

    st.markdown("Bem-vindo à pelada entre amigos!")

    col1, col2 = st.columns(2)

    with col1:
        image = Image.open("./imagens/borrusia_escudo.jpg")
        st.image(image, caption="Borussia", use_container_width=True)

    with col2:
        image = Image.open("./imagens/inter_escudo.jpg")
        st.image(image, caption="Inter", use_container_width=True)

    st.header("Resumo das Partidas")
    st.write(f"Total de partidas registradas: {len(partidas)}")
    if not partidas.empty:
        st.write("Última partida registrada:")
        st.write(partidas.tail(1))

    st.header("Resumo dos Jogadores")
    st.write(f"Total de jogadores registrados: {len(jogadores)}")
    if not jogadores.empty:
        gols_totais = jogadores["Gols"].sum()
        st.write(f"Gols totais: {gols_totais}")

        # Gráfico de gols por jogador
        gols_por_jogador = jogadores.groupby("Nome")["Gols"].sum().sort_values(ascending=False)
        st.bar_chart(gols_por_jogador)

# Exemplo de carregamento seguro:
def load_data_safe():
    try:
        partidas = pd.read_csv("partidas/estatisticas_partidas.csv")
    except (FileNotFoundError, pd.errors.EmptyDataError):
        partidas = pd.DataFrame(columns=["Data", "Partida", "Borussia", "Inter de Milão"])

    try:
        jogadores = pd.read_csv("jogadores/jogadores.csv")
    except (FileNotFoundError, pd.errors.EmptyDataError):
        jogadores = pd.DataFrame(columns=["Nome", "Time", "Gols", "Assistências", "Faltas", "Cartões Amarelos", "Cartões Vermelhos"])

    return partidas, jogadores

# Carrega os dados antes de chamar tela_principal
partidas, jogadores = load_data_safe()

#Tela para registrar estatísticas da partida
def tela_partida(partidas):
    st.title("Registrar Estatísticas da Partida")

    with st.form("form_partida", clear_on_submit=True):
        data = st.date_input("Data da partida")
        time1 = st.selectbox("Time 1", ["Borrusia", "Time 2"])
        time2 = "Borrusia" if time1 == "Time 2" else "Time 2"
        placar1 = st.number_input(f"Placar {time1}", min_value=0, step=1)
        placar2 = st.number_input(f"Placar {time2}", min_value=0, step=1)
        local = st.text_input("Local da partida")

        submit = st.form_submit_button("Registrar")

        if submit:
            nova_partida = {
                "Data": data,
                "Time 1": time1,
                "Time 2": time2,
                "Placar Time 1": placar1,
                "Placar Time 2": placar2,
                "Local": local,
            }
            partidas = partidas.append(nova_partida, ignore_index=True)
            partidas.to_csv(FILE_PARTIDAS, index=False)
            st.success("Partida registrada com sucesso!")

    st.write("Partidas registradas:")
    st.dataframe(partidas)

    return partidas

# Tela para registrar estatísticas dos jogadores
def tela_jogadores(jogadores):
    st.title("Registrar Estatísticas dos Jogadores")

    jogadores_lista = [
        "Matheus Moreira", "José Moreira", "Lucas", "Alex", "Gustavo",
        "Lula", "Juninho", "Jesus", "Gabriel", "Arthur",
        "Walter", "Eduardo", "Cristian", "Luciano", "Deivid"
    ]

    times = ["Borrusia", "Time 2"]

    with st.form("form_jogadores", clear_on_submit=True):
        nome = st.selectbox("Jogador", jogadores_lista)
        time = st.selectbox("Time", times)
        gols = st.number_input("Gols", min_value=0, step=1)
        assistencias = st.number_input("Assistências", min_value=0, step=1)
        faltas = st.number_input("Faltas", min_value=0, step=1)
        cart_amarelos = st.number_input("Cartões Amarelos", min_value=0, step=1)
        cart_vermelhos = st.number_input("Cartões Vermelhos", min_value=0, step=1)

        submit = st.form_submit_button("Registrar")

        if submit:
            registro = {
                "Nome": nome,
                "Time": time,
                "Gols": gols,
                "Assistências": assistencias,
                "Faltas": faltas,
                "Cartões Amarelos": cart_amarelos,
                "Cartões Vermelhos": cart_vermelhos
            }
            jogadores = jogadores.append(registro, ignore_index=True)
            jogadores.to_csv(FILE_JOGADORES, index=False)
            st.success("Estatísticas do jogador registradas com sucesso!")

    st.write("Estatísticas registradas dos jogadores:")
    st.dataframe(jogadores)

    return jogadores

# Tela para sorteio dos times
def tela_sorteio():
    st.title("Sorteio de Times")

    jogadores_lista = [
        "Matheus Moreira", "José Moreira", "Lucas", "Alex", "Gustavo",
        "Lula", "Juninho", "Jesus", "Gabriel", "Arthur",
        "Walter", "Eduardo", "Cristian", "Luciano", "Deivid"
    ]

    if st.button("Sortear times"):
        random.shuffle(jogadores_lista)
        time1 = jogadores_lista[:len(jogadores_lista)//2]
        time2 = jogadores_lista[len(jogadores_lista)//2:]
        st.write("**Time 1 (Borrusia):**")
        for jogador in time1:
            st.write("- " + jogador)
        st.write("**Time 2:**")
        for jogador in time2:
            st.write("- " + jogador)

# Garante que a pasta "usuarios" existe
os.makedirs("usuarios", exist_ok=True)

# Caminhos dos arquivos (dentro da pasta criada)
# Define o diretório base (onde o script está localizado)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PASTA_USUARIOS = os.path.join(BASE_DIR, "usuarios")

# Cria a pasta 'usuarios' se não existir
os.makedirs(PASTA_USUARIOS, exist_ok=True)

## Define os caminhos dos arquivos
PASTA_USUARIOS = "usuarios"
os.makedirs(PASTA_USUARIOS, exist_ok=True)
FILE_USUARIOS = os.path.join(PASTA_USUARIOS, "cadastro.csv")
FILE_PRESENCAS = os.path.join(PASTA_USUARIOS, "presenca.csv")

def tela_presenca_login():
    st.title("Cadastro, Login e Confirmação de Presença")

    # Carrega os dados dos usuários com tratamento para arquivos vazios
    if os.path.exists(FILE_USUARIOS):
        try:
            usuarios = pd.read_csv(FILE_USUARIOS)
        except pd.errors.EmptyDataError:
            usuarios = pd.DataFrame(columns=["Nome", "Email", "Senha"])
    else:
        usuarios = pd.DataFrame(columns=["Nome", "Email", "Senha"])

    # Carrega as presenças com tratamento para arquivos vazios
    if os.path.exists(FILE_PRESENCAS):
        try:
            presencas = pd.read_csv(FILE_PRESENCAS)
        except pd.errors.EmptyDataError:
            presencas = pd.DataFrame(columns=["Nome", "Email"])
    else:
        presencas = pd.DataFrame(columns=["Nome", "Email"])

    # Inicializa o estado da sessão
    if "usuario_logado" not in st.session_state:
        st.session_state.usuario_logado = None

    # Tela de login ou cadastro
    if not st.session_state.usuario_logado:
        aba = st.radio("Selecione uma opção:", ["🔐 Login", "📝 Cadastro"])

        if aba == "🔐 Login":
            with st.form("form_login"):
                email = st.text_input("E-mail")
                senha = st.text_input("Senha", type="password")
                login = st.form_submit_button("Entrar")

                if login:
                    user = usuarios[(usuarios["Email"] == email) & (usuarios["Senha"] == senha)]
                    if not user.empty:
                        st.session_state.usuario_logado = user.iloc[0].to_dict()
                        st.success(f"Bem-vindo, {user.iloc[0]['Nome']}!")
                        st.experimental_rerun()
                    else:
                        st.error("E-mail ou senha incorretos.")

        elif aba == "📝 Cadastro":
            with st.form("form_cadastro", clear_on_submit=True):
                nome = st.text_input("Nome completo")
                email = st.text_input("E-mail")
                senha = st.text_input("Senha", type="password")
                submit = st.form_submit_button("Cadastrar")

                if submit:
                    if not nome or not email or not senha:
                        st.warning("Preencha todos os campos.")
                    elif email in usuarios["Email"].values:
                        st.warning("Este e-mail já está cadastrado.")
                    else:
                        novo_usuario = {"Nome": nome, "Email": email, "Senha": senha}
                        usuarios = pd.concat([usuarios, pd.DataFrame([novo_usuario])], ignore_index=True)
                        usuarios.to_csv(FILE_USUARIOS, index=False)
                        st.success("Cadastro realizado! Faça login para confirmar presença.")
                        st.write(f"📁 Dados salvos em: `{FILE_USUARIOS}`")

    else:
        usuario = st.session_state.usuario_logado
        st.success(f"Logado como: {usuario['Nome']} ({usuario['Email']})")

        if usuario["Email"] in presencas["Email"].values:
            st.info("✅ Presença já confirmada.")
        else:
            if st.button("Confirmar Presença"):
                nova_presenca = {"Nome": usuario["Nome"], "Email": usuario["Email"]}
                presencas = pd.concat([presencas, pd.DataFrame([nova_presenca])], ignore_index=True)
                presencas.to_csv(FILE_PRESENCAS, index=False)
                st.success("Presença confirmada com sucesso!")
                st.write(f"📁 Presença salva em: `{FILE_PRESENCAS}`")

        if st.button("Sair"):
            st.session_state.usuario_logado = None
            st.experimental_rerun()

# Menu lateral para navegação
with st.sidebar:
    image = Image.open("./imagens/logo.png")  # Substitua "logo.png" pelo nome do seu arquivo
    st.image(image, caption="Chopp's League", use_container_width =True)
    pagina = st.selectbox("Navegue pelo app:", [
        "🏠 Tela Principal",
        "📊 Estatísticas da Partida",
        "👟 Estatísticas dos Jogadores",
        "🎲 Sorteio de Times",
        "✅ Presença e Login",  # ADICIONAR ESTA LINHA
    ])

# Controle de navegação
if pagina == "🏠 Tela Principal":
    tela_principal(partidas)
elif pagina == "📊 Estatísticas da Partida":
    partidas = tela_partida(partidas)
elif pagina == "👟 Estatísticas dos Jogadores":
    jogadores = tela_jogadores(jogadores)
elif pagina == "🎲 Sorteio de Times":
    tela_sorteio()
elif pagina == "✅ Presença e Login":
    tela_presenca_login()