import streamlit as st
import re

def formatar_telefone_9fixo(numero):
    if len(numero) == 11:
        return f"({numero[:2]}) {numero[2:7]}-{numero[7:]}"
    return numero

def tela_login():
    st.set_page_config(page_title="Login", page_icon="🔐")
    st.title("Acesso ao Sistema")

    if "usuario_logado" not in st.session_state:
        st.session_state["usuario_logado"] = False
    if "usuario_cadastrado" not in st.session_state:
        st.session_state["usuario_cadastrado"] = False

    aba = st.radio("Selecione uma opção:", ["🔐 Login", "📝 Cadastro"])

    if aba == "📝 Cadastro":
        with st.form("form_cadastro"):
            nome = st.text_input("Nome completo")
            email = st.text_input("E-mail")
            senha = st.text_input("Senha", type="password")
            posicao = st.selectbox("Posição que joga", ["", "Linha", "Goleiro"])
            nascimento = st.date_input("Data de nascimento")
            telefone_input = st.text_input("Número de telefone (com DDD)")

            submit = st.form_submit_button("Cadastrar")

            if submit:
                numeros = re.sub(r'\D', '', telefone_input)[:11]
                if len(numeros) >= 3 and numeros[2] != '9':
                    numeros = numeros[:2] + '9' + numeros[2:]
                telefone_formatado = formatar_telefone_9fixo(numeros)

                if len(numeros) != 11:
                    st.warning("Número de telefone inválido. Deve conter exatamente 11 dígitos.")
                elif not nome or not email or not senha or not posicao:
                    st.warning("Preencha todos os campos.")
                else:
                    st.session_state["cadastro"] = {
                        "nome": nome,
                        "email": email,
                        "senha": senha
                    }
                    st.session_state["usuario_cadastrado"] = True
                    st.success("Cadastro realizado com sucesso! Agora faça login.")

    elif aba == "🔐 Login":
        with st.form("form_login", clear_on_submit=True):
            email_login = st.text_input("E-mail")
            senha_login = st.text_input("Senha", type="password")
            submit_login = st.form_submit_button("Entrar")

            if submit_login:
                cadastro = st.session_state.get("cadastro", {})
                if (
                    st.session_state["usuario_cadastrado"]
                    and email_login == cadastro.get("email")
                    and senha_login == cadastro.get("senha")
                ):
                    st.session_state["usuario_logado"] = True
                    st.session_state["nome"] = cadastro.get("nome")
                    st.success("Login realizado com sucesso!")
                    st.switch_page("main")
                else:
                    st.warning("E-mail ou senha incorretos.")

tela_login()
tela_login()
#teste