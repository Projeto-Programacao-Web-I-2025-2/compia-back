import logging

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore

from .models import Pedido
from datetime import date

logger = logging.getLogger(__name__)

AVANCAR_STATUS = {
    'CONFIRMADO': 'ENVIADO',
    'ENVIADO': 'ENTREGUE',
}


def _apenas_ebooks(pedido):
    for item in pedido.itens.all():
        try:
            item.produto.ebook
        except Exception:
            return False
    return True


def avancar_status_pedidos():
    pedidos = Pedido.objects.filter(status__in=AVANCAR_STATUS.keys())

    for pedido in pedidos:
        if pedido.status == 'CONFIRMADO' and _apenas_ebooks(pedido):
            pedido.status = 'ENTREGUE'
            pedido.data_entrega = date.today()
        else:
            pedido.status = AVANCAR_STATUS[pedido.status]
            if pedido.status == 'ENTREGUE':
                pedido.data_entrega = date.today()

        pedido.save()
        logger.info(f"Pedido #{pedido.id} atualizado para {pedido.status}")


def iniciar_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'default')

    scheduler.add_job(
        avancar_status_pedidos,
        trigger='interval',
        minutes=5,
        id='avancar_status_pedidos',
        replace_existing=True,
    )

    scheduler.start()
    logger.info("Scheduler iniciado.")
