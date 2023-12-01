from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from . import models
from .forms import ProductoForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)


def index(request):
    logger.info('Se ha accedidio a la página principal')
    return render(request, 'etienda/index.html')

def categorias(request, categoria):
    if categoria == "Todos los productos":
        productos = models.consultarProductos()
        messages.success(request, "Se ha accedido a 'Todos los producto'")
    else:
        productos = models.consultaCategoria(categoria)
        messages.success(request, "Se ha accedido a la categoría " + categoria) 
    logger.info('Se ha accedido a la página de %s', categoria)
    return render(request, 'etienda/inicio.html', {'productos': productos, 'categoria':categoria})

def buscar(request):
    productos = models.buscarProducto(request, request.GET['buscar'])
    logger.info('Se ha buscado %s', request.GET['buscar'])
    return render(request, 'etienda/inicio.html', {'productos': productos})

@login_required
def nuevoProducto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            precio = form.cleaned_data['precio']
            descripcion = form.cleaned_data['descripcion']
            categoria = form.cleaned_data['categoria']
            imagen = form.cleaned_data['imagen'] 
            insertado = models.insertarProducto(nombre, precio, descripcion, categoria, imagen)
            if insertado:
                logger.info('El usuario %s ha añadido el producto %s',request.user, nombre)
                messages.success(request, 'Producto añadido correctamente')
            else:
                logger.error('Fallo al insertar el productor en la base de datos')
                messages.warning('Ha habido un error al añadir el productor')
            return index(request)
    else:
        logger.info('Se ha accedido a la página de nuevo producto')
        form = ProductoForm()
    
    return render(request, 'etienda/form_producto.html', {'form': form})

