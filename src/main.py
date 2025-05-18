import streamlit as st
import requests
from io import BytesIO
from PIL import Image
import pandas as pd
import random
import os
import re

def tela_login_e_cadastro():
    st.title("Acesso ao Sistema")

    # Inicializa os campos no session_state
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

    # Abas de navegação entre login e cadastro
    aba = st.radio("Selecione uma opção:", ["🔐 Login", "📝 Cadastro"])

    # Tela de Cadastro
    if aba == "📝 Cadastro":
        with st.form("form_cadastro"):
            nome = st.text_input("Nome completo", value=st.session_state["nome"])
            email = st.text_input("E-mail", value=st.session_state["email"])
            senha = st.text_input("Senha", type="password", value=st.session_state["senha"])
            posicao = st.selectbox(
                "Posição que joga",
                ["", "Linha", "Goleiro"],
                index=["", "Linha", "Goleiro"].index(st.session_state["posicao"]) if st.session_state["posicao"] else 0
            )
            nascimento = st.date_input("Data de nascimento", value=st.session_state["nascimento"])
            telefone_input = st.text_input("Número de telefone (com DDD)", value=st.session_state["telefone_raw"], key="telefone_input")

            submit = st.form_submit_button("Cadastrar")

            if submit:
                # Salva os dados no session_state
                st.session_state["nome"] = nome
                st.session_state["email"] = email
                st.session_state["senha"] = senha
                st.session_state["posicao"] = posicao
                st.session_state["nascimento"] = nascimento
                st.session_state["telefone_raw"] = telefone_input

                # Limpa e valida o telefone
                numeros = re.sub(r'\D', '', telefone_input)[:11]

                if len(numeros) >= 3 and numeros[2] != '9':
                    numeros = numeros[:2] + '9' + numeros[2:]

                telefone_formatado = formatar_telefone_9fixo(numeros)

                if len(numeros) != 11:
                    st.warning("Número de telefone inválido. Deve conter exatamente 11 dígitos.")
                elif not nome or not email or not senha or not posicao or not nascimento:
                    st.warning("Preencha todos os campos.")
                else:
                    st.success("Cadastro realizado com sucesso! Agora faça login.")

    # Tela de Login
    elif aba == "🔐 Login":
        with st.form("form_login", clear_on_submit=True):
            email_login = st.text_input("E-mail", key="email_login")
            senha_login = st.text_input("Senha", type="password", key="senha_login")
            submit_login = st.form_submit_button("Entrar")

            if submit_login:
                if email_login == st.session_state["email"] and senha_login == st.session_state["senha"]:
                    st.session_state["usuario_logado"] = True
                    st.success(f"Usuário {email_login} logado com sucesso!")
                else:
                    st.warning("Credenciais incorretas. Tente novamente.")