from django.db import models


class ItemPedido(models.Model):
    produto = models.ForeignKey(
        "produto.Produto",
        on_delete=models.CASCADE,
        related_name="itens_pedido",
        verbose_name="Produto",
    )
    quantidade = models.PositiveIntegerField(verbose_name="Quantidade")
    pedido = models.ForeignKey(
        "pedido.Pedido",
        on_delete=models.CASCADE,
        related_name="itens",
        verbose_name="Pedido",
    )

    class Meta:
        unique_together = ("pedido", "produto")

    def __str__(self):
        return f"{self.quantidade}x {self.produto} (Pedido {self.pedido_id})"


class Pedido(models.Model):
    class StatusPedido(models.TextChoices):
        ABERTO = "ABERTO", "Aberto"
        CONFIRMADO = "CONFIRMADO", "Confirmado"
        ENVIADO = "ENVIADO", "Enviado"
        ENTREGUE = "ENTREGUE", "Entregue"
        CANCELADO = "CANCELADO", "Cancelado"

    cliente = models.ForeignKey(
        "cliente.Cliente",
        on_delete=models.CASCADE,
        related_name="pedidos",
        verbose_name="Cliente",
    )
    produtos = models.ManyToManyField(
        "produto.Produto",
        through=ItemPedido,
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
    data_entrega = models.DateTimeField(
        verbose_name="Data de Entrega",
        null=True,
        blank=True,
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

    def __str__(self):
        return f"Pedido #{self.pk} - {self.get_status_display()}"
