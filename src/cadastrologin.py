import streamlit as st
import re

# Função de formatação de telefone
def formatar_telefone_9fixo(numero):
    if len(numero) == 11:
        return f"({numero[:2]}) {numero[2:7]}-{numero[7:]}"
    return numero

# Tela principal (só acessível após login)
def tela_main():
    st.title("🏆 Tela Principal")
    st.success(f"Bem-vindo(a), {st.session_state['nome']}!")

    st.write("Essa é a tela protegida do sistema. Você só vê isso após login.")

    if st.button("Sair"):
        for chave in list(st.session_state.keys()):
            del st.session_state[chave]
        st.experimental_rerun()

# Tela de login/cadastro
def tela_login():
    st.title("Acesso ao Sistema")

    # Inicialização de estados
    for k, v in {
        "telefone_raw": "",
        "nome": "",
        "email": "",
        "senha": "",
        "posicao": "",
        "nascimento": None,
        "usuario_logado": False,
        "usuario_cadastrado": False
    }.items():
        if k not in st.session_state:
            st.session_state[k] = v

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
                elif not nome or not email or not senha or not posicao or not nascimento:
                    st.warning("Preencha todos os campos.")
                else:
                    # Salva cadastro na sessão
                    st.session_state["nome"] = nome
                    st.session_state["email"] = email
                    st.session_state["senha"] = senha
                    st.session_state["posicao"] = posicao
                    st.session_state["nascimento"] = nascimento
                    st.session_state["telefone_raw"] = telefone_formatado
                    st.session_state["usuario_cadastrado"] = True
                    st.success("Cadastro realizado com sucesso! Agora faça login.")

    elif aba == "🔐 Login":
        with st.form("form_login", clear_on_submit=True):
            email_login = st.text_input("E-mail")
            senha_login = st.text_input("Senha", type="password")
            submit_login = st.form_submit_button("Entrar")

            if submit_login:
                if (
                    st.session_state.get("usuario_cadastrado")
                    and email_login == st.session_state["email"]
                    and senha_login == st.session_state["senha"]
                ):
                    st.session_state["usuario_logado"] = True
                    st.success("Login realizado com sucesso!")
                    st.experimental_rerun()
                else:
                    st.warning("Credenciais inválidas ou usuário não cadastrado.")

# 🔁 Fluxo principal
if not st.session_state.get("usuario_logado", False):
    tela_login()
else:
    tela_main()
