from rest_framework.routers import DefaultRouter

from django.urls import include, path

from . import views

router = DefaultRouter()
router.register("", views.ProdutoViewSet, basename="produto")

urlpatterns = [
    path("", include(router.urls)),
]
