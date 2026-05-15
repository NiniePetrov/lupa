import anthropic
from config import ANTHROPIC_API_KEY

cliente = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """Você é um classificador editorial especializado na interseção entre Psicologia e comportamento de LLMs.

Dado um item coletado de feeds RSS ou agregadores, você deve:
1. Classificar em UMA das três categorias: SUBSTACK, NEWS ou TECNICO
2. Gerar um resumo executivo em 5 a 8 linhas em prosa fluida

Definições das categorias:
- SUBSTACK: tem potencial de virar artigo longo — envolve viés cognitivo, comportamento de modelos, fenomenologia digital, pressão filosófica ou sistêmica
- NEWS: movimento de mercado, lançamento relevante, decisão de política com impacto real em produtos
- TECNICO: paper novo, release de framework, atualização de biblioteca, benchmark com metodologia interessante

Responda SOMENTE em JSON válido, sem markdown, neste formato exato:
{
  "categoria": "SUBSTACK" | "NEWS" | "TECNICO",
  "resumo": "texto em prosa fluida de 5 a 8 linhas"
}"""


def classificar_item(item):
    """
    Recebe um item aprovado pelo pré-filtro.
    Retorna o item enriquecido com categoria e resumo.
    """
    try:
        conteudo = f"""Título: {item['titulo']}
Fonte: {item['fonte']}
URL: {item['url']}
Resumo original: {item.get('resumo', 'não disponível')}"""

        resposta = cliente.messages.create(
            model="claude-haiku-4-5",
            max_tokens=400,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": conteudo}
            ]
        )

        texto = resposta.content[0].text.strip()

        # Remove possíveis marcadores de markdown se o modelo incluir
        texto = texto.replace("```json", "").replace("```", "").strip()

        import json
        resultado = json.loads(texto)

        item["categoria"] = resultado.get("categoria", "NEWS")
        item["resumo_gerado"] = resultado.get("resumo", "")

        return item

    except Exception as e:
        print(f"Erro ao classificar item '{item.get('titulo', '')}': {e}")
        item["categoria"] = "NEWS"
        item["resumo_gerado"] = ""
        return item


def classificar_itens(itens):
    """
    Classifica todos os itens aprovados pelo pré-filtro.
    Retorna lista com categoria e resumo preenchidos.
    """
    resultado = []

    for item in itens:
        classificado = classificar_item(item)
        resultado.append(classificado)

    # Contagem por categoria
    substack = sum(1 for i in resultado if i["categoria"] == "SUBSTACK")
    news = sum(1 for i in resultado if i["categoria"] == "NEWS")
    tecnico = sum(1 for i in resultado if i["categoria"] == "TECNICO")

    print(f"Classificação: {substack} SUBSTACK | {news} NEWS | {tecnico} TECNICO")

    return resultado