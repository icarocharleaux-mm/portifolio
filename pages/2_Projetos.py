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
    aviso_demo,
    bloco_rotulado,
    cabecalho_secao,
    carregar_json,
    carregar_perfil,
    carregar_projetos,
    coluna_funil,
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
# `required=True` e obrigatorio: em selection_mode="single" sem ele, clicar na
# pilula ja ativa a desmarca, o widget devolve None e o filtro quebra.
categorias = sorted({p.get("categoria", "Outros") for p in projetos})
escolhida = st.pills(
    "Filtrar por tipo de trabalho",
    options=["Todos"] + categorias,
    selection_mode="single",
    default="Todos",
    required=True,
)

visiveis = (
    projetos
    if escolhida == "Todos"
    else [p for p in projetos if p.get("categoria", "Outros") == escolhida]
)

# --------------------------------------------------------------------------- #
# Lista de projetos
# --------------------------------------------------------------------------- #
# Titulo, metadados e resumo ficam FORA do expander. Antes o cabecalho era so
# icone + titulo, e o campo `resumo` -- uma frase pronta em cada projeto -- nao
# era renderizado em lugar nenhum desta pagina: o visitante via nove rotulos
# mudos e precisava abrir cada um para saber se interessava.
for projeto in visiveis:
    st.markdown(f"##### {projeto.get('icone', '')} {projeto['titulo']}".strip())

    meta = " · ".join(
        filtro
        for filtro in (projeto.get("categoria"), projeto.get("periodo"))
        if filtro
    )
    if meta:
        st.caption(meta)

    if projeto.get("resumo"):
        st.write(projeto["resumo"])

    with st.expander("Problema, solução e resultado"):
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
# Demonstracao interativa: o funil da plataforma de triagem
#
# Esta e uma RECRIACAO do fluxo em Streamlit, nao a plataforma real (NestJS,
# PostgreSQL, Redis e Next.js em contedor). Existe para o visitante manusear a
# mecanica -- mover candidato, ver a trilha de auditoria crescer -- em vez de
# so ler que ela existe. Os dados sao ficticios e nao ha nenhum campo pessoal.
#
# O estado vive em st.session_state, entao cada visitante mexe na propria
# copia: um nao interfere no outro, e nada e gravado em lugar nenhum.
# --------------------------------------------------------------------------- #
cabecalho_secao(
    "Demonstração",
    "Funil de triagem, funcionando",
    "Mova um candidato e veja a trilha de auditoria registrar a transição.",
)

aviso_demo(
    "Esta tela é uma <b>recriação do fluxo</b> em Streamlit, para você manusear a "
    "mecânica aqui mesmo. A plataforma real roda em NestJS, PostgreSQL, Redis e "
    "Next.js, em contêiner. Os candidatos são <b>fictícios</b> — sem nome, documento "
    "ou telefone — e nada do que você fizer aqui é gravado."
)

demo = carregar_json("demo_triagem.json")
ETAPAS = [e["nome"] for e in demo["etapas"]]

# Primeira visita da sessao: copia o estado inicial do JSON.
if "triagem_candidatos" not in st.session_state:
    st.session_state.triagem_candidatos = [dict(c) for c in demo["candidatos"]]
    st.session_state.triagem_auditoria = []


def _mover(codigo: str, destino: str) -> None:
    """Move um candidato e registra a transicao, como o sistema real faz."""
    for candidato in st.session_state.triagem_candidatos:
        if candidato["codigo"] == codigo:
            origem = candidato["etapa"]
            if origem == destino:
                return
            candidato["etapa"] = destino
            st.session_state.triagem_auditoria.insert(
                0, {"codigo": codigo, "de": origem, "para": destino}
            )
            return


# --- Quadro: uma coluna por etapa -------------------------------------------
colunas = st.columns(len(ETAPAS), gap="medium")

for coluna, etapa in zip(colunas, demo["etapas"]):
    nome = etapa["nome"]
    fichas = [
        {
            "codigo": c["codigo"],
            "meta": [
                f"{c['veiculo']} · {c['regiao']}",
                f"{c['documentos']}/{demo['documentos_exigidos']} documentos · {c['dias_no_funil']}d no funil",
            ],
        }
        for c in st.session_state.triagem_candidatos
        if c["etapa"] == nome
    ]
    with coluna:
        coluna_funil(nome, etapa["descricao"], fichas)

# --- Controles ---------------------------------------------------------------
st.write("")
controle_candidato, controle_etapa, controle_acao = st.columns([2, 2, 1], gap="medium")

with controle_candidato:
    escolhido = st.selectbox(
        "Candidato",
        options=[c["codigo"] for c in st.session_state.triagem_candidatos],
        help="Código mascarado, como aparece no painel real.",
    )

with controle_etapa:
    atual = next(
        c["etapa"] for c in st.session_state.triagem_candidatos if c["codigo"] == escolhido
    )
    destino = st.selectbox(
        "Mover para", options=ETAPAS, index=ETAPAS.index(atual)
    )

with controle_acao:
    st.write("")
    if st.button("Mover", type="primary", use_container_width=True):
        _mover(escolhido, destino)
        st.rerun()

# --- Trilha de auditoria ------------------------------------------------------
auditoria = st.session_state.triagem_auditoria

if auditoria:
    quantas = len(auditoria)
    rotulo(f"Trilha de auditoria · {quantas} {'movimentação' if quantas == 1 else 'movimentações'}")
    lista([f"`{a['codigo']}` — {a['de']} → **{a['para']}**" for a in auditoria[:8]])
    if quantas > 8:
        restantes = quantas - 8
        st.caption(
            f"…e mais {restantes} {'registro' if restantes == 1 else 'registros'} anteriores."
        )
    if st.button("Reiniciar a simulação"):
        del st.session_state.triagem_candidatos
        del st.session_state.triagem_auditoria
        st.rerun()
else:
    st.caption(
        "Nenhuma movimentação ainda. Cada transição que você fizer aparece aqui — "
        "no sistema real, gravada com autor, data e etapa de origem."
    )

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
