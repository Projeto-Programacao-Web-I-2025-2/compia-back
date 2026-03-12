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
    class Linguagem(models.TextChoices):
        PORTUGUES = "PT", "Português"
        INGLES = "EN", "Inglês"
        ESPANHOL = "ES", "Espanhol"
        OTHER = "OT", "Outro"

    nome = models.CharField(
        max_length=100,
        verbose_name="Título",
    )
    vendedor = models.ForeignKey(
        "vendedor.Vendedor",
        on_delete=models.CASCADE,
        related_name="produtos",
        verbose_name="Vendedor",
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
        blank=True,
    )
    idioma = models.CharField(
        max_length=2,
        choices=Linguagem.choices,
        verbose_name="Idioma",
    )


class Livro(Produto):
    estoque = models.IntegerField(
        verbose_name="Estoque",
    )

    class Meta:
        verbose_name = "Livro"
        verbose_name_plural = "Livros"


class Ebook(Produto):
    arquivo = models.FileField(
        upload_to='ebooks/',
        verbose_name="Arquivo",
    )

    class Meta:
        verbose_name = "E-book"
        verbose_name_plural = "E-books"
