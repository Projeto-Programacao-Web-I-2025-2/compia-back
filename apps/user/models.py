from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        CLIENTE = "CLIENTE", "Cliente"
        VENDEDOR = "VENDEDOR", "Vendedor"
        BACKOFFICE = "BACKOFFICE", "Backoffice"

    nome = models.CharField(
        max_length=100,
        verbose_name="Nome",
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Email",
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        verbose_name="Função",
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name="Membro da equipe",
    )
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nome"]

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    @property
    def is_client(self):
        return self.role == self.Role.CLIENTE

    @property
    def is_seller(self):
        return self.role == self.Role.VENDEDOR

    @property
    def is_backoffice(self):
        return self.role == self.Role.BACKOFFICE
