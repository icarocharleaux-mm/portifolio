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

import altair as alt
import streamlit as st

from utils import (
    CORES_GRAFICO,
    ROTAS,
    aplicar_css,
    bloco_rotulado,
    cabecalho_secao,
    carregar_csv,
    carregar_perfil,
    carregar_projetos,
    estimativa,
    faixa_cta,
    hero,
    lista_de_tags,
    rodape,
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
                st.markdown("**Tecnologias**")
                lista_de_tags(projeto["tecnologias"])

            if projeto.get("resultado"):
                st.markdown("**Resultado verificável**")
                for linha in projeto["resultado"]:
                    st.markdown(f"- {linha}")

            # Sai visualmente separado do bloco acima: projetado nao e medido.
            if projeto.get("estimativa"):
                estimativa(projeto["estimativa"])

            # Links opcionais: so aparecem se preenchidos no JSON.
            if projeto.get("repositorio"):
                st.link_button("Código", projeto["repositorio"])
            if projeto.get("demo"):
                st.link_button("Demo", projeto["demo"])

# --------------------------------------------------------------------------- #
# Mini-demo: exemplo de visualizacao com dados ficticios
#
# Serve para mostrar que o portfolio roda codigo de verdade, nao so texto.
# Troque por uma demo de um projeto seu quando tiver uma.
# --------------------------------------------------------------------------- #
cabecalho_secao(
    "Demonstração",
    "SLA por filial",
    "Exemplo de painel operacional. Os dados são fictícios (data/sla_exemplo.csv).",
)

dados = carregar_csv("sla_exemplo.csv")

coluna_grafico, coluna_tabela = st.columns([1.6, 1], gap="large")

with coluna_grafico:
    # Altair em vez de st.line_chart porque aqui precisamos fixar o dominio do
    # eixo Y: a variacao de SLA e pequena e, com o eixo comecando no zero, as
    # linhas ficariam coladas no topo e sem leitura.
    grafico = (
        alt.Chart(dados)
        .mark_line(point=True, strokeWidth=2.5)
        .encode(
            x=alt.X("mes:N", title="Mês"),
            y=alt.Y(
                "sla_pct:Q",
                title="SLA (%)",
                scale=alt.Scale(domain=[80, 100], nice=False),
            ),
            # Cores do tema, para o grafico conversar com o resto da pagina.
            color=alt.Color(
                "filial:N",
                title="Filial",
                scale=alt.Scale(range=CORES_GRAFICO),
            ),
            tooltip=["mes", "filial", "sla_pct", "entregas"],
        )
        .properties(height=320)
    )
    st.altair_chart(grafico, width="stretch")

with coluna_tabela:
    resumo = (
        dados.groupby("filial")
        .agg(entregas=("entregas", "sum"), sla_medio=("sla_pct", "mean"))
        .round({"sla_medio": 1})
        .reset_index()
    )
    st.dataframe(resumo, hide_index=True)
    st.caption("Valores fictícios, gerados apenas para a demonstração.")

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
