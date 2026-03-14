import os
import requests as http_requests
import threading

from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import Pedido


def _enviar_email(instance):
    context = {
        "cliente_nome": instance.cliente.user.nome,
        "pedido_id": instance.id,
        "pedido_total": instance.total,
    }
    html_content = render_to_string("mail/pedido-confirmado.html", context)
    text_content = "Seu pedido foi confirmado com sucesso."

    email = EmailMultiAlternatives(
        subject="Pedido confirmado!",
        body=text_content,
        from_email="no-reply@compia.com",
        to=[instance.cliente.user.email],
    )
    email.attach_alternative(html_content, "text/html")

    for item in instance.itens.all():
        produto = item.produto
        if hasattr(produto, "ebook") and produto.ebook.arquivo:
            arquivo_ebook = produto.ebook.arquivo
            try:
                url = arquivo_ebook.url
                response = http_requests.get(url)
                response.raise_for_status()
                content_type = response.headers.get("Content-Type", "application/octet-stream")
                nome_arquivo = os.path.basename(arquivo_ebook.name)
                email.attach(nome_arquivo, response.content, content_type)
            except Exception as e:
                print(f"Erro ao anexar ebook: {e}")

    email.send()


@receiver(post_save, sender=Pedido)
def enviar_email_pedido_confirmado(sender, instance, created, **kwargs):
    if instance.status == 'CONFIRMADO':
        thread = threading.Thread(target=_enviar_email, args=(instance,))
        thread.daemon = True
        thread.start()