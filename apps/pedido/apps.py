from django.apps import AppConfig


class PedidoConfig(AppConfig):
    name = "apps.pedido"
    verbose_name = "Pedidos"

    def ready(self):
        import apps.pedido.signals  # noqa: F401
        from .scheduler import iniciar_scheduler
        iniciar_scheduler()
