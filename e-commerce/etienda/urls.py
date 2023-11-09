from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("buscar-categoria/<str:categoria>/", views.categorias, name="buscar-categoria"),
    path("buscar/", views.buscar, name="buscar-nombre"),
    path("nuevo-producto/", views.nuevoProducto, name="nuevo-producto"),
]