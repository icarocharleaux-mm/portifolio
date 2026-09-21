"""Funcoes auxiliares compartilhadas entre as paginas do portfolio.

Reexporta o que as paginas usam, para que o import fique curto:

    from utils import carregar_projetos, aplicar_css
"""

from utils.data_loader import (
    BASE_DIR,
    DATA_DIR,
    carregar_csv,
    carregar_json,
    carregar_perfil,
    carregar_projetos,
    carregar_skills,
    projetos_em_destaque,
)
from utils.styles import (
    CORES_GRAFICO,
    PALETA,
    ROTAS,
    aplicar_css,
    avatar,
    barra_de_nivel,
    bloco_rotulado,
    botoes,
    cabecalho_secao,
    card_projeto,
    card_servico,
    card_solucao,
    estimativa,
    faixa_cta,
    hero,
    lista,
    lista_de_tags,
    passo,
    rodape,
    rotulo,
    skill,
)

__all__ = [
    "BASE_DIR",
    "DATA_DIR",
    "carregar_csv",
    "carregar_json",
    "carregar_perfil",
    "carregar_projetos",
    "carregar_skills",
    "projetos_em_destaque",
    "CORES_GRAFICO",
    "PALETA",
    "ROTAS",
    "aplicar_css",
    "avatar",
    "barra_de_nivel",
    "bloco_rotulado",
    "botoes",
    "cabecalho_secao",
    "card_projeto",
    "card_servico",
    "card_solucao",
    "estimativa",
    "faixa_cta",
    "hero",
    "lista",
    "lista_de_tags",
    "passo",
    "rodape",
    "rotulo",
    "skill",
]
