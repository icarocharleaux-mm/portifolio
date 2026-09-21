"""Home do portfolio.

Ponto de entrada do app. Rode com:

    streamlit run app.py

As demais paginas ficam em `pages/` e o Streamlit as descobre sozinho,
na ordem do prefixo numerico do nome do arquivo.

TODO (voce): o conteudo desta pagina vem de `data/perfil.json` e
`data/projetos.json`. Edite esses arquivos -- nao e preciso mexer aqui.
"""

import streamlit as st

from utils import (
    aplicar_css,
    avatar,
    cabecalho_secao,
    card_projeto,
    carregar_perfil,
    projetos_em_destaque,
    rodape,
)

# --------------------------------------------------------------------------- #
# Configuracao da pagina -- precisa ser o primeiro comando Streamlit do script
# --------------------------------------------------------------------------- #
st.set_page_config(
    page_title="Portfolio | Automacao e TI para Logistica",
    page_icon="\U0001f4e6",  # emoji de caixa
    layout="wide",
    initial_sidebar_state="expanded",
)

aplicar_css()

perfil = carregar_perfil()
destaques = projetos_em_destaque()

# --------------------------------------------------------------------------- #
# Apresentacao: avatar a esquerda, resumo a direita
# --------------------------------------------------------------------------- #
coluna_avatar, coluna_texto = st.columns([1, 2.4], gap="large")

with coluna_avatar:
    avatar(perfil.get("avatar", "assets/avatar_placeholder.svg"), largura=200)

with coluna_texto:
    st.title(perfil["nome"])
    st.subheader(perfil["cargo"])
    st.write(perfil["resumo_curto"])

    if perfil.get("localizacao"):
        st.caption(f"\U0001f4cd {perfil['localizacao']}")

    # Links externos. Campos vazios em data/perfil.json sao simplesmente ignorados.
    links = perfil.get("links", {})
    rotulos = {
        "linkedin": "LinkedIn",
        "whatsapp": "WhatsApp",
        "github": "GitHub",
        "site": "Site",
    }
    partes = [
        f"[{rotulo}]({links[chave]})"
        for chave, rotulo in rotulos.items()
        if links.get(chave)
    ]
    if links.get("email"):
        partes.append(f"[E-mail](mailto:{links['email']})")
    if partes:
        st.markdown(" &nbsp;·&nbsp; ".join(partes))

st.divider()

# --------------------------------------------------------------------------- #
# Projetos em destaque
# --------------------------------------------------------------------------- #
cabecalho_secao(
    "Projetos em destaque",
    "Casos anonimizados. Problema, solucao e impacto na pagina Projetos.",
)

if destaques:
    # Ate 3 cards por linha.
    for inicio in range(0, len(destaques), 3):
        linha = destaques[inicio : inicio + 3]
        colunas = st.columns(3, gap="medium")
        for coluna, projeto in zip(colunas, linha):
            with coluna:
                card_projeto(projeto)
else:
    st.info(
        'Nenhum projeto marcado como destaque. Coloque `"destaque": true` '
        "em algum item de data/projetos.json."
    )

st.page_link("pages/2_Projetos.py", label="Ver todos os projetos", icon="\U0001f4c1")

st.divider()

# --------------------------------------------------------------------------- #
# Navegacao rapida
# --------------------------------------------------------------------------- #
cabecalho_secao("Navegue pelo portfolio")

coluna_sobre, coluna_projetos, coluna_contato = st.columns(3, gap="medium")

with coluna_sobre:
    st.page_link("pages/1_Sobre.py", label="**Sobre**", icon="\U0001f464")
    st.caption("Bio, trajetoria e stack tecnica.")

with coluna_projetos:
    st.page_link("pages/2_Projetos.py", label="**Projetos**", icon="\U0001f6e0️")
    st.caption("Problema, solucao, tecnologias e impacto de cada entrega.")

with coluna_contato:
    st.page_link("pages/3_Contato.py", label="**Contato**", icon="✉️")
    st.caption("Onde me encontrar e como falar comigo.")

rodape(
    "Portfolio construido com Streamlit · "
    "casos descritos de forma anonimizada, sem dado operacional real."
)
