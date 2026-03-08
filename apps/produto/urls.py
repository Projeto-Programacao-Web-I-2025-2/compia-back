from rest_framework.routers import DefaultRouter

from django.urls import include, path

from . import views

router = DefaultRouter()
router.register("livros", views.LivroViewSet, basename="livro")
router.register("ebooks", views.EbookViewSet, basename="ebook")
router.register("", views.ProdutoViewSet, basename="produto")

urlpatterns = [
    path("", include(router.urls)),
]
