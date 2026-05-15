import urllib.request
import json

# Hacker News API — sem autenticação necessária
HN_TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Quantidade máxima de posts para analisar
MAX_POSTS = 50
# Score mínimo para considerar o post
MIN_SCORE = 100


def coletar_hackernews():
    """
    Coleta posts do Hacker News com score acima do mínimo.
    Retorna lista de itens com: titulo, url, resumo, fonte.
    """
    itens = []

    try:
        # Busca lista de IDs dos top stories
        with urllib.request.urlopen(HN_TOP_STORIES_URL) as response:
            top_ids = json.loads(response.read())[:MAX_POSTS]

        for post_id in top_ids:
            try:
                url = HN_ITEM_URL.format(post_id)
                with urllib.request.urlopen(url) as response:
                    post = json.loads(response.read())

                # Ignora posts sem título ou abaixo do score mínimo
                if not post.get("title"):
                    continue
                if post.get("score", 0) < MIN_SCORE:
                    continue
                # Ignora posts sem URL externa (perguntas internas do HN)
                if not post.get("url"):
                    continue

                itens.append({
                    "titulo": post.get("title", "").strip(),
                    "url": post.get("url", "").strip(),
                    "resumo": "",  # HN não tem resumo — pré-filtro usará só o título
                    "fonte": "Hacker News",
                    "score": post.get("score", 0)
                })

            except Exception as e:
                print(f"Erro ao coletar post HN {post_id}: {e}")
                continue

    except Exception as e:
        print(f"Erro ao acessar Hacker News: {e}")

    print(f"Hacker News: {len(itens)} itens coletados")
    return itens