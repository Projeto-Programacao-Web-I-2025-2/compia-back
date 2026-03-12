from django.urls import path
from .views import MelhorEnvioFreteView

urlpatterns = [
    path("melhorenvio/frete/", MelhorEnvioFreteView.as_view(), name="melhorenvio-frete"),
]
