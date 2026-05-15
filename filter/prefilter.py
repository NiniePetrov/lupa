from keywords.terms import C_TIER, MULTI_TOKEN


def normalizar(texto):
    """
    Converte texto para minúsculas para comparação case-insensitive.
    """
    return texto.lower()


def passou_filtro(item):
    """
    Verifica se um item passa no pré-filtro.
    Retorna True se aprovado, False se descartado.

    Lógica:
    1. Se qualquer termo C-tier aparecer no título ou resumo — aprovado
    2. Se qualquer par MULTI_TOKEN tiver os dois termos presentes — aprovado
    3. Caso contrário — descartado
    """
    # Junta título e resumo para verificação
    texto = normalizar(item.get("titulo", "") + " " + item.get("resumo", ""))

    # Verifica termos C-tier
    for termo in C_TIER:
        if termo.lower() in texto:
            return True

    # Verifica combinações multi-token
    for termo_a, termo_b in MULTI_TOKEN:
        if termo_a.lower() in texto and termo_b.lower() in texto:
            return True

    return False


def aplicar_prefiltro(itens):
    """
    Recebe lista de itens coletados e retorna apenas os aprovados.
    """
    aprovados = []

    for item in itens:
        if passou_filtro(item):
            aprovados.append(item)

    total = len(itens)
    aprovados_count = len(aprovados)
    descartados = total - aprovados_count

    print(f"Pré-filtro: {total} itens recebidos → {aprovados_count} aprovados, {descartados} descartados")

    return aprovados