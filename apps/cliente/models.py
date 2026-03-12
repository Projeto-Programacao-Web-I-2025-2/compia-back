from django.db import models


class Endereco(models.Model):
    rua = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.rua}, {self.numero} - {self.cidade}/{self.estado}"


class Cliente(models.Model):
    user = models.OneToOneField(
        "user.User",
        on_delete=models.CASCADE,
        related_name="cliente",
        verbose_name="Cliente",
    )
    endereco = models.OneToOneField(
        Endereco,
        on_delete=models.SET_NULL,
        related_name="cliente",
        verbose_name="Endereço",
        null=True,
    )

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return f"{self.user.nome} - {self.user.email}"
