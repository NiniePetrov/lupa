# Lupa — Sistema de Inteligência Editorial Pessoal

[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-MVP-orange)]()

> 🇺🇸 [Read in English](README.md)

---

## O que é o Lupa

Lupa é um pipeline de monitoramento diário que varre feeds RSS e agregadores, filtra itens por relevância editorial e entrega uma newsletter curada na sua caixa de entrada — automaticamente.

O sistema é construído em torno de um posicionamento editorial específico: a interseção entre **Psicologia e comportamento de LLMs**. Ele não apenas coleta conteúdo — classifica, explica por que passou no filtro e mapeia como cada item se conecta nos registros técnico, psicológico e filosófico.

---

## Como Funciona

```
Feeds RSS + Hacker News
        ↓
   Pré-filtro por palavras-chave (sem custo de LLM)
        ↓
   Haiku — Classificação + Resumo
        ↓
   Sonnet — Diagnóstico Editorial (apenas candidatos Substack)
        ↓
   Newsletter diária via Gmail
```

**Módulo 1 — Coleta:** `feedparser` lê 7 feeds RSS. A API do Hacker News (sem autenticação) adiciona posts filtrados por score.

**Módulo 2 — Pré-filtro:** Matching por palavras-chave em Python puro contra uma taxonomia curada de ~60 termos em 5 categorias. Sem chamadas de API. Itens que não correspondem são descartados a custo zero.

**Módulo 3 — Classificação (Haiku):** Itens aprovados são classificados em SUBSTACK, NEWS ou TECNICO e recebem um resumo executivo.

**Módulo 4 — Enriquecimento editorial (Sonnet):** Apenas itens SUBSTACK recebem diagnóstico editorial completo e mapeamento de registros (técnico / psicológico / filosófico).

**Módulo 5 — Email:** Newsletter em HTML entregue diariamente via Gmail SMTP.

---

## Fontes Monitoradas

| Fonte | Tipo |
|---|---|
| arXiv cs.AI | RSS |
| Hugging Face Blog | RSS |
| Hacker News (100+ pontos) | API |
| SPSP Character & Context | RSS |
| APA Journals | RSS |
| Ars Technica | RSS |
| MIT Technology Review | RSS |
| Reddit (7 subreddits) | API — aguardando credenciais |

---

## Estrutura do Output

Cada email diário contém até 15 itens em três seções:

- **Candidatos Substack** — diagnóstico editorial completo + mapeamento de registros
- **News & Mercado** — resumo + fonte
- **Atualizações técnicas** — resumo + fonte

---

## Stack Tecnológica

- **Python 3.13**
- **feedparser** — leitura de RSS
- **Anthropic Claude API** — Haiku para classificação, Sonnet para enriquecimento editorial
- **schedule** — agendamento de execução diária
- **smtplib** — entrega via Gmail SMTP

---

## Rodando Localmente

**Pré-requisitos**
- Python 3.13+
- Chave de API da Anthropic
- Conta Gmail com Senha de App habilitada

**Configuração**

```bash
git clone https://github.com/NiniePetrov/lupa.git
cd lupa

python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

pip install -r requirements.txt

cp .env.example .env
# Preencha suas credenciais no .env

python main.py
```

---

## Custo Diário Estimado

| Modelo | Função | Custo estimado/dia |
|---|---|---|
| Claude Haiku | Classificação + resumo | ~$0,06 |
| Claude Sonnet | Enriquecimento editorial (só Substack) | ~$0,04 |
| **Total** | | **~$0,10/dia** |

---

## Roadmap

- [ ] Integração com Reddit (aguardando aprovação da API)
- [ ] Auditoria semanal por LLM dos itens descartados
- [ ] Taxonomia de palavras-chave em PT-BR
- [ ] Deploy em servidor cloud para agendamento 24/7

---

## Autor

**Weberson Azemclever**
Prompt Engineer | Análise de Comportamento de LLMs | Vieses Cognitivos Aplicados em IA

[![LinkedIn](https://img.shields.io/badge/LinkedIn-blue)](https://linkedin.com/in/weberson-azemclever)
[![Substack](https://img.shields.io/badge/Substack-orange)](https://substack.com/@stranight)