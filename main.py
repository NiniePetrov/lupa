import schedule
import time
from collector.rss import coletar_rss
from collector.hackernews import coletar_hackernews
from collector.reddit import coletar_reddit
from filter.prefilter import aplicar_prefiltro
from classifier.haiku import classificar_itens
from classifier.sonnet import enriquecer_substack
from email.sender import enviar_email


def executar():
    """
    Pipeline completo do Lupa.
    Roda uma vez por dia no horário agendado.
    """
    print("\n" + "="*50)
    print("LUPA — iniciando coleta")
    print("="*50)

    # Módulo 1 — Coleta
    itens_rss = coletar_rss()
    itens_hn = coletar_hackernews()
    itens_reddit = coletar_reddit()

    todos = itens_rss + itens_hn + itens_reddit
    print(f"Total coletado: {len(todos)} itens")

    # Módulo 2 — Pré-filtro
    aprovados = aplicar_prefiltro(todos)

    if not aprovados:
        print("Nenhum item aprovado pelo pré-filtro hoje")
        return

    # Módulo 3 — Classificação com Haiku
    classificados = classificar_itens(aprovados)

    # Módulo 4 — Enriquecimento Substack com Sonnet
    enriquecidos = enriquecer_substack(classificados)

    # Módulo 5 — Email
    enviar_email(enriquecidos)

    print("="*50)
    print("LUPA — concluído")
    print("="*50 + "\n")


def main():
    print("Lupa iniciado — aguardando horário agendado (08:00)")
    
    # Agendamento diário às 08:00
    schedule.every().day.at("08:00").do(executar)

    # Para testar imediatamente sem esperar o horário:
    # executar()

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()