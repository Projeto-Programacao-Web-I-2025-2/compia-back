from rest_framework.routers import DefaultRouter

from django.urls import include, path

from . import views

router = DefaultRouter()
router.register("", views.VendaViewSet, basename="vendas")

urlpatterns = [
    path("", include(router.urls)),
]
