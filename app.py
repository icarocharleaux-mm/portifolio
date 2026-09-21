"""Home do portfolio.

Ponto de entrada do app. Rode com:

    streamlit run app.py

As demais paginas ficam em `pages/` e o Streamlit as descobre sozinho,
na ordem do prefixo numerico do nome do arquivo.

TODO (voce): o conteudo desta pagina vem de `data/perfil.json` (hero, secao
"o que eu resolvo", links) e `data/projetos.json` (cards de destaque).
Edite esses arquivos -- nao e preciso mexer aqui.
"""

import streamlit as st

from utils import (
    ROTAS,
    aplicar_css,
    cabecalho_secao,
    card_projeto,
    card_solucao,
    carregar_perfil,
    faixa_cta,
    hero,
    projetos_em_destaque,
    rodape,
)

# --------------------------------------------------------------------------- #
# Configuracao da pagina -- precisa ser o primeiro comando Streamlit do script
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

aplicar_css()

perfil = carregar_perfil()
links = perfil.get("links", {})
destaques = projetos_em_destaque()

# --------------------------------------------------------------------------- #
# Hero
# --------------------------------------------------------------------------- #
acoes_hero = [("Ver projetos", ROTAS["projetos"], "primario")]

# O segundo botao leva ao canal mais direto que estiver configurado.
if links.get("whatsapp"):
    acoes_hero.append(("Falar no WhatsApp", links["whatsapp"], "secundario"))
else:
    acoes_hero.append(("Falar comigo", ROTAS["contato"], "secundario"))

hero(
    kicker=perfil.get("cargo", ""),
    titulo=perfil.get("nome", ""),
    titulo_destaque="Automação que tira a operação do manual",
    descricao=perfil.get("resumo_curto", ""),
    localizacao=perfil.get("localizacao", ""),
    acoes=acoes_hero,
)

# --------------------------------------------------------------------------- #
# O que eu resolvo -- traduz competencia tecnica em dor de operacao
# --------------------------------------------------------------------------- #
solucoes = perfil.get("solucoes", [])

if solucoes:
    cabecalho_secao(
        "O que eu resolvo",
        "Três gargalos que aparecem em toda operação",
        "Se algum deles parece a sua rotina, dá para automatizar.",
    )

    colunas = st.columns(len(solucoes[:3]), gap="medium")
    for posicao, (coluna, item) in enumerate(zip(colunas, solucoes[:3]), start=1):
        with coluna:
            card_solucao(
                icone=item.get("icone", ""),
                titulo=item.get("titulo", ""),
                texto=item.get("texto", ""),
                atraso=posicao,
            )

# --------------------------------------------------------------------------- #
# Projetos em destaque
# --------------------------------------------------------------------------- #
cabecalho_secao(
    "Portfólio",
    "Projetos em destaque",
    "Casos anonimizados. Problema, solução e impacto na página Projetos.",
)

if destaques:
    # Ate 3 cards por linha.
    for inicio in range(0, len(destaques), 3):
        linha = destaques[inicio : inicio + 3]
        colunas = st.columns(3, gap="medium")
        for posicao, (coluna, projeto) in enumerate(zip(colunas, linha), start=1):
            with coluna:
                card_projeto(projeto, atraso=posicao)
else:
    st.info(
        'Nenhum projeto marcado como destaque. Coloque `"destaque": true` '
        "em algum item de data/projetos.json."
    )

st.write("")
st.page_link("pages/2_Projetos.py", label="Ver todos os projetos", icon="\U0001f4c1")

# --------------------------------------------------------------------------- #
# Fechamento
# --------------------------------------------------------------------------- #
faixa_cta(
    "Tem um processo travando a sua operação?",
    "Me conte o gargalo em duas linhas. Se der para automatizar, eu digo como — "
    "e se não der, digo isso também.",
    [
        ("Falar comigo", ROTAS["contato"], "primario"),
        ("Conhecer minha stack", ROTAS["sobre"], "secundario"),
    ],
)

rodape(
    "Portfólio construído com Streamlit · "
    "casos descritos de forma anonimizada, sem dado operacional real."
)
