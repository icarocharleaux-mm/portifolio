"""Pagina Projetos: cada projeto em um expander, no formato
problema -> solucao -> tecnologias -> resultado.

TODO (voce): para colocar ou trocar projetos, edite `data/projetos.json`:

  - `titulo`, `resumo`      -> nome e uma linha de descricao
  - `problema`              -> o gargalo, em linguagem de negocio
  - `solucao`               -> o que voce construiu
  - `tecnologias`           -> lista de strings (vira tag na tela)
  - `resultado`             -> lista de bullets com o impacto
  - `destaque`              -> true para o card aparecer na Home
  - `repositorio` / `demo`  -> URLs; deixe "" para esconder o botao

Regra que vale para tudo aqui: nada de nome real de empresa, filial ou
cliente, e nenhum dado pessoal. Numeros de projetos fechados devem ser
apresentados como variacao percentual, nunca como base bruta.
"""

import streamlit as st

from utils import (
    ROTAS,
    aplicar_css,
    bloco_rotulado,
    carregar_perfil,
    carregar_projetos,
    estimativa,
    faixa_cta,
    hero,
    lista,
    lista_de_tags,
    rodape,
    rotulo,
)

st.set_page_config(
    page_title="Projetos | Icaro Charleaux", page_icon="\U0001f6e0️", layout="wide"
)
aplicar_css()

perfil = carregar_perfil()
projetos = carregar_projetos()

# --------------------------------------------------------------------------- #
# Abertura
# --------------------------------------------------------------------------- #
hero(
    kicker="Portfolio",
    titulo="Cada caso segue a mesma",
    titulo_destaque="linha: problema, solução, impacto",
    descricao=(
        "Casos descritos de forma anonimizada: sem nome de empresa, filial, cliente "
        "ou fornecedor, e sem número operacional bruto."
    ),
)

# --------------------------------------------------------------------------- #
# Filtro por categoria
# --------------------------------------------------------------------------- #
categorias = sorted({p.get("categoria", "Outros") for p in projetos})
selecionadas = st.multiselect(
    "Filtrar por categoria",
    options=categorias,
    default=categorias,
    help="Desmarque para esconder categorias.",
)

visiveis = [p for p in projetos if p.get("categoria", "Outros") in selecionadas]

if not visiveis:
    st.info("Nenhum projeto para o filtro selecionado.")

# --------------------------------------------------------------------------- #
# Lista de projetos
# --------------------------------------------------------------------------- #
for indice, projeto in enumerate(visiveis):
    cabecalho = f"{projeto.get('icone', '')} {projeto['titulo']}".strip()

    # O primeiro vem aberto; os demais, fechados.
    with st.expander(cabecalho, expanded=(indice == 0)):
        meta = " · ".join(
            filtro
            for filtro in (projeto.get("categoria"), projeto.get("periodo"))
            if filtro
        )
        if meta:
            st.caption(meta)

        coluna_texto, coluna_lateral = st.columns([2, 1], gap="large")

        with coluna_texto:
            if projeto.get("problema"):
                bloco_rotulado("Problema", projeto["problema"])
            if projeto.get("solucao"):
                bloco_rotulado("Solução", projeto["solucao"])
            if projeto.get("aprendizado"):
                bloco_rotulado("O que eu tirei disso", projeto["aprendizado"])

        with coluna_lateral:
            if projeto.get("tecnologias"):
                rotulo("Tecnologias")
                lista_de_tags(projeto["tecnologias"])

            if projeto.get("resultado"):
                rotulo("Resultado verificável")
                lista(projeto["resultado"])

            # Sai visualmente separado do bloco acima: projetado nao e medido.
            if projeto.get("estimativa"):
                estimativa(projeto["estimativa"])

            # Links opcionais: so aparecem se preenchidos no JSON.
            if projeto.get("repositorio"):
                st.link_button("Código", projeto["repositorio"])
            if projeto.get("demo"):
                st.link_button("Demo", projeto["demo"])

# --------------------------------------------------------------------------- #
# Fechamento
# --------------------------------------------------------------------------- #
faixa_cta(
    "Seu gargalo se parece com algum destes?",
    "Se o processo é repetitivo, tem regra clara e hoje consome gente, provavelmente dá "
    "para automatizar. Me chame que eu avalio.",
    [
        ("Falar comigo", ROTAS["contato"], "primario"),
        ("O que eu entrego", ROTAS["servicos"], "secundario"),
    ],
)

rodape(autor=perfil.get("nome", ""))
