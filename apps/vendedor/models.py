from django.db import models


class Vendedor(models.Model):
    user = models.OneToOneField(
        "user.User",
        on_delete=models.CASCADE,
        related_name="vendedor",
        verbose_name="Vendedor",
    )
    endereco = models.OneToOneField(
        "cliente.Endereco",
        on_delete=models.SET_NULL,
        related_name="vendedor",
        verbose_name="Endereço",
        null=True,
    )

    class Meta:
        verbose_name = "Vendedor"
        verbose_name_plural = "Vendedores"

    def __str__(self):
        return f"Vendedor - {self.user.nome}"
