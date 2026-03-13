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
            content_type = (
                arquivo_ebook.file.content_type
                if hasattr(arquivo_ebook.file, "content_type")
                else "application/octet-stream"
            )
            email.attach(
                arquivo_ebook.name,
                arquivo_ebook.read(),
                content_type
            )

    email.send()


@receiver(post_save, sender=Pedido)
def enviar_email_pedido_confirmado(sender, instance, created, **kwargs):
    if instance.status == 'CONFIRMADO':
        thread = threading.Thread(target=_enviar_email, args=(instance,))
        thread.daemon = True
        thread.start()
