# MÓDULO REDDIT — aguardando aprovação de credenciais
# Para ativar: descomentar todo o código e instalar praw com:
# pip install praw

# import praw
# from config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT

# SUBREDDITS = [
#     "MachineLearning",
#     "artificial",
#     "ChatGPT",
#     "singularity",
#     "psychology",
#     "cognitivescience",
#     "Anthropic",
# ]

# MIN_SCORE = 100
# MAX_POSTS_POR_SUB = 25


# def coletar_reddit():
#     """
#     Coleta posts dos subreddits monitorados com score acima do mínimo.
#     Retorna lista de itens com: titulo, url, resumo, fonte.
#     """
#     reddit = praw.Reddit(
#         client_id=REDDIT_CLIENT_ID,
#         client_secret=REDDIT_CLIENT_SECRET,
#         user_agent=REDDIT_USER_AGENT,
#     )
#
#     itens = []
#
#     for sub in SUBREDDITS:
#         try:
#             subreddit = reddit.subreddit(sub)
#             for post in subreddit.hot(limit=MAX_POSTS_POR_SUB):
#                 if post.score < MIN_SCORE:
#                     continue
#                 if not post.url:
#                     continue
#
#                 itens.append({
#                     "titulo": post.title.strip(),
#                     "url": post.url.strip(),
#                     "resumo": post.selftext[:500].strip() if post.selftext else "",
#                     "fonte": f"r/{sub}",
#                     "score": post.score
#                 })
#
#         except Exception as e:
#             print(f"Erro ao coletar r/{sub}: {e}")
#             continue
#
#     print(f"Reddit: {len(itens)} itens coletados")
#     return itens


def coletar_reddit():
    """Placeholder — Reddit pendente de credenciais."""
    print("Reddit: módulo pendente de credenciais — pulando")
    return []