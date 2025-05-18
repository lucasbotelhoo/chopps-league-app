import streamlit as st
import requests
from io import BytesIO
from PIL import Image
import pandas as pd
import random
import os
import re


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

# Função para formatar telefone com nono dígito fixo
def formatar_telefone_9fixo(numero):
    if len(numero) == 11:
        return f"({numero[:2]}) {numero[2:7]}-{numero[7:]}"
    return numero

# Tela de cadastro e login
def tela_presenca_login():
    st.title("Cadastro, Login e Confirmação de Presença")

    # Inicializa estados
    if "telefone_raw" not in st.session_state:
        st.session_state["telefone_raw"] = ""
    if "nome" not in st.session_state:
        st.session_state["nome"] = ""
    if "email" not in st.session_state:
        st.session_state["email"] = ""
    if "senha" not in st.session_state:
        st.session_state["senha"] = ""
    if "posicao" not in st.session_state:
        st.session_state["posicao"] = ""
    if "nascimento" not in st.session_state:
        st.session_state["nascimento"] = None

    if not st.session_state.get("usuario_logado", False):
        aba = st.radio("Selecione uma opção:", ["🔐 Login", "📝 Cadastro"])

        if aba == "📝 Cadastro":
            # Tratamento do telefone ANTES do formulário
            telefone_input = st.text_input(
                "Número de telefone (somente números, com DDD)",
                value=st.session_state["telefone_raw"],
                key="telefone_input"
            )

            # Mantém somente dígitos
            numeros = re.sub(r'\D', '', telefone_input)
            # Limita a 11 dígitos
            numeros = numeros[:11]

            # Atualiza valor do campo se necessário
            if numeros != re.sub(r'\D', '', st.session_state["telefone_raw"]):
                st.session_state["telefone_raw"] = numeros
                st.experimental_rerun()

            # Formulário de cadastro
            with st.form("form_cadastro"):
                nome = st.text_input("Nome completo", value=st.session_state["nome"])
                email = st.text_input("E-mail", value=st.session_state["email"])
                senha = st.text_input("Senha", type="password", value=st.session_state["senha"])
                posicao = st.selectbox("Posição que joga", ["", "Linha", "Goleiro"],
                                       index=["", "Linha", "Goleiro"].index(st.session_state["posicao"]) if st.session_state["posicao"] else 0)
                nascimento = st.date_input("Data de nascimento", value=st.session_state["nascimento"])

                submit = st.form_submit_button("Cadastrar")

                if submit:
                    # Salva valores preenchidos
                    st.session_state["nome"] = nome
                    st.session_state["email"] = email
                    st.session_state["senha"] = senha
                    st.session_state["posicao"] = posicao
                    st.session_state["nascimento"] = nascimento

                    if len(numeros) != 11:
                        st.warning("Número de telefone inválido. Deve conter exatamente 11 dígitos.")
                    elif not nome or not email or not senha or not posicao or not nascimento:
                        st.warning("Preencha todos os campos.")
                    else:
                        telefone_formatado = formatar_telefone_9fixo(numeros)
                        st.session_state["telefone_raw"] = telefone_formatado
                        st.success(f"Cadastro realizado com sucesso!\nTelefone formatado: {telefone_formatado}")

        elif aba == "🔐 Login":
            with st.form("form_login", clear_on_submit=True):
                email_login = st.text_input("E-mail", key="email_login")
                senha_login = st.text_input("Senha", type="password", key="senha_login")
                submit_login = st.form_submit_button("Entrar")

                if submit_login:
                    if email_login and senha_login:
                        st.session_state["usuario_logado"] = True
                        st.success(f"Usuário {email_login} logado com sucesso!")
                    else:
                        st.warning("Preencha email e senha para login.")
    else:
        st.write("Usuário já está logado!")
        if st.button("Confirmar Presença"):
            st.success("Presença confirmada. Obrigado!")
            
# Regras Oficiais
def tela_regras():
    # Título principal maior, não quebra linha
    st.markdown(
        """
        <h1 style="font-size:32px; white-space: nowrap; overflow-x: auto; margin-bottom: 0.5em;">
            📜 Regras Oficiais – Chopp's League
        </h1>
        """,
        unsafe_allow_html=True
    )

    # Subtítulos menores que o título principal
    def subtitulo(texto):
        st.markdown(f'<h3 style="font-size:20px; margin-top: 1em;">{texto}</h3>', unsafe_allow_html=True)

    subtitulo("✅ 1. Confirmação de Presença")
    st.markdown("""
    - Os jogadores devem confirmar presença **até as 22h de quarta-feira**.
    - Quem não confirmar no prazo **não poderá jogar**.
    """)

    subtitulo("⌛ 2. Tempo de Jogo e Rodízio")
    st.markdown("""
    - Cada partida terá duração de **7 minutos ou até 2 gols**, o que ocorrer primeiro.
    - O **time que entra joga pelo empate**:
        - Se empatar, o **time vencedor da partida anterior sai**.
        - Se perder, o **time que entrou sai normalmente**.
    """)

    subtitulo("👕 3. Uniforme Obrigatório")
    st.markdown("""
    - É obrigatório comparecer com o uniforme padrão completo:
        - Camisa do **Borussia Dortmund**
        - Camisa da **Inter de Milão**
        - **Calção preto**
        - **Meião preto**
    - Jogadores sem o uniforme completo **não poderão jogar**.
    """)

    subtitulo("💰 4. Mensalidade e Pagamento")
    st.markdown("""
    - A mensalidade deve ser paga **até o dia 10 de cada mês**.
    - **Jogadores inadimplentes não poderão jogar até quitar sua dívida**.
    - **Goleiros são isentos da mensalidade**, mas devem pagar **o uniforme**.
    """)

    subtitulo("💸 5. Contribuição para o Caixa")
    st.markdown("""
    - Todos os jogadores, incluindo goleiros, devem contribuir com **R$20,00 adicionais**.
    - O valor será utilizado exclusivamente para:
        - **Materiais esportivos** (bolas, bomba de encher bola, etc.)
        - **Itens médicos** (Gelol, faixa, esparadrapo, gelo, etc.)
        - **Água**
        - **Confraternizações** ou outras necessidades da pelada
    """)

    subtitulo("📅 6. Comprometimento")
    st.markdown("""
    - Ao confirmar presença, o jogador assume o compromisso de comparecer.
    - **Faltas não justificadas** podem resultar em **suspensão da próxima rodada**.
    """)

    subtitulo("⚠️ 7. Comportamento")
    st.markdown("""
    - Discussões, brigas ou qualquer tipo de agressividade resultam em **suspensão automática da próxima rodada**.
    - Em caso de reincidência, o jogador poderá ser **banido temporariamente ou definitivamente**, conforme decisão da gestão.
    """)

    subtitulo("🧤 8. Goleiros e Rodízio")
    st.markdown("""
    - Na ausência de goleiro fixo, haverá **rodízio entre os jogadores de linha** para cobrir o gol.
    """)

    subtitulo("🔐 9. Responsabilidade")
    st.markdown("""
    - Comprometimento com **pagamentos, presença e respeito** é essencial para manter a organização.
    - **Quem não estiver em dia com os compromissos não joga.**
    """)

    # Nova regra: Avaliação pós-jogo
    subtitulo("⭐ 10. Avaliação Pós-Jogo: Péreba, Craque e Destaque")
    st.markdown("""
    - Após cada partida, será feita uma votação divertida para eleger:
        - **Péreba**: jogador com a pior performance da rodada.
        - **Craque**: jogador com a melhor performance.
    - A votação é **exclusiva para quem confirmou presença e jogou na pelada**.
    - Somente jogadores presentes poderão votar.
    - A finalidade é **uma brincadeira para animar o grupo e fortalecer o espírito da pelada**.
    - Os resultados serão divulgados para descontração na tela 'Avaliação pós-jogo'.
    """)

# Menu lateral para navegação
with st.sidebar:
    image = Image.open("./imagens/logo.png")  # Substitua "logo.png" pelo nome do seu arquivo
    st.image(image, caption="Chopp's League", use_container_width=True)
    pagina = st.selectbox("Navegue pelo app:", [
        "🏠 Tela Principal",
        "📊 Estatísticas da Partida",
        "👟 Estatísticas dos Jogadores",
        "🎲 Sorteio de Times",
        "✅ Presença e Login",
        "📜 Regras Choppe's League",
    ])

# Controle de navegação
if pagina == "🏠 Tela Principal":
    tela_principal(partidas, jogadores)
elif pagina == "📊 Estatísticas da Partida":
    partidas = tela_partida(partidas)
elif pagina == "👟 Estatísticas dos Jogadores":
    jogadores = tela_jogadores(jogadores)
elif pagina == "🎲 Sorteio de Times":
    tela_sorteio()
elif pagina == "✅ Presença e Login":
    tela_presenca_login()
elif pagina == "📜 Regras Choppe's League":
    tela_regras()