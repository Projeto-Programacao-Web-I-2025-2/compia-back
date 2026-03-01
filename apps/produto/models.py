from django.db import models


class Categoria(models.Model):
    nome = models.CharField(
        max_length=100,
        verbose_name="Categoria",
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.nome


class Produto(models.Model):
    class TipoProduto(models.TextChoices):
        LIVRO = "LIVRO", "Livro"
        EBOOK = "EBOOK", "E-book"

    class Languagem(models.TextChoices):
        PORTUGUES = "PT", "Português"
        INGLES = "EN", "Inglês"
        ESPANHOL = "ES", "Espanhol"
        OTHER = "OT", "Outro"

    nome = models.CharField(
        max_length=100,
        verbose_name="Produto",
    )
    descricao = models.TextField(
        verbose_name="Descrição",
        null=False,
        blank=False,
    )
    preco = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Preço",
    )
    autor = models.CharField(
        max_length=100,
        verbose_name="Autor",
    )
    ano_lancamento = models.IntegerField(
        verbose_name="Ano de lançamento",
    )
    imagem = models.ImageField(
        upload_to='produtos/',
        verbose_name="Imagem",
        null=True,
        blank=True,
    )
    categorias = models.ManyToManyField(
        "Categoria",
        related_name="produtos",
        verbose_name="Categorias",
    )
    tipo_produto = models.CharField(
        max_length=20,
        choices=TipoProduto.choices,
        verbose_name="Tipo do produto",
    )
    idioma = models.CharField(
        max_length=2,
        choices=Languagem.choices,
        verbose_name="Idioma",
    )
