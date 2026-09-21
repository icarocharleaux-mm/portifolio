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
    # A navegacao e por abas no topo (ver st.navigation abaixo), entao nao ha
    # barra lateral. "auto" fica como padrao seguro caso alguma pagina passe
    # a usar a sidebar para outra coisa.
    initial_sidebar_state="auto",
)

# --------------------------------------------------------------------------- #
# Paginas
#
# A ORDEM DA LISTA e a ordem do menu, independente do nome do arquivo --
# por isso Servicos (arquivo 4_) aparece em segundo: quem chega para
# contratar ve a oferta antes do curriculo.
#
# `url_path` fica explicito para as URLs continuarem as mesmas de antes
# (/Sobre, /Projetos, /Contato) -- links ja compartilhados seguem valendo.
# "Servicos" vai sem cedilha de proposito: acento em URL vira escape feio
# quando alguem cola o link em uma mensagem.
# A pagina marcada como `default` responde na raiz e nao aceita url_path.
# --------------------------------------------------------------------------- #
PAGINAS = [
    st.Page("pages/0_Home.py", title="Home", icon="⚡", default=True),
    st.Page("pages/4_Servicos.py", title="Serviços", icon="⚙️", url_path="Servicos"),
    st.Page("pages/2_Projetos.py", title="Projetos", icon="🛠️", url_path="Projetos"),
    st.Page("pages/1_Sobre.py", title="Sobre", icon="👤", url_path="Sobre"),
    st.Page("pages/3_Contato.py", title="Contato", icon="✉️", url_path="Contato"),
]

# `position="top"` troca a barra lateral por abas no topo da area principal.
# Some com a sidebar por completo -- o que tambem resolve, de lambuja, o
# menu cobrindo o conteudo no celular.
st.navigation(PAGINAS, position="top").run()
