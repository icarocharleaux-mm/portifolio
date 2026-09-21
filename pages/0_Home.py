"""Home do portfolio.

Esta pagina e registrada por `app.py`, que e o ponto de entrada do app
(`streamlit run app.py`) e monta a navegacao com `st.navigation`.

TODO (voce): o conteudo desta pagina vem de `data/perfil.json` (hero, secao
"o que eu resolvo", links) e `data/projetos.json` (cards de destaque).
Edite esses arquivos -- nao e preciso mexer aqui.
"""

import streamlit as st

from utils import (
    ROTAS,
    aplicar_css,
    botoes,
    cabecalho_secao,
    card_projeto,
    card_solucao,
    carregar_perfil,
    faixa_cta,
    hero,
    projetos_em_destaque,
    rodape,
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
    # O nome e o <h1> e o destaque absoluto da pagina; a frase de impacto vai
    # como `subtitulo`, que sai em um <h2> bem menor e mais leve.
    titulo=perfil.get("nome", ""),
    subtitulo="Automação que tira a operação do manual",
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

botoes([("Ver todos os projetos", ROTAS["projetos"], "secundario")])

# --------------------------------------------------------------------------- #
# Fechamento
# --------------------------------------------------------------------------- #
faixa_cta(
    "Tem um processo travando a sua operação?",
    "Me conte o gargalo em duas linhas. Se der para automatizar, eu digo como — "
    "e se não der, digo isso também.",
    [
        ("Ver o que eu entrego", ROTAS["servicos"], "primario"),
        ("Falar comigo", ROTAS["contato"], "secundario"),
    ],
)

rodape(
    autor=perfil.get("nome", ""),
    nota="Casos descritos de forma anonimizada, sem dado operacional real.",
)
