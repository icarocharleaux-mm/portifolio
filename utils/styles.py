"""Componentes visuais compartilhados.

O CSS mora em `assets/tema.css` -- para mudar cores, espacamentos ou o
gradiente, mexa la (nas variaveis de `:root`), nao aqui. Este modulo so
monta o HTML que consome aquelas classes.

Regra de ouro: todo texto vindo de `data/` passa por `html.escape` antes de
entrar no HTML. Assim um `&`, um `<` ou um acento em um JSON nunca quebra o
layout nem injeta marcacao.

O HTML e montado sem identacao de proposito: o Streamlit trata linha com 4
espacos como bloco de codigo e o card apareceria cru na tela.
"""

from __future__ import annotations

from html import escape
from typing import Any, Iterable, Sequence

import streamlit as st

# Paleta espelhada de assets/tema.css e de .streamlit/config.toml.
# Usada pelo Python (graficos, por exemplo); o CSS tem a sua propria copia.
PALETA = {
    "fundo": "#0B0F17",
    "superficie": "#131A26",
    "borda": "#22304A",
    "acento": "#22D3EE",
    "acento_2": "#6366F1",
    "acento_3": "#A78BFA",
    "texto": "#E6EDF7",
    "suave": "#8FA3BF",
}

# Sequencia de cores para series de grafico, na ordem de uso.
CORES_GRAFICO = [PALETA["acento"], PALETA["acento_2"], PALETA["acento_3"]]


def _render(html: str) -> None:
    """Renderiza HTML proprio.

    Usa `st.html` em vez de `st.markdown(unsafe_allow_html=True)` porque o
    renderizador de Markdown do Streamlit reescreve toda tag <a> com
    target="_blank" -- o que faria os botoes internos do portfolio abrirem
    em aba nova a cada clique.
    """
    st.html(html)


def aplicar_css() -> None:
    """Injeta `assets/tema.css`. Chame uma vez no inicio de cada pagina."""
    from utils.data_loader import BASE_DIR  # import local evita ciclo de import

    caminho = BASE_DIR / "assets" / "tema.css"

    if not caminho.is_file():
        st.error("assets/tema.css não encontrado — a página vai abrir sem estilo.")
        return

    st.markdown(f"<style>{caminho.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


# --------------------------------------------------------------------------- #
# Botoes e navegacao
# --------------------------------------------------------------------------- #

# Destinos internos. As paginas do Streamlit ficam em /<Nome>, sem o prefixo
# numerico do arquivo. Sao links relativos para funcionar tanto local quanto
# no Streamlit Cloud.
ROTAS = {
    "home": ".",
    "servicos": "Servicos",
    "projetos": "Projetos",
    "sobre": "Sobre",
    "contato": "Contato",
}


def _html_botoes(botoes: Sequence[tuple[str, str, str]]) -> str:
    """Monta a barra de botoes. Cada item e (rotulo, url, estilo).

    `estilo` e "primario" ou "secundario".
    """
    partes = ['<div class="pf-ctas">']

    for rotulo, url, estilo in botoes:
        classe = "pf-btn-primario" if estilo == "primario" else "pf-btn-secundario"
        # Link externo abre em nova aba; interno navega na propria aba.
        alvo = ' target="_blank" rel="noopener noreferrer"' if url.startswith(("http", "mailto:")) else ""
        partes.append(
            f'<a class="pf-btn {classe}" href="{escape(url, quote=True)}"{alvo}>{escape(rotulo)}</a>'
        )

    partes.append("</div>")
    return "".join(partes)


def botoes(itens: Sequence[tuple[str, str, str]]) -> None:
    """Renderiza uma barra de botoes. Ver `_html_botoes` para o formato."""
    _render(_html_botoes(itens))


# --------------------------------------------------------------------------- #
# Blocos de pagina
# --------------------------------------------------------------------------- #


def hero(
    kicker: str,
    titulo: str,
    titulo_destaque: str = "",
    subtitulo: str = "",
    descricao: str = "",
    localizacao: str = "",
    acoes: Sequence[tuple[str, str, str]] = (),
) -> None:
    """Bloco de abertura da pagina, em dois formatos.

    `titulo_destaque` continua a frase DENTRO do <h1>, no mesmo tamanho, so
    trocando a cor pelo gradiente. Serve para uma frase unica quebrada em
    duas linhas -- e o que as paginas internas usam.

    `subtitulo` sai em um <h2> proprio, bem menor e mais leve que o <h1>.
    Serve quando o titulo e o nome e a frase e um complemento -- e o que a
    Home usa, para o nome ser o destaque absoluto.

    Os dois podem coexistir, mas em geral so um deles e preenchido.
    """
    # Com subtitulo, o <h1> e um nome proprio e recebe a escala de marca.
    # Sem ele, o <h1> carrega uma frase e fica na escala de leitura.
    classes = "pf-hero pf-anima" + (" pf-hero-nome" if subtitulo else "")
    partes = [f'<div class="{classes}">']

    if kicker:
        partes.append(f'<span class="pf-eyebrow">{escape(kicker)}</span>')

    partes.append("<h1>")
    if titulo:
        partes.append(escape(titulo))
    if titulo_destaque:
        separador = "<br>" if titulo else ""
        partes.append(f'{separador}<span class="pf-grad">{escape(titulo_destaque)}</span>')
    partes.append("</h1>")

    if subtitulo:
        partes.append(f'<h2 class="pf-hero-sub pf-grad">{escape(subtitulo)}</h2>')

    if descricao:
        partes.append(f'<p class="pf-lead">{escape(descricao)}</p>')

    if localizacao:
        partes.append(f'<div class="pf-local">\U0001f4cd {escape(localizacao)}</div>')

    if acoes:
        partes.append(_html_botoes(acoes))

    partes.append("</div>")
    _render("".join(partes))


def cabecalho_secao(kicker: str, titulo: str, subtitulo: str = "") -> None:
    """Titulo de secao com etiqueta acima e subtitulo opcional."""
    partes = ['<div class="pf-secao pf-anima">']

    if kicker:
        partes.append(f'<div class="pf-kicker">{escape(kicker)}</div>')

    partes.append(f"<h3>{escape(titulo)}</h3>")

    if subtitulo:
        partes.append(f"<p>{escape(subtitulo)}</p>")

    partes.append("</div>")
    _render("".join(partes))


def card_projeto(projeto: dict[str, Any], atraso: int = 0) -> None:
    """Card compacto de projeto, usado na Home.

    `atraso` (1 a 4) escalona a animacao de entrada quando os cards estao
    lado a lado, para eles nao subirem todos no mesmo instante.
    """
    _card(
        icone=projeto.get("icone", ""),
        titulo=projeto.get("titulo", "Sem titulo"),
        texto=projeto.get("resumo", ""),
        rodape_=projeto.get("categoria", ""),
        atraso=atraso,
    )


def card_solucao(icone: str, titulo: str, texto: str, atraso: int = 0) -> None:
    """Card da secao 'o que eu resolvo'."""
    _card(icone=icone, titulo=titulo, texto=texto, rodape_="", atraso=atraso)


def _card(icone: str, titulo: str, texto: str, rodape_: str, atraso: int) -> None:
    """Estrutura comum dos cards."""
    classes = "pf-card pf-anima" + (f" pf-d{atraso}" if 1 <= atraso <= 4 else "")
    partes = [f'<div class="{classes}">']

    if icone:
        partes.append(f'<span class="pf-icone">{escape(icone)}</span>')

    partes.append(f"<h4>{escape(titulo)}</h4>")
    partes.append(f"<p>{escape(texto)}</p>")

    if rodape_:
        partes.append(f'<span class="pf-meta">{escape(rodape_)}</span>')

    partes.append("</div>")
    _render("".join(partes))


def card_servico(
    icone: str,
    titulo: str,
    texto: str,
    entregaveis: Sequence[str] = (),
    prova: str = "",
    atraso: int = 0,
) -> None:
    """Card de pacote de servico: descricao, entregaveis e o caso que comprova."""
    classes = "pf-card pf-anima" + (f" pf-d{atraso}" if 1 <= atraso <= 4 else "")
    partes = [f'<div class="{classes}">']

    if icone:
        partes.append(f'<span class="pf-icone">{escape(icone)}</span>')

    partes.append(f"<h4>{escape(titulo)}</h4>")
    partes.append(f"<p>{escape(texto)}</p>")

    if entregaveis:
        itens = "".join(f"<li>{escape(str(i))}</li>" for i in entregaveis)
        partes.append(f'<ul class="pf-entregaveis">{itens}</ul>')

    if prova:
        partes.append(f'<span class="pf-prova"><b>Comprovado em</b>{escape(prova)}</span>')

    partes.append("</div>")
    _render("".join(partes))


def passo(numero: str, titulo: str, texto: str) -> None:
    """Etapa numerada do processo de trabalho."""
    _render(
        '<div class="pf-passo pf-anima">'
        f'<span class="pf-passo-num">{escape(numero)}</span>'
        f"<h4>{escape(titulo)}</h4>"
        f"<p>{escape(texto)}</p>"
        "</div>"
    )


def estimativa(texto: str) -> None:
    """Ganho projetado.

    Sai com rotulo e borda tracejada de proposito: numero estimado nao pode
    ser lido como numero medido. O que foi verificado vai em `resultado`.
    """
    _render(
        '<div class="pf-estimativa">'
        "<b>Ganho estimado</b>"
        f"{escape(texto)}"
        "</div>"
    )


def faixa_cta(titulo: str, texto: str, acoes: Sequence[tuple[str, str, str]]) -> None:
    """Faixa de fechamento convidando ao contato."""
    _render(
        '<div class="pf-cta-faixa pf-anima">'
        f"<h3>{escape(titulo)}</h3>"
        f"<p>{escape(texto)}</p>"
        f"{_html_botoes(acoes)}"
        "</div>"
    )


# --------------------------------------------------------------------------- #
# Elementos menores
# --------------------------------------------------------------------------- #


def lista_de_tags(tags: Iterable[str]) -> None:
    """Renderiza uma lista de tecnologias como pills."""
    itens = "".join(f'<span class="pf-tag">{escape(str(t))}</span>' for t in tags)
    _render(f'<div class="pf-tags">{itens}</div>')


def bloco_rotulado(rotulo: str, conteudo: str) -> None:
    """Par rotulo + texto, usado no detalhe do projeto (Problema, Solucao...)."""
    _render(
        '<div class="pf-bloco">'
        f'<div class="pf-rotulo">{escape(rotulo)}</div>'
        f'<div class="pf-conteudo">{escape(conteudo)}</div>'
        "</div>"
    )


def skill(nome: str, nivel: Any = None) -> None:
    """Renderiza uma skill, adaptando-se ao formato do nivel informado.

    Aceita os tres casos que aparecem em `data/skills.json`:
      - numero (0 a 100)             -> barra de proficiencia
      - texto ("Avancado", "Basico") -> nome seguido do rotulo
      - vazio / ausente              -> so o nome
    """
    if nivel is None or (isinstance(nivel, str) and not nivel.strip()):
        _render(f'<div class="pf-tags"><span class="pf-tag">{escape(nome)}</span></div>')
        return

    if isinstance(nivel, (int, float)) or str(nivel).strip().isdigit():
        barra_de_nivel(nome, int(float(nivel)))
        return

    _render(
        '<div class="pf-tags">'
        f'<span class="pf-tag">{escape(nome)} · {escape(str(nivel))}</span>'
        "</div>"
    )


def barra_de_nivel(nome: str, nivel: int) -> None:
    """Barra horizontal de proficiencia. `nivel` vai de 0 a 100."""
    nivel = max(0, min(100, int(nivel)))
    _render(
        '<div class="pf-skill">'
        '<div class="pf-skill-topo">'
        f"<span>{escape(nome)}</span><span>{nivel}%</span>"
        "</div>"
        '<div class="pf-skill-trilho">'
        f'<div class="pf-skill-preenchido" style="width:{nivel}%"></div>'
        "</div>"
        "</div>"
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
        st.info("Avatar não encontrado. Confira o campo `avatar` em data/perfil.json.")
        return

    if caminho.suffix.lower() == ".svg":
        svg = caminho.read_text(encoding="utf-8")
        _render(f'<div style="width:{largura}px;max-width:100%">{svg}</div>')
    else:
        st.image(str(caminho), width=largura)


def rodape(autor: str = "", nota: str = "") -> None:
    """Rodape padrao das paginas.

    `autor` sai como credito de autoria do portfolio; `nota` e uma linha
    menor abaixo, para avisos (anonimizacao dos dados, por exemplo).
    """
    creditos = "Desenvolvido e construído com Python + Streamlit"
    if autor:
        creditos = (
            f"Portfólio desenvolvido e construído por <strong>{escape(autor)}</strong>"
            " · Python + Streamlit"
        )

    partes = [f'<div class="pf-rodape">{creditos}']

    if nota:
        partes.append(f'<div class="pf-rodape-nota">{escape(nota)}</div>')

    partes.append("</div>")
    _render("".join(partes))
