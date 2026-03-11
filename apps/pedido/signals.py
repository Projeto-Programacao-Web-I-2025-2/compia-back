from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import Pedido


@receiver(post_save, sender=Pedido)
def enviar_email_pedido_confirmado(sender, instance, created, **kwargs):
    if not created and instance.status == 'CONFIRMADO':
        context = {
            "cliente_nome": instance.cliente.user.nome,
            "pedido_id": instance.id,
            "pedido_total": instance.total,
            "pedido_frete": instance.frete,
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
        email.send()
