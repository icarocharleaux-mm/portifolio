"""Ponto de entrada do portfolio.

    streamlit run app.py

Este arquivo nao desenha nada: ele so registra as paginas e entrega a
navegacao para o Streamlit. O conteudo de cada pagina fica em `pages/`.

POR QUE `st.navigation` E NAO A DESCOBERTA AUTOMATICA DE `pages/`
No modo automatico, o rotulo de cada pagina no menu vem do nome do arquivo
-- e a pagina inicial aparecia como "app", porque o arquivo se chama
app.py (nome exigido pela configuracao do Streamlit Cloud). Com
`st.navigation`, o rotulo, o icone e a URL de cada pagina sao explicitos.

Para adicionar uma pagina: crie o arquivo em `pages/` e acrescente um
`st.Page` na lista abaixo, na posicao em que ele deve aparecer no menu.
"""

import streamlit as st

# --------------------------------------------------------------------------- #
# Configuracao global -- precisa vir antes de qualquer outro comando Streamlit
# --------------------------------------------------------------------------- #
st.set_page_config(
    page_title="Icaro Charleaux | Automação e Inovação em Logística",
    page_icon="⚡",
    layout="wide",
    # "auto" abre a barra lateral no desktop e a mantem fechada no celular.
    # Com "expanded", quem chega pelo celular cai numa tela coberta pelo menu,
    # com o hero escondido atras dele.
    initial_sidebar_state="auto",
)

# --------------------------------------------------------------------------- #
# Paginas
#
# `url_path` fica explicito para as URLs continuarem as mesmas de antes
# (/Sobre, /Projetos, /Contato) -- links ja compartilhados seguem valendo.
# A pagina marcada como `default` responde na raiz e nao aceita url_path.
# --------------------------------------------------------------------------- #
PAGINAS = [
    st.Page("pages/0_Home.py", title="Home", icon="⚡", default=True),
    st.Page("pages/1_Sobre.py", title="Sobre", icon="👤", url_path="Sobre"),
    st.Page("pages/2_Projetos.py", title="Projetos", icon="🛠️", url_path="Projetos"),
    st.Page("pages/3_Contato.py", title="Contato", icon="✉️", url_path="Contato"),
]

st.navigation(PAGINAS).run()
