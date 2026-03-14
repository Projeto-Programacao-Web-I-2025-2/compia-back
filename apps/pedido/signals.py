import base64
import os
import threading

import sib_api_v3_sdk
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
import requests as http_requests

from .models import Pedido


def _enviar_email(instance):
    context = {
        "cliente_nome": instance.cliente.user.nome,
        "pedido_id": instance.id,
        "pedido_total": instance.total,
    }
    html_content = render_to_string("mail/pedido-confirmado.html", context)

    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = settings.BREVO_API_KEY
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

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
                conteudo_base64 = base64.b64encode(response.content).decode('utf-8')
                attachments.append({
                    "name": nome_arquivo,
                    "content": conteudo_base64,
                })
            except Exception as e:
                print(f"Erro ao anexar ebook: {e}")

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": instance.cliente.user.email, "name": instance.cliente.user.nome}],
        sender={"email": "erikdinizbeserra@gmail.com", "name": "CompIA"},
        subject="Pedido confirmado!",
        html_content=html_content,
        attachment=attachments if attachments else None,
    )

    try:
        api_instance.send_transac_email(send_smtp_email)
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")


@receiver(post_save, sender=Pedido)
def enviar_email_pedido_confirmado(sender, instance, created, **kwargs):
    if instance.status == 'CONFIRMADO':
        thread = threading.Thread(target=_enviar_email, args=(instance,))
        thread.daemon = True
        thread.start()
