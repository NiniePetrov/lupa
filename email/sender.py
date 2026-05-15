import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import GMAIL_APP_PASSWORD, GMAIL_SENDER, GMAIL_RECIPIENT
from datetime import date


def selecionar_itens(itens):
    """
    Seleciona até 5 itens por categoria.
    Retorna dicionário com três listas separadas.
    """
    substack = [i for i in itens if i.get("categoria") == "SUBSTACK"][:5]
    news = [i for i in itens if i.get("categoria") == "NEWS"][:5]
    tecnico = [i for i in itens if i.get("categoria") == "TECNICO"][:5]
    return {"substack": substack, "news": news, "tecnico": tecnico}


def montar_secao_substack(itens):
    if not itens:
        return ""
    html = "<h2 style='color:#1a1a2e;border-bottom:2px solid #4a9eed;padding-bottom:8px'>📝 Candidatos Substack</h2>"
    for item in itens:
        conexao = item.get("conexao_registros", {})
        html += f"""
        <div style='margin-bottom:32px;padding:20px;background:#f8f9fa;border-left:4px solid #4a9eed;border-radius:4px'>
            <h3 style='margin:0 0 8px 0'><a href='{item['url']}' style='color:#1a1a2e;text-decoration:none'>{item['titulo']}</a></h3>
            <p style='color:#666;font-size:13px;margin:0 0 12px 0'>📡 {item['fonte']}</p>
            <p style='margin:0 0 12px 0'>{item.get('resumo_gerado', '')}</p>
            <div style='background:#fff;padding:12px;border-radius:4px;margin-top:8px'>
                <p style='margin:0 0 6px 0;font-weight:bold;color:#4a9eed'>Diagnóstico editorial</p>
                <p style='margin:0 0 12px 0;font-size:14px'>{item.get('diagnostico', '')}</p>
                <p style='margin:0 0 6px 0;font-weight:bold;color:#4a9eed'>Conexão de registros</p>
                <p style='margin:0 0 4px 0;font-size:13px'><strong>Técnico:</strong> {conexao.get('tecnico', '')}</p>
                <p style='margin:0 0 4px 0;font-size:13px'><strong>Psicológico:</strong> {conexao.get('psicologico', '')}</p>
                <p style='margin:0 0 0 0;font-size:13px'><strong>Filosófico:</strong> {conexao.get('filosofico', '')}</p>
            </div>
        </div>"""
    return html


def montar_secao_simples(itens, titulo, cor):
    if not itens:
        return ""
    html = f"<h2 style='color:#1a1a2e;border-bottom:2px solid {cor};padding-bottom:8px'>{titulo}</h2>"
    for item in itens:
        html += f"""
        <div style='margin-bottom:20px;padding:16px;background:#f8f9fa;border-left:4px solid {cor};border-radius:4px'>
            <h3 style='margin:0 0 8px 0'><a href='{item['url']}' style='color:#1a1a2e;text-decoration:none'>{item['titulo']}</a></h3>
            <p style='color:#666;font-size:13px;margin:0 0 10px 0'>📡 {item['fonte']}</p>
            <p style='margin:0'>{item.get('resumo_gerado', '')}</p>
        </div>"""
    return html


def montar_html(selecionados):
    hoje = date.today().strftime("%d/%m/%Y")
    total = sum(len(v) for v in selecionados.values())

    html_substack = montar_secao_substack(selecionados["substack"])
    html_news = montar_secao_simples(selecionados["news"], "📰 News & Mercado", "#22c55e")
    html_tecnico = montar_secao_simples(selecionados["tecnico"], "⚙️ Atualização Técnica", "#f59e0b")

    return f"""
    <html>
    <body style='font-family:Georgia,serif;max-width:700px;margin:0 auto;padding:20px;color:#1a1a2e'>
        <div style='background:#1a1a2e;padding:24px;border-radius:8px;margin-bottom:32px'>
            <h1 style='color:#e5e5e5;margin:0;font-size:28px'>🔍 Lupa</h1>
            <p style='color:#a0a0a0;margin:8px 0 0 0'>{hoje} · {total} itens selecionados</p>
        </div>
        {html_substack}
        {html_news}
        {html_tecnico}
        <div style='margin-top:40px;padding:16px;background:#f8f9fa;border-radius:4px;text-align:center'>
            <p style='color:#666;font-size:12px;margin:0'>Lupa · Sistema de inteligência editorial pessoal</p>
        </div>
    </body>
    </html>"""


def enviar_email(itens):
    """
    Recebe lista completa de itens classificados.
    Seleciona, monta o HTML e envia o email.
    """
    selecionados = selecionar_itens(itens)
    total = sum(len(v) for v in selecionados.values())

    if total == 0:
        print("Email: nenhum item para enviar hoje")
        return

    html = montar_html(selecionados)
    hoje = date.today().strftime("%d/%m/%Y")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🔍 Lupa — {hoje}"
    msg["From"] = GMAIL_SENDER
    msg["To"] = GMAIL_RECIPIENT
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_SENDER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_SENDER, GMAIL_RECIPIENT, msg.as_string())
        print(f"Email enviado com sucesso — {total} itens")
    except Exception as e:
        print(f"Erro ao enviar email: {e}")