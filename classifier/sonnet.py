import anthropic
import json
from config import ANTHROPIC_API_KEY

cliente = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """Você é um analista editorial especializado na interseção entre Psicologia e comportamento de LLMs.

Seu canal (Stranight) opera em três registros simultâneos:
- Técnico: comportamento observável de modelos, arquitetura, falhas documentadas
- Psicológico: vieses cognitivos, teoria da mente, fenomenologia, cognição
- Filosófico: pressão sistêmica, epistemologia, identidade, linguagem

Dado um item classificado como SUBSTACK, você deve produzir:
1. Diagnóstico de seleção: por que esse item é editorialmente relevante para o canal
2. Conexão de registros: como os três registros (técnico, psicológico, filosófico) se conectam nesse tema

Responda SOMENTE em JSON válido, sem markdown, neste formato exato:
{
  "diagnostico": "texto explicando por que o filtro foi ativado e qual o potencial editorial",
  "conexao_registros": {
    "tecnico": "como o registro técnico se manifesta nesse tema",
    "psicologico": "como o registro psicológico se manifesta nesse tema",
    "filosofico": "como o registro filosófico se manifesta nesse tema"
  }
}"""


def enriquecer_item(item):
    """
    Recebe item classificado como SUBSTACK pelo Haiku.
    Adiciona diagnóstico editorial e conexão de registros via Sonnet.
    """
    try:
        conteudo = f"""Título: {item['titulo']}
Fonte: {item['fonte']}
URL: {item['url']}
Resumo gerado: {item.get('resumo_gerado', '')}"""

        resposta = cliente.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=600,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": conteudo}
            ]
        )

        texto = resposta.content[0].text.strip()
        texto = texto.replace("```json", "").replace("```", "").strip()

        resultado = json.loads(texto)

        item["diagnostico"] = resultado.get("diagnostico", "")
        item["conexao_registros"] = resultado.get("conexao_registros", {})

        return item

    except Exception as e:
        print(f"Erro ao enriquecer item '{item.get('titulo', '')}': {e}")
        item["diagnostico"] = ""
        item["conexao_registros"] = {}
        return item


def enriquecer_substack(itens):
    """
    Filtra apenas itens SUBSTACK e enriquece com diagnóstico editorial.
    Retorna a lista completa com itens SUBSTACK enriquecidos.
    """
    resultado = []

    for item in itens:
        if item.get("categoria") == "SUBSTACK":
            enriquecido = enriquecer_item(item)
            resultado.append(enriquecido)
        else:
            resultado.append(item)

    substack_count = sum(1 for i in resultado if i.get("categoria") == "SUBSTACK")
    print(f"Sonnet: {substack_count} itens SUBSTACK enriquecidos")

    return resultado