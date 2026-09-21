"""Carregamento dos dados de exemplo da pasta `data/`.

Tudo que as paginas mostram vem daqui. Para trocar o conteudo de exemplo pelo
conteudo real, edite os arquivos em `data/` -- nenhuma pagina precisa ser mexida.

Os arquivos sao lidos com cache do Streamlit, entao alterar um JSON exige um
rerun com "Clear cache" (menu do canto superior direito) ou reiniciar o app.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st

# Raiz do projeto (a pasta que contem app.py) e a pasta de dados.
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"

# Tempo de cache em segundos. 0 = cache permanente enquanto o app roda.
_TTL = 600


def _caminho_seguro(nome_arquivo: str) -> Path:
    """Resolve `nome_arquivo` dentro de `data/` e recusa qualquer coisa fora.

    Barra travessia de diretorio (`../`, caminho absoluto, link simbolico que
    aponte para fora). Hoje so o proprio codigo chama isso, mas se um dia o nome
    do arquivo vier de um input do usuario a validacao ja esta no lugar.
    """
    alvo = (DATA_DIR / nome_arquivo).resolve()
    raiz = DATA_DIR.resolve()

    if raiz not in alvo.parents:
        raise ValueError(f"Caminho fora da pasta data/: {nome_arquivo!r}")
    if not alvo.is_file():
        raise FileNotFoundError(f"Arquivo nao encontrado: data/{nome_arquivo}")

    return alvo


@st.cache_data(ttl=_TTL, show_spinner=False)
def carregar_json(nome_arquivo: str) -> Any:
    """Le um arquivo JSON de `data/` e devolve dict ou list."""
    caminho = _caminho_seguro(nome_arquivo)
    with caminho.open("r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


@st.cache_data(ttl=_TTL, show_spinner=False)
def carregar_csv(nome_arquivo: str, **kwargs: Any) -> pd.DataFrame:
    """Le um CSV de `data/` como DataFrame."""
    caminho = _caminho_seguro(nome_arquivo)
    return pd.read_csv(caminho, **kwargs)


# --------------------------------------------------------------------------- #
# Atalhos de alto nivel usados pelas paginas
# --------------------------------------------------------------------------- #


def carregar_perfil() -> dict[str, Any]:
    """Dados do dono do portfolio (data/perfil.json)."""
    return carregar_json("perfil.json")


def carregar_skills() -> dict[str, Any]:
    """Skills tecnicas agrupadas por categoria (data/skills.json)."""
    return carregar_json("skills.json")


def carregar_projetos() -> list[dict[str, Any]]:
    """Lista de projetos (data/projetos.json), sem as chaves de comentario."""
    projetos = carregar_json("projetos.json")
    # As chaves que comecam com "_" sao anotacoes para voce, nao devem aparecer.
    return [
        {chave: valor for chave, valor in projeto.items() if not chave.startswith("_")}
        for projeto in projetos
    ]


def projetos_em_destaque(limite: int | None = None) -> list[dict[str, Any]]:
    """Projetos marcados com `"destaque": true`, usados na Home."""
    destaques = [p for p in carregar_projetos() if p.get("destaque")]
    return destaques[:limite] if limite else destaques
