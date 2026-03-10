from django.db import models


class ItemVenda(models.Model):
    venda = models.ForeignKey(
        "venda.Venda",
        on_delete=models.CASCADE,
        related_name="itens"
    )
    produto = models.ForeignKey(
        "produto.Produto",
        on_delete=models.CASCADE
    )
    quantidade = models.PositiveIntegerField()


class Venda(models.Model):
    produtos = models.ManyToManyField(
        "produto.Produto",
        through=ItemVenda,
        related_name="vendas",
    )
    cliente = models.ForeignKey(
        "cliente.Cliente",
        on_delete=models.CASCADE,
    )
    vendedor = models.ForeignKey(
        "vendedor.Vendedor",
        on_delete=models.CASCADE,
        related_name="vendas",
    )
    data_venda = models.DateTimeField(auto_now_add=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
