import streamlit as st
import requests
from io import BytesIO
from PIL import Image
import pandas as pd
import random
import os
import re

# Tela de cadastro e login
def tela_presenca_login():
    st.title("Cadastro, Login e Confirmação de Presença")

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
            with st.form("form_cadastro"):  # <- removido clear_on_submit
                nome = st.text_input("Nome completo", value=st.session_state["nome"])
                email = st.text_input("E-mail", value=st.session_state["email"])
                senha = st.text_input("Senha", type="password", value=st.session_state["senha"])
                posicao = st.selectbox("Posição que joga", ["", "Linha", "Goleiro"], index=["", "Linha", "Goleiro"].index(st.session_state["posicao"]) if st.session_state["posicao"] else 0)
                nascimento = st.date_input("Data de nascimento", value=st.session_state["nascimento"])
                telefone_input = st.text_input("Número de telefone (com DDD)", value=st.session_state["telefone_raw"], key="telefone_input")

                submit = st.form_submit_button("Cadastrar")

                if submit:
                    # Salva os valores preenchidos
                    st.session_state["nome"] = nome
                    st.session_state["email"] = email
                    st.session_state["senha"] = senha
                    st.session_state["posicao"] = posicao
                    st.session_state["nascimento"] = nascimento
                    st.session_state["telefone_raw"] = telefone_input

                    numeros = re.sub(r'\D', '', telefone_input)

                    if len(numeros) >= 3 and numeros[2] != '9':
                        numeros = numeros[:2] + '9' + numeros[2:]

                    telefone_formatado = formatar_telefone_9fixo(numeros)

                    if len(numeros) != 11:
                        st.warning("Número de telefone inválido. Deve conter DDD + 9 + número completo (11 dígitos).")
                    elif not nome or not email or not senha or not posicao or not nascimento or not numeros:
                        st.warning("Preencha todos os campos.")
                    else:
                        # Resetar estado se quiser limpar após sucesso
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