"""Estilizacao compartilhada: CSS global, cards, tags, barras de nivel.

Regra de ouro deste modulo: todo texto vindo de `data/` passa por `html.escape`
antes de entrar no HTML. Assim um acento, um `&` ou um `<` em um JSON nunca
quebra o layout nem injeta marcacao.

O HTML e montado sem identacao de propósito: o Streamlit trata linha com 4
espacos como bloco de codigo e o card apareceria cru na tela.
"""

from __future__ import annotations

from html import escape
from typing import Any, Iterable

import streamlit as st

# --------------------------------------------------------------------------- #
# Paleta -- mantenha em sincronia com .streamlit/config.toml
# --------------------------------------------------------------------------- #
PALETA = {
    "primaria": "#3D5A80",      # azul ardosia -- acentos, titulos, links
    "primaria_clara": "#5B7CA6",
    "texto": "#1F2933",         # quase preto, mais suave que #000
    "texto_suave": "#62707F",   # textos secundarios
    "fundo": "#FFFFFF",
    "superficie": "#F4F6F8",    # fundo dos cards
    "borda": "#E2E7EC",
    "sucesso": "#2E7D5B",
    "aviso": "#B26B00",
}


def aplicar_css() -> None:
    """Injeta o CSS global. Chame uma vez no inicio de cada pagina."""
    st.markdown(
        f"""
<style>
:root {{
  --cor-primaria: {PALETA["primaria"]};
  --cor-primaria-clara: {PALETA["primaria_clara"]};
  --cor-texto: {PALETA["texto"]};
  --cor-texto-suave: {PALETA["texto_suave"]};
  --cor-superficie: {PALETA["superficie"]};
  --cor-borda: {PALETA["borda"]};
  --cor-sucesso: {PALETA["sucesso"]};
}}

/* Deixa o conteudo um pouco mais estreito -- melhora a leitura */
.block-container {{ padding-top: 2.5rem; max-width: 1100px; }}

/* ---------- Card de projeto ---------- */
.pf-card {{
  background: var(--cor-superficie);
  border: 1px solid var(--cor-borda);
  border-left: 4px solid var(--cor-primaria);
  border-radius: 10px;
  padding: 1.1rem 1.25rem;
  margin-bottom: 0.9rem;
  height: 100%;
}}
.pf-card h4 {{
  margin: 0 0 .35rem 0;
  font-size: 1.05rem;
  color: var(--cor-texto);
  line-height: 1.35;
}}
.pf-card p {{
  margin: 0;
  color: var(--cor-texto-suave);
  font-size: .92rem;
  line-height: 1.5;
}}
.pf-card .pf-icone {{ font-size: 1.5rem; display: block; margin-bottom: .4rem; }}
.pf-card .pf-meta {{
  display: block;
  margin-top: .6rem;
  font-size: .78rem;
  text-transform: uppercase;
  letter-spacing: .04em;
  color: var(--cor-primaria);
  font-weight: 600;
}}

/* ---------- Bloco problema / solucao / resultado ---------- */
.pf-bloco {{ margin-bottom: 1rem; }}
.pf-bloco .pf-rotulo {{
  font-size: .75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: .06em;
  color: var(--cor-primaria);
  margin-bottom: .25rem;
}}
.pf-bloco .pf-conteudo {{ color: var(--cor-texto); line-height: 1.6; font-size: .94rem; }}

/* ---------- Tags de tecnologia ---------- */
.pf-tags {{ display: flex; flex-wrap: wrap; gap: .4rem; margin: .2rem 0 .2rem 0; }}
.pf-tag {{
  background: #FFFFFF;
  border: 1px solid var(--cor-borda);
  color: var(--cor-texto-suave);
  border-radius: 999px;
  padding: .18rem .65rem;
  font-size: .78rem;
  white-space: nowrap;
}}

/* ---------- Barra de nivel de skill ---------- */
.pf-skill {{ margin-bottom: .7rem; }}
.pf-skill-topo {{
  display: flex; justify-content: space-between;
  font-size: .88rem; color: var(--cor-texto); margin-bottom: .2rem;
}}
.pf-skill-topo span:last-child {{ color: var(--cor-texto-suave); font-size: .8rem; }}
.pf-skill-trilho {{
  background: var(--cor-borda); border-radius: 999px; height: 7px; overflow: hidden;
}}
.pf-skill-preenchido {{
  background: var(--cor-primaria); height: 100%; border-radius: 999px;
}}

/* ---------- Cabecalho de secao ---------- */
.pf-secao {{ margin: 1.6rem 0 .9rem 0; }}
.pf-secao h3 {{ margin: 0; font-size: 1.25rem; color: var(--cor-texto); }}
.pf-secao p {{ margin: .2rem 0 0 0; color: var(--cor-texto-suave); font-size: .9rem; }}

/* ---------- Rodape ---------- */
.pf-rodape {{
  margin-top: 2.5rem; padding-top: 1rem;
  border-top: 1px solid var(--cor-borda);
  color: var(--cor-texto-suave); font-size: .82rem; text-align: center;
}}
</style>
""",
        unsafe_allow_html=True,
    )


# --------------------------------------------------------------------------- #
# Componentes
# --------------------------------------------------------------------------- #


def cabecalho_secao(titulo: str, subtitulo: str | None = None) -> None:
    """Titulo de secao com subtitulo opcional."""
    partes = ['<div class="pf-secao">', f"<h3>{escape(titulo)}</h3>"]
    if subtitulo:
        partes.append(f"<p>{escape(subtitulo)}</p>")
    partes.append("</div>")
    st.markdown("".join(partes), unsafe_allow_html=True)


def lista_de_tags(tags: Iterable[str]) -> None:
    """Renderiza uma lista de tecnologias como pills."""
    itens = "".join(f'<span class="pf-tag">{escape(str(t))}</span>' for t in tags)
    st.markdown(f'<div class="pf-tags">{itens}</div>', unsafe_allow_html=True)


def card_projeto(projeto: dict[str, Any]) -> None:
    """Card compacto de projeto -- usado na Home.

    Espera as chaves: titulo, resumo, categoria, icone (todas opcionais).
    """
    partes = ['<div class="pf-card">']

    if projeto.get("icone"):
        partes.append(f'<span class="pf-icone">{escape(projeto["icone"])}</span>')

    partes.append(f'<h4>{escape(projeto.get("titulo", "Sem titulo"))}</h4>')
    partes.append(f'<p>{escape(projeto.get("resumo", ""))}</p>')

    if projeto.get("categoria"):
        partes.append(f'<span class="pf-meta">{escape(projeto["categoria"])}</span>')

    partes.append("</div>")
    st.markdown("".join(partes), unsafe_allow_html=True)


def bloco_rotulado(rotulo: str, conteudo: str) -> None:
    """Par rotulo + texto, usado no detalhe do projeto (Problema, Solucao...)."""
    st.markdown(
        '<div class="pf-bloco">'
        f'<div class="pf-rotulo">{escape(rotulo)}</div>'
        f'<div class="pf-conteudo">{escape(conteudo)}</div>'
        "</div>",
        unsafe_allow_html=True,
    )


def skill(nome: str, nivel: Any = None) -> None:
    """Renderiza uma skill, adaptando-se ao formato do nivel informado.

    Aceita os tres casos que aparecem em `data/skills.json`:
      - numero (0 a 100)            -> barra de proficiencia
      - texto ("Avancado", "Basico") -> nome seguido do rotulo
      - vazio / ausente              -> so o nome
    """
    if nivel is None or (isinstance(nivel, str) and not nivel.strip()):
        st.markdown(f"- {escape(nome)}")
        return

    if isinstance(nivel, (int, float)) or str(nivel).strip().isdigit():
        barra_de_nivel(nome, int(float(nivel)))
        return

    st.markdown(
        f'- {escape(nome)} <span class="pf-tag">{escape(str(nivel))}</span>',
        unsafe_allow_html=True,
    )


def barra_de_nivel(nome: str, nivel: int) -> None:
    """Barra horizontal de proficiencia. `nivel` vai de 0 a 100."""
    nivel = max(0, min(100, int(nivel)))
    st.markdown(
        '<div class="pf-skill">'
        '<div class="pf-skill-topo">'
        f"<span>{escape(nome)}</span><span>{nivel}%</span>"
        "</div>"
        '<div class="pf-skill-trilho">'
        f'<div class="pf-skill-preenchido" style="width:{nivel}%"></div>'
        "</div>"
        "</div>",
        unsafe_allow_html=True,
    )


def avatar(caminho_relativo: str, largura: int = 190) -> None:
    """Mostra a foto/avatar a partir de um caminho relativo a raiz do projeto.

    Aceita SVG (renderizado inline, porque `st.image` nao lida bem com SVG) e
    formatos raster (PNG/JPG, via `st.image`). Para trocar o placeholder pela
    sua foto: coloque o arquivo em `assets/` e aponte `avatar` em
    `data/perfil.json` para ele -- por exemplo `"assets/foto.jpg"`.
    """
    from utils.data_loader import BASE_DIR  # import local evita ciclo de import

    caminho = (BASE_DIR / caminho_relativo).resolve()

    if BASE_DIR.resolve() not in caminho.parents or not caminho.is_file():
        st.info("Avatar nao encontrado. Confira o campo `avatar` em data/perfil.json.")
        return

    if caminho.suffix.lower() == ".svg":
        svg = caminho.read_text(encoding="utf-8")
        st.markdown(
            f'<div style="width:{largura}px;max-width:100%">{svg}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.image(str(caminho), width=largura)


def rodape(texto: str = "Portfolio pessoal construido com Streamlit.") -> None:
    """Rodape padrao das paginas."""
    st.markdown(f'<div class="pf-rodape">{escape(texto)}</div>', unsafe_allow_html=True)
