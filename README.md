# Portfolio — Automação e TI para Logística

Portfólio pessoal em [Streamlit](https://streamlit.io), multi-página, pensado para
mostrar ferramentas internas de logística: roteirização, geocoding, checklists
digitais, automações de e-mail e dashboards operacionais.

> **Nada de dado sensível aqui.** Os casos em `data/projetos.json` são reais, mas
> descritos de forma anonimizada: sem nome de empresa, filial, cliente ou
> fornecedor, sem número operacional bruto e sem dado pessoal. O CSV usado na
> mini-demo (`data/sla_exemplo.csv`) é inteiramente fictício.

---

## Rodando localmente

Pré-requisito: Python 3.10 ou superior.

```bash
python -m venv .venv
```

```bash
.venv\Scripts\activate
```

```bash
pip install -r requirements.txt
```

```bash
streamlit run app.py
```

O app sobe em `http://localhost:8501`. No Linux/macOS, troque a ativação do venv
por `source .venv/bin/activate`.

Por padrão o Streamlit escuta em todas as interfaces de rede — em rede corporativa
ou Wi-Fi público, prefira restringir a máquina local:

```bash
streamlit run app.py --server.address localhost
```

(Esse parâmetro vale só para execução local; o Streamlit Cloud gerencia o bind por
conta própria, por isso ele não está fixado em `.streamlit/config.toml`.)

---

## Estrutura de pastas

```
portfolio/
├── app.py                     # Home: apresentação + cards de destaque
├── pages/
│   ├── 1_Sobre.py             # bio, diferenciais, skills, stack
│   ├── 2_Projetos.py          # projetos em expanders + mini-demo de gráfico
│   └── 3_Contato.py           # links + formulário que monta um e-mail
├── data/                      # TODO o conteúdo editável (fictício)
│   ├── perfil.json            # nome, cargo, bio, links
│   ├── projetos.json          # lista de projetos
│   ├── skills.json            # skills por categoria, ferramentas, idiomas
│   └── sla_exemplo.csv        # dados fictícios usados na mini-demo
├── assets/
│   └── avatar_placeholder.svg # troque pela sua foto
├── utils/
│   ├── __init__.py            # reexporta os helpers
│   ├── data_loader.py         # leitura cacheada e validada de data/
│   └── styles.py              # CSS global, cards, tags, barras de nível
├── .streamlit/
│   └── config.toml            # tema (paleta neutra profissional)
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Como trocar o conteúdo de exemplo pelo real

O código não precisa ser tocado — **tudo vive em `data/`**:

| Quero mudar | Edite |
|---|---|
| Nome, cargo, resumo, bio, links | `data/perfil.json` |
| Projetos (problema → solução → tecnologias → resultado) | `data/projetos.json` |
| Skills, ferramentas, idiomas | `data/skills.json` |
| Dados da mini-demo | `data/sla_exemplo.csv` |
| Foto/avatar | coloque o arquivo em `assets/` e aponte `avatar` em `perfil.json` |
| Cores do tema | `.streamlit/config.toml` **e** `PALETA` em `utils/styles.py` |

Campos de cada projeto em `projetos.json`:

- `titulo`, `resumo` — nome e uma linha de descrição
- `categoria`, `periodo`, `icone` — metadados exibidos no card
- `destaque` — `true` faz o card aparecer na Home
- `problema`, `solucao`, `aprendizado` — texto corrido
- `tecnologias` — lista de strings (vira tag na tela)
- `resultado` — lista de bullets com o impacto
- `repositorio`, `demo` — URLs; deixe `""` para esconder o botão

As chaves que começam com `_` (como `_comentario`) são anotações para você e são
filtradas antes de chegar na tela.

> Depois de editar um arquivo de `data/`, use **Clear cache** no menu do canto
> superior direito do app (ou reinicie), porque a leitura é cacheada.

---

## Deploy no Streamlit Community Cloud

1. Suba o projeto para o GitHub — repositório deste portfólio:
   [`icarocharleaux-mm/portifolio`](https://github.com/icarocharleaux-mm/portifolio).
   O repositório precisa ser **público** para o plano gratuito.
2. Acesse [share.streamlit.io](https://share.streamlit.io) e entre com a conta do GitHub.
3. Clique em **New app** e preencha:
   - **Repository:** `icarocharleaux-mm/portifolio`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Clique em **Deploy**. O build instala o `requirements.txt` automaticamente.
5. Se algum dia o app precisar de credenciais, use **Settings → Secrets** no painel
   do Streamlit Cloud. Elas ficam disponíveis via `st.secrets` e **nunca** devem ir
   para o repositório.

Cada `git push` na branch configurada redeploya o app sozinho.

---

## Checklist antes de publicar

Este repositório é público. Antes de cada push:

- [ ] Nenhum nome real de empresa, filial, cliente, transportadora ou fornecedor
- [ ] Nenhum dado pessoal: CPF, RG, CNH, endereço residencial, telefone, e-mail
      pessoal de terceiros, dados bancários
- [ ] Números de projetos internos apresentados como variação percentual, não como
      base bruta
- [ ] Nenhuma credencial, token, string de conexão ou URL interna no código
- [ ] `.env` e `.streamlit/secrets.toml` fora do Git (já cobertos pelo `.gitignore`)
- [ ] Prints e imagens em `assets/` sem dados de tela real

---

## Licença

Defina a licença antes de publicar (por exemplo, MIT) ou mantenha o repositório
sem licença explícita, o que reserva todos os direitos a você.
