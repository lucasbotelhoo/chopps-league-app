import streamlit as st
import re
import os

# Função para formatar telefone
def formatar_telefone_9fixo(numero):
    if len(numero) == 11:
        return f"({numero[:2]}) {numero[2:7]}-{numero[7:]}"
    return numero

# Tela de login e cadastro
def tela_login_e_cadastro():
    st.set_page_config(page_title="Login", page_icon="🔐", layout="centered")
    st.title("Acesso ao Sistema")

    # Session state inicial
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
    if "usuario_logado" not in st.session_state:
        st.session_state["usuario_logado"] = False

    aba = st.radio("Selecione uma opção:", ["🔐 Login", "📝 Cadastro"])

    if aba == "📝 Cadastro":
        with st.form("form_cadastro"):
            nome = st.text_input("Nome completo", value=st.session_state["nome"])
            email = st.text_input("E-mail", value=st.session_state["email"])
            senha = st.text_input("Senha", type="password", value=st.session_state["senha"])
            posicao = st.selectbox("Posição que joga", ["", "Linha", "Goleiro"],
                                   index=["", "Linha", "Goleiro"].index(st.session_state["posicao"]) if st.session_state["posicao"] else 0)
            nascimento = st.date_input("Data de nascimento", value=st.session_state["nascimento"])
            telefone_input = st.text_input("Número de telefone (com DDD)", value=st.session_state["telefone_raw"])

            submit = st.form_submit_button("Cadastrar")

            if submit:
                numeros = re.sub(r'\D', '', telefone_input)[:11]
                if len(numeros) >= 3 and numeros[2] != '9':
                    numeros = numeros[:2] + '9' + numeros[2:]

                telefone_formatado = formatar_telefone_9fixo(numeros)

                st.session_state["nome"] = nome
                st.session_state["email"] = email
                st.session_state["senha"] = senha
                st.session_state["posicao"] = posicao
                st.session_state["nascimento"] = nascimento
                st.session_state["telefone_raw"] = telefone_formatado

                if len(numeros) != 11:
                    st.warning("Número de telefone inválido. Deve conter exatamente 11 dígitos.")
                elif not nome or not email or not senha or not posicao or not nascimento:
                    st.warning("Preencha todos os campos.")
                else:
                    st.success("Cadastro realizado com sucesso! Agora faça login.")

    elif aba == "🔐 Login":
        with st.form("form_login", clear_on_submit=True):
            email_login = st.text_input("E-mail")
            senha_login = st.text_input("Senha", type="password")
            submit_login = st.form_submit_button("Entrar")

            if submit_login:
                if email_login == st.session_state["email"] and senha_login == st.session_state["senha"]:
                    st.session_state["usuario_logado"] = True
                    st.success("Login realizado com sucesso!")
                    st.experimental_rerun()
                else:
                    st.warning("E-mail ou senha incorretos.")

# Executa
tela_login_e_cadastro()

# Redireciona para main.py se estiver logado
if st.session_state.get("usuario_logado"):
    st.switch_page("main.py")  # Só funciona com múltiplas páginas do Streamlit
