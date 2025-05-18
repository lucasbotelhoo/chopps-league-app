import streamlit as st
import re

# Função de formatação
def formatar_telefone_9fixo(numero):
    if len(numero) == 11:
        return f"({numero[:2]}) {numero[2:7]}-{numero[7:]}"
    return numero

# Página protegida
def tela_principal():
    st.title("🎯 Bem-vindo ao Sistema")
    st.success(f"Você está logado como: {st.session_state.get('nome')}")

    st.markdown("Aqui vai o conteúdo da sua tela principal.")

    if st.button("Sair"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()

# Tela de login/cadastro
def tela_login():
    st.title("Acesso ao Sistema")

    # Inicializa estados
    for key, default in {
        "telefone_raw": "",
        "nome": "",
        "email": "",
        "senha": "",
        "posicao": "",
        "nascimento": None,
        "usuario_logado": False
    }.items():
        if key not in st.session_state:
            st.session_state[key] = default

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
                    st.session_state.update({
                        "nome": nome,
                        "email": email,
                        "senha": senha,
                        "posicao": posicao,
                        "nascimento": nascimento,
                        "telefone_raw": telefone_formatado
                    })
                    st.success("Cadastro realizado! Agora faça login.")

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

# Controle de navegação
if st.session_state.get("usuario_logado"):
    tela_principal()
else:
    tela_login()
