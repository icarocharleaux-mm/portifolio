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
    ROTAS,
    aplicar_css,
    avatar,
    cabecalho_secao,
    carregar_perfil,
    carregar_skills,
    faixa_cta,
    hero,
    lista_de_tags,
    rodape,
    skill,
)

st.set_page_config(page_title="Sobre | Icaro Charleaux", page_icon="\U0001f464", layout="wide")
aplicar_css()

perfil = carregar_perfil()
skills = carregar_skills()

# --------------------------------------------------------------------------- #
# Abertura
# --------------------------------------------------------------------------- #
hero(
    kicker="Sobre mim",
    titulo="Entre a operação",
    titulo_destaque="e o código que a sustenta",
    descricao=perfil.get("resumo_curto", ""),
)

# --------------------------------------------------------------------------- #
# Bio
# --------------------------------------------------------------------------- #
coluna_bio, coluna_avatar = st.columns([2.4, 1], gap="large")

with coluna_bio:
    paragrafos = perfil.get("bio") or []

    if paragrafos:
        for paragrafo in paragrafos:
            st.write(paragrafo)
    else:
        st.info(
            'Adicione uma chave `"bio"` (lista de paragrafos) em data/perfil.json '
            "para contar a sua trajetória com mais espaço. O texto acima é o resumo curto.",
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
    cabecalho_secao("Método", "Como eu trabalho")
    for item in perfil["diferenciais"]:
        st.markdown(f"- {item}")

# --------------------------------------------------------------------------- #
# Skills tecnicas, agrupadas por categoria em duas colunas
# --------------------------------------------------------------------------- #
categorias = skills.get("categorias", [])

if categorias:
    cabecalho_secao(
        "Stack",
        "Com o que eu construo",
        "Ferramentas que uso nos projetos desta página. Ajuste em data/skills.json.",
    )

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

# --------------------------------------------------------------------------- #
# Ferramentas e idiomas (cada bloco so aparece se houver conteudo)
# --------------------------------------------------------------------------- #
ferramentas = skills.get("ferramentas", [])
idiomas = skills.get("idiomas", [])

if ferramentas or idiomas:
    coluna_ferramentas, coluna_idiomas = st.columns([2, 1], gap="large")

    with coluna_ferramentas:
        if ferramentas:
            cabecalho_secao("", "Ferramentas do dia a dia")
            lista_de_tags(ferramentas)

    with coluna_idiomas:
        if idiomas:
            cabecalho_secao("", "Idiomas")
            for idioma in idiomas:
                st.markdown(f"**{idioma['nome']}** — {idioma.get('nivel', '')}")

# --------------------------------------------------------------------------- #
# Fechamento
# --------------------------------------------------------------------------- #
faixa_cta(
    "Quer ver isso aplicado?",
    "Os projetos mostram o caminho completo: qual era o gargalo, o que foi construído "
    "e o que mudou na operação depois.",
    [
        ("Ver projetos", ROTAS["projetos"], "primario"),
        ("Falar comigo", ROTAS["contato"], "secundario"),
    ],
)

rodape(autor=perfil.get("nome", ""))
