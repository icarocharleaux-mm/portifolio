"""Pagina Projetos: cada projeto em um expander, no formato
problema -> solucao -> tecnologias -> resultado.

TODO (voce): OS TRES PROJETOS SAO EXEMPLOS COM DADOS 100% FICTICIOS.
Para colocar os seus projetos reais, edite `data/projetos.json`:

  - `titulo`, `resumo`      -> nome e uma linha de descricao
  - `problema`              -> o gargalo, em linguagem de negocio
  - `solucao`               -> o que voce construiu
  - `tecnologias`           -> lista de strings (vira tag na tela)
  - `resultado`             -> lista de bullets com o impacto medido
  - `destaque`              -> true para o card aparecer na Home
  - `repositorio` / `demo`  -> URLs; deixe "" para esconder o botao

Regra que vale para tudo aqui: nada de nome real de empresa, filial ou
cliente, e nenhum dado pessoal. Numeros em projetos fechados devem ser
apresentados como variacao percentual, nunca como base bruta.
"""

import altair as alt
import streamlit as st

from utils import (
    aplicar_css,
    bloco_rotulado,
    cabecalho_secao,
    carregar_csv,
    carregar_projetos,
    lista_de_tags,
    rodape,
)

st.set_page_config(
    page_title="Projetos | Portfolio", page_icon="\U0001f6e0️", layout="wide"
)
aplicar_css()

projetos = carregar_projetos()

st.title("Projetos")
st.write(
    "Cada bloco segue a mesma estrutura: o problema da operacao, a solucao "
    "entregue, o que foi usado e o impacto."
)

st.info(
    "Os casos abaixo estao descritos de forma anonimizada: sem nome de empresa, "
    "filial, cliente ou fornecedor, e sem numero operacional bruto.",
    icon="ℹ️",
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
                bloco_rotulado("Solucao", projeto["solucao"])
            if projeto.get("aprendizado"):
                bloco_rotulado("O que eu tirei disso", projeto["aprendizado"])

        with coluna_lateral:
            if projeto.get("tecnologias"):
                st.markdown("**Tecnologias**")
                lista_de_tags(projeto["tecnologias"])

            if projeto.get("resultado"):
                st.markdown("**Resultado / impacto**")
                for linha in projeto["resultado"]:
                    st.markdown(f"- {linha}")

            # Links opcionais: so aparecem se preenchidos no JSON.
            if projeto.get("repositorio"):
                st.link_button("Codigo", projeto["repositorio"])
            if projeto.get("demo"):
                st.link_button("Demo", projeto["demo"])

st.divider()

# --------------------------------------------------------------------------- #
# Mini-demo: exemplo de visualizacao com dados ficticios
#
# Serve para mostrar que o portfolio roda codigo de verdade, nao so texto.
# Troque por uma demo de um projeto seu quando tiver uma.
# --------------------------------------------------------------------------- #
cabecalho_secao(
    "Mini-demo: SLA por filial",
    "Amostra de visualizacao usando data/sla_exemplo.csv (dados ficticios).",
)

dados = carregar_csv("sla_exemplo.csv")

coluna_grafico, coluna_tabela = st.columns([1.6, 1], gap="large")

with coluna_grafico:
    # Altair em vez de st.line_chart porque aqui precisamos fixar o dominio do
    # eixo Y: a variacao de SLA e pequena e, com o eixo comecando no zero, as
    # linhas ficariam coladas no topo e sem leitura.
    grafico = (
        alt.Chart(dados)
        .mark_line(point=True)
        .encode(
            x=alt.X("mes:N", title="Mes"),
            y=alt.Y(
                "sla_pct:Q",
                title="SLA (%)",
                scale=alt.Scale(domain=[80, 100], nice=False),
            ),
            color=alt.Color("filial:N", title="Filial"),
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
    st.caption("Valores ficticios, gerados apenas para a demonstracao.")

rodape()
