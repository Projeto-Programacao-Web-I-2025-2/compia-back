from django.db import models


class Pedido(models.Model):
    class StatusPedido(models.TextChoices):
        ABERTO = "ABERTO", "Aberto"
        CONFIRMADO = "CONFIRMADO", "Confirmado"
        ENVIADO = "ENVIADO", "Enviado"
        ENTREGUE = "ENTREGUE", "Entregue"
        CANCELADO = "CANCELADO", "Cancelado"

    cliente = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        related_name="pedidos",
        verbose_name="Cliente",
    )
    produtos = models.ManyToManyField(
        "produto.Produto",
        related_name="pedidos",
        verbose_name="Produtos",
    )
    data_pedido = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data do Pedido",
        null=True,
        blank=True,
    )
    frete = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Valor do Frete",
        blank=True,
        null=True,
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Valor Total",
        blank=True,
        default=0.00
    )
    status = models.CharField(
        max_length=20,
        choices=StatusPedido.choices,
        default=StatusPedido.ABERTO,
        verbose_name="Status do Pedido"
    )
