"""Pagina Servicos: o que eu vendo, em pacotes, e como eu trabalho.

Enquanto a pagina Projetos mostra o que ja foi feito, esta mostra o que da
para contratar. Cada pacote aponta para um caso real que o comprova -- e
essa amarracao e o ponto: pacote sem prova vira promessa.

TODO (voce): todo o conteudo vem de `data/servicos.json` -- pacotes,
entregaveis, etapas do processo e o texto de fechamento. Ao criar um pacote
novo, preencha o campo `prova` com o projeto que o sustenta.
"""

import streamlit as st

from utils import (
    ROTAS,
    aplicar_css,
    cabecalho_secao,
    card_servico,
    carregar_json,
    carregar_perfil,
    faixa_cta,
    hero,
    passo,
    rodape,
)

st.set_page_config(
    page_title="Serviços | Icaro Charleaux", page_icon="⚙️", layout="wide"
)
aplicar_css()

perfil = carregar_perfil()
servicos = carregar_json("servicos.json")
links = perfil.get("links", {})

# --------------------------------------------------------------------------- #
# Abertura
# --------------------------------------------------------------------------- #
acoes_hero = [("Ver os casos", ROTAS["projetos"], "primario")]

if links.get("whatsapp"):
    acoes_hero.append(("Falar no WhatsApp", links["whatsapp"], "secundario"))
else:
    acoes_hero.append(("Falar comigo", ROTAS["contato"], "secundario"))

hero(
    kicker="Serviços",
    titulo=servicos.get("chamada", ""),
    # Servicos era a unica pagina com o h1 chapado, sem o gradiente que as
    # outras quatro usam -- justamente a pagina que existe para vender.
    titulo_destaque=servicos.get("chamada_destaque", ""),
    descricao=servicos.get("subchamada", ""),
    acoes=acoes_hero,
)

# --------------------------------------------------------------------------- #
# Pacotes -- tres por linha
# --------------------------------------------------------------------------- #
pacotes = servicos.get("pacotes", [])

if pacotes:
    cabecalho_secao(
        "O que eu entrego",
        "Seis frentes, sempre amarradas a um caso real",
        "Cada pacote traz o projeto que comprova a entrega — não é catálogo de intenção.",
    )

    for inicio in range(0, len(pacotes), 3):
        linha = pacotes[inicio : inicio + 3]
        colunas = st.columns(3, gap="medium")
        for posicao, (coluna, item) in enumerate(zip(colunas, linha), start=1):
            with coluna:
                card_servico(
                    icone=item.get("icone", ""),
                    titulo=item.get("titulo", ""),
                    texto=item.get("texto", ""),
                    entregaveis=item.get("entregaveis", []),
                    prova=item.get("prova", ""),
                    atraso=posicao,
                )

# --------------------------------------------------------------------------- #
# Como eu trabalho -- etapas numeradas, duas por linha
# --------------------------------------------------------------------------- #
etapas = servicos.get("processo", [])

if etapas:
    cabecalho_secao(
        "Como eu trabalho",
        "Do diagnóstico à sua independência",
        "O critério de sucesso é o processo seguir de pé sem mim.",
    )

    for inicio in range(0, len(etapas), 2):
        linha = etapas[inicio : inicio + 2]
        colunas = st.columns(2, gap="large")
        for coluna, etapa in zip(colunas, linha):
            with coluna:
                passo(
                    numero=etapa.get("numero", ""),
                    titulo=etapa.get("titulo", ""),
                    texto=etapa.get("texto", ""),
                )

# --------------------------------------------------------------------------- #
# Fechamento
# --------------------------------------------------------------------------- #
faixa_cta(
    servicos.get("cta_titulo", "Vamos conversar?"),
    servicos.get("cta_texto", ""),
    [
        ("Falar comigo", ROTAS["contato"], "primario"),
        ("Ver os casos", ROTAS["projetos"], "secundario"),
    ],
)

rodape(autor=perfil.get("nome", ""))
