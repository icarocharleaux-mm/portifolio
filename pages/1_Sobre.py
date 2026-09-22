"""Pagina Sobre: bio, diferenciais, skills tecnicas e stack.

TODO (voce): o conteudo vem de `data/perfil.json` (bio, diferenciais) e
`data/skills.json` (categorias e ferramentas).

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
    lista,
    lista_de_tags,
    rodape,
    rotulo,
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
    lista(perfil["diferenciais"])

# --------------------------------------------------------------------------- #
# Skills tecnicas, agrupadas por categoria em duas colunas
# --------------------------------------------------------------------------- #
def _tem_nivel(item: dict) -> bool:
    """True quando o item traz um nivel preenchido (texto ou numero)."""
    valor = item.get("nivel")
    return valor is not None and str(valor).strip() != ""


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
            rotulo(f"{categoria.get('icone', '')} {titulo}".strip())

            # Se nenhum item da categoria tem nivel, sai tudo como um unico
            # grupo de etiquetas, que quebra em varias colunas. Uma etiqueta
            # por linha gastaria meia tela de rolagem com a lista cheia.
            if any(_tem_nivel(item) for item in itens):
                for item in itens:
                    skill(item.get("nome", ""), item.get("nivel"))
            else:
                lista_de_tags([item.get("nome", "") for item in itens])

            st.write("")  # respiro entre categorias

# --------------------------------------------------------------------------- #
# Ferramentas do dia a dia (some se a lista estiver vazia)
# --------------------------------------------------------------------------- #
ferramentas = skills.get("ferramentas", [])

if ferramentas:
    rotulo("Ferramentas do dia a dia")
    lista_de_tags(ferramentas)

# --------------------------------------------------------------------------- #
# Fechamento
# --------------------------------------------------------------------------- #
faixa_cta(
    "Já deu para ver como eu trabalho?",
    "Se a sua operação se parece com os casos daqui, o próximo passo é uma conversa: "
    "você descreve o gargalo, eu digo se dá para automatizar e o que seria preciso.",
    [
        ("Falar comigo", ROTAS["contato"], "primario"),
        ("Ver os casos", ROTAS["projetos"], "secundario"),
    ],
)

rodape(autor=perfil.get("nome", ""))
