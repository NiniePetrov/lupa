import feedparser

# Fontes RSS monitoradas
FEEDS = [
    {
        "name": "arXiv cs.AI",
        "url": "https://rss.arxiv.org/rss/cs.AI"
    },
    {
        "name": "Hugging Face Blog",
        "url": "https://huggingface.co/blog/feed.xml"
    },
    {
        "name": "Hacker News (100+ pontos)",
        "url": "https://hnrss.org/frontpage?points=100"
    },
    {
        "name": "SPSP Character & Context",
        "url": "https://spsp.org/news/character-and-context-blog/feed"
    },
    {
        "name": "APA Journals",
        "url": "https://www.apa.org/pubs/journals/releases/rss"
    },
    {
        "name": "Ars Technica AI",
        "url": "https://feeds.arstechnica.com/arstechnica/technology-lab"
    },
    {
        "name": "MIT Technology Review AI",
        "url": "https://www.technologyreview.com/feed/"
    },
]


def coletar_rss():
    """
    Lê todos os feeds RSS e retorna lista de itens coletados.
    Cada item é um dicionário com: titulo, url, resumo, fonte.
    """
    itens = []

    for feed in FEEDS:
        try:
            parsed = feedparser.parse(feed["url"])

            for entry in parsed.entries:
                titulo = entry.get("title", "").strip()
                url = entry.get("link", "").strip()
                resumo = entry.get("summary", "").strip()

                # Ignora itens sem título ou URL
                if not titulo or not url:
                    continue

                itens.append({
                    "titulo": titulo,
                    "url": url,
                    "resumo": resumo,
                    "fonte": feed["name"]
                })

        except Exception as e:
            print(f"Erro ao coletar {feed['name']}: {e}")
            continue

    print(f"RSS: {len(itens)} itens coletados")
    return itens