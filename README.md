# Lupa — Personal Editorial Intelligence System

[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-MVP-orange)]()

> 🇧🇷 [Leia em Português](README.pt-br.md)

---

## What is Lupa

Lupa is a daily content monitoring pipeline that scans RSS feeds and aggregators, filters items by editorial relevance, and delivers a curated newsletter to your inbox — automatically.

The system is built around a specific editorial positioning: the intersection of **Psychology and LLM behavior**. It doesn't just collect content — it classifies it, explains why it passed the filter, and maps how each item connects across technical, psychological, and philosophical registers.

---

## How It Works

```
RSS Feeds + Hacker News
        ↓
   Keyword Pre-filter (no LLM cost)
        ↓
   Haiku — Classification + Summary
        ↓
   Sonnet — Editorial Diagnosis (Substack candidates only)
        ↓
   Daily Newsletter via Gmail
```

**Module 1 — Collection:** `feedparser` reads 7 RSS feeds. Hacker News API (no auth required) adds top posts filtered by score.

**Module 2 — Pre-filter:** Pure Python keyword matching against a curated taxonomy of ~60 terms across 5 categories. No API calls. Items that don't match are discarded at zero cost.

**Module 3 — Classification (Haiku):** Approved items are classified into SUBSTACK, NEWS, or TECNICO, and receive an executive summary.

**Module 4 — Editorial enrichment (Sonnet):** Only SUBSTACK items receive a full editorial diagnosis and register mapping (technical / psychological / philosophical).

**Module 5 — Email:** HTML newsletter delivered daily via Gmail SMTP.

---

## Sources Monitored

| Source | Type |
|---|---|
| arXiv cs.AI | RSS |
| Hugging Face Blog | RSS |
| Hacker News (100+ points) | API |
| SPSP Character & Context | RSS |
| APA Journals | RSS |
| Ars Technica | RSS |
| MIT Technology Review | RSS |
| Reddit (7 subreddits) | API — pending credentials |

---

## Output Structure

Each daily email contains up to 15 items across three sections:

- **Substack candidates** — full editorial diagnosis + register mapping
- **News & Market** — summary + source
- **Technical updates** — summary + source

---

## Tech Stack

- **Python 3.13**
- **feedparser** — RSS parsing
- **Anthropic Claude API** — Haiku for classification, Sonnet for editorial enrichment
- **GitHub Actions** — daily scheduling, no server required
- **smtplib** — Gmail SMTP delivery

---

## Running Locally

**Prerequisites**
- Python 3.13+
- Anthropic API key
- Gmail account with App Password enabled

**Setup**

```bash
git clone https://github.com/NiniePetrov/lupa.git
cd lupa

python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

pip install -r requirements.txt

cp .env.example .env
# Fill in your credentials in .env

python main.py  # executes once and exits
```

---

## Deploy

This project runs automatically via **GitHub Actions** — no server required.

- Scheduled daily at 08:00 BRT (UTC-3)
- Credentials stored as GitHub repository secrets
- Trigger manually anytime via the Actions tab on GitHub

---

## Estimated Daily Cost

| Model | Role | Est. cost/day |
|---|---|---|
| Claude Haiku | Classification + summary | ~$0.06 |
| Claude Sonnet | Editorial enrichment (Substack only) | ~$0.04 |
| **Total** | | **~$0.10/day** |

---

## Roadmap

- [ ] Reddit integration (pending API approval)
- [ ] Weekly LLM audit of discarded items
- [ ] PT-BR keyword taxonomy
- [ ] Deploy to cloud server for 24/7 scheduling

---

## Author

**Weberson Azemclever**
Prompt Engineer | LLM Behavior Analysis | Applied Cognitive Biases in AI

[![LinkedIn](https://img.shields.io/badge/LinkedIn-blue)](https://linkedin.com/in/weberson-azemclever)
[![Substack](https://img.shields.io/badge/Substack-orange)](https://substack.com/@stranight)