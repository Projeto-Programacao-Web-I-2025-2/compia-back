import os
import threading
import resend

from django.conf import settings
from django.template.loader import render_to_string
import requests as http_requests

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Pedido

resend.api_key = settings.RESEND_API_KEY


def _enviar_email(instance):
    context = {
        "cliente_nome": instance.cliente.user.nome,
        "pedido_id": instance.id,
        "pedido_total": instance.total,
    }
    html_content = render_to_string("mail/pedido-confirmado.html", context)

    attachments = []
    for item in instance.itens.all():
        produto = item.produto
        if hasattr(produto, "ebook") and produto.ebook.arquivo:
            arquivo_ebook = produto.ebook.arquivo
            try:
                url = arquivo_ebook.url
                response = http_requests.get(url)
                response.raise_for_status()
                nome_arquivo = os.path.basename(arquivo_ebook.name)
                attachments.append({
                    "filename": nome_arquivo,
                    "content": list(response.content),
                })
            except Exception as e:
                print(f"Erro ao anexar ebook: {e}")

    params = {
        "from": "onboarding@resend.dev",
        "to": [instance.cliente.user.email],
        "subject": "Pedido confirmado!",
        "html": html_content,
    }

    if attachments:
        params["attachments"] = attachments

    resend.Emails.send(params)


@receiver(post_save, sender=Pedido)
def enviar_email_pedido_confirmado(sender, instance, created, **kwargs):
    if instance.status == 'CONFIRMADO':
        thread = threading.Thread(target=_enviar_email, args=(instance,))
        thread.daemon = True
        thread.start()
