from django.apps import AppConfig


class PedidoConfig(AppConfig):
    name = "apps.pedido"
    verbose_name = "Pedidos"

    def ready(self):
        import apps.pedido.signals  # noqa: F401
