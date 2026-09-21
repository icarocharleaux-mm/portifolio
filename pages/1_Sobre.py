"""Pagina Sobre: bio, diferenciais, skills tecnicas e stack.

TODO (voce): o conteudo vem de `data/perfil.json` (bio, diferenciais) e
`data/skills.json` (categorias, ferramentas, idiomas).

Sobre o schema de skills.json: a pagina aceita duas formas de escrever uma
categoria, para voce nao ficar preso a um formato so --

    {"nome": "Automacao", "ferramentas": [{"nome": "Power Apps", "nivel": ""}]}
    {"titulo": "Automacao", "itens":      [{"nome": "Power Apps", "nivel": 85}]}

E `nivel` pode ser numero (vira barra de 0 a 100), texto ("Avancado", vira
rotulo) ou vazio (so o nome aparece).
"""

import streamlit as st

from utils import (
    aplicar_css,
    avatar,
    cabecalho_secao,
    carregar_perfil,
    carregar_skills,
    lista_de_tags,
    rodape,
    skill,
)

st.set_page_config(page_title="Sobre | Portfolio", page_icon="\U0001f464", layout="wide")
aplicar_css()

perfil = carregar_perfil()
skills = carregar_skills()

# --------------------------------------------------------------------------- #
# Bio
# --------------------------------------------------------------------------- #
st.title("Sobre mim")

coluna_bio, coluna_avatar = st.columns([2.4, 1], gap="large")

with coluna_bio:
    paragrafos = perfil.get("bio") or []

    if paragrafos:
        for paragrafo in paragrafos:
            st.write(paragrafo)
    else:
        # Sem bio escrita, cai no resumo curto da Home para a pagina nao ficar vazia.
        st.write(perfil.get("resumo_curto", ""))
        st.info(
            'Adicione uma chave `"bio"` (lista de paragrafos) em data/perfil.json '
            "para contar a sua trajetoria com mais espaco.",
            icon="✍️",
        )

with coluna_avatar:
    avatar(perfil.get("avatar", "assets/avatar_placeholder.svg"), largura=170)
    if perfil.get("localizacao"):
        st.caption(f"\U0001f4cd {perfil['localizacao']}")

# --------------------------------------------------------------------------- #
# Diferenciais (opcional -- some se a chave nao existir)
# --------------------------------------------------------------------------- #
if perfil.get("diferenciais"):
    cabecalho_secao("Como eu trabalho")
    for item in perfil["diferenciais"]:
        st.markdown(f"- {item}")

st.divider()

# --------------------------------------------------------------------------- #
# Skills tecnicas, agrupadas por categoria em duas colunas
# --------------------------------------------------------------------------- #
categorias = skills.get("categorias", [])

if categorias:
    cabecalho_secao("Skills tecnicas", "Ajuste as categorias em data/skills.json.")

    coluna_esquerda, coluna_direita = st.columns(2, gap="large")

    for indice, categoria in enumerate(categorias):
        destino = coluna_esquerda if indice % 2 == 0 else coluna_direita

        # Aceita os dois nomes de chave, para o JSON poder ser escrito de
        # qualquer uma das duas formas documentadas no topo do arquivo.
        titulo = categoria.get("titulo") or categoria.get("nome", "Sem categoria")
        itens = categoria.get("itens") or categoria.get("ferramentas") or []

        with destino:
            # O strip fica dentro do negrito: "** titulo**" nao renderiza em Markdown.
            rotulo = f"{categoria.get('icone', '')} {titulo}".strip()
            st.markdown(f"**{rotulo}**")
            for item in itens:
                skill(item.get("nome", ""), item.get("nivel"))
            st.write("")  # respiro entre categorias

    st.divider()

# --------------------------------------------------------------------------- #
# Ferramentas e idiomas (cada bloco so aparece se houver conteudo)
# --------------------------------------------------------------------------- #
ferramentas = skills.get("ferramentas", [])
idiomas = skills.get("idiomas", [])

if ferramentas or idiomas:
    coluna_ferramentas, coluna_idiomas = st.columns([2, 1], gap="large")

    with coluna_ferramentas:
        if ferramentas:
            cabecalho_secao("Ferramentas do dia a dia")
            lista_de_tags(ferramentas)

    with coluna_idiomas:
        if idiomas:
            cabecalho_secao("Idiomas")
            for idioma in idiomas:
                st.markdown(f"**{idioma['nome']}** — {idioma.get('nivel', '')}")

    st.divider()

coluna_a, coluna_b = st.columns(2)
with coluna_a:
    st.page_link("pages/2_Projetos.py", label="Ver projetos", icon="\U0001f6e0️")
with coluna_b:
    st.page_link("pages/3_Contato.py", label="Falar comigo", icon="✉️")

rodape()
