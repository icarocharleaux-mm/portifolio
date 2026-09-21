"""Pagina Contato: links diretos + formulario simples.

IMPORTANTE SOBRE O FORMULARIO
O Streamlit Community Cloud nao tem backend de e-mail. Este formulario
NAO envia e NAO armazena nada: ele apenas monta a mensagem e devolve um
link `mailto:` e um bloco para copiar. Os dados ficam na sessao do proprio
visitante e somem quando ele fecha a pagina.

Se um dia voce quiser receber de verdade, as opcoes sao:
  1. Apontar o form para um servico externo (Formspree, Getform, Basin);
  2. Enviar por SMTP usando credenciais em `st.secrets` -- nunca no codigo;
  3. Gravar em uma planilha/banco via API.
Em qualquer uma delas, vale a LGPD: avise o visitante o que voce coleta,
para que usa e por quanto tempo guarda.

TODO (voce): os links vem de `data/perfil.json` -> chave `links`.
"""

from __future__ import annotations

import re
from urllib.parse import quote

import streamlit as st

from utils import aplicar_css, cabecalho_secao, carregar_perfil, rodape

st.set_page_config(page_title="Contato | Portfolio", page_icon="✉️", layout="centered")
aplicar_css()

perfil = carregar_perfil()
links = perfil.get("links", {})

# Limites de tamanho -- validacao na entrada, antes de montar qualquer coisa.
LIMITE_NOME = 80
LIMITE_ASSUNTO = 120
LIMITE_MENSAGEM = 2000
PADRAO_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[A-Za-z]{2,}$")

st.title("Contato")
st.write("Aberto a conversas sobre automacao, dados e processos de logistica.")

# --------------------------------------------------------------------------- #
# Links diretos
# --------------------------------------------------------------------------- #
cabecalho_secao("Onde me encontrar")

# Ordem dos botoes na tela. Canal com valor vazio em data/perfil.json some
# sozinho -- e so apagar a URL para tirar do ar, sem mexer no codigo.
CANAIS = [
    ("linkedin", "LinkedIn"),
    ("whatsapp", "WhatsApp"),
    ("github", "GitHub"),
    ("site", "Site"),
]

botoes = [(rotulo, links[chave]) for chave, rotulo in CANAIS if links.get(chave)]

# O e-mail vem por ultimo porque precisa do prefixo mailto:.
if links.get("email"):
    botoes.append(("E-mail", f"mailto:{links['email']}"))

if botoes:
    colunas = st.columns(len(botoes), gap="medium")
    for coluna, (rotulo, url) in zip(colunas, botoes):
        with coluna:
            st.link_button(rotulo, url)
else:
    st.caption("Preencha `links` em data/perfil.json para exibir seus canais.")

st.divider()

# --------------------------------------------------------------------------- #
# Formulario
# --------------------------------------------------------------------------- #
cabecalho_secao(
    "Enviar uma mensagem",
    "O formulario monta o e-mail para voce. Nada e gravado nesta pagina.",
)

with st.form("formulario_contato", clear_on_submit=False):
    nome = st.text_input("Seu nome", max_chars=LIMITE_NOME, placeholder="Nome e sobrenome")
    email = st.text_input("Seu e-mail", max_chars=120, placeholder="voce@empresa.com")
    assunto = st.text_input(
        "Assunto", max_chars=LIMITE_ASSUNTO, placeholder="Sobre o que voce quer falar"
    )
    mensagem = st.text_area("Mensagem", max_chars=LIMITE_MENSAGEM, height=170)

    enviado = st.form_submit_button("Gerar mensagem")

if enviado:
    # Validacao simples de entrada.
    erros: list[str] = []
    nome = nome.strip()
    email = email.strip()
    assunto = assunto.strip() or "Contato pelo portfolio"
    mensagem = mensagem.strip()

    if len(nome) < 2:
        erros.append("Informe o seu nome.")
    if not PADRAO_EMAIL.match(email):
        erros.append("Informe um e-mail valido.")
    if len(mensagem) < 10:
        erros.append("Escreva uma mensagem com pelo menos 10 caracteres.")

    if erros:
        for erro in erros:
            st.error(erro, icon="⚠️")
    elif not links.get("email"):
        st.error(
            "Nenhum e-mail de destino configurado. Preencha `links.email` em "
            "data/perfil.json.",
            icon="⚠️",
        )
    else:
        corpo = f"{mensagem}\n\n---\nEnviado por: {nome} <{email}>"

        st.success("Mensagem pronta. Use o link abaixo ou copie o texto.", icon="✅")

        # `quote` escapa o conteudo para caber com seguranca em uma URL mailto.
        url_mailto = (
            f"mailto:{links['email']}"
            f"?subject={quote(assunto)}"
            f"&body={quote(corpo)}"
        )
        st.link_button("Abrir no meu cliente de e-mail", url_mailto)

        # O endereco de destino NAO entra aqui de proposito: ele so existe no
        # href do botao acima. Imprimir "Para: <email>" na tela devolveria o
        # endereco para qualquer robo que le o texto da pagina.
        with st.expander("Ou copie o texto da mensagem"):
            st.code(f"Assunto: {assunto}\n\n{corpo}", language="text")

        st.caption(
            "Esta pagina nao guarda o que voce digitou. O conteudo so sai daqui "
            "quando voce mesmo envia pelo seu cliente de e-mail."
        )

rodape()
