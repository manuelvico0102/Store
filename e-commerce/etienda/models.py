from django.db import models
import Seed
# Create your models here.

def consultarProductos():
    productos = Seed.consultarProductos()
    return productos

def consultaCategoria(categoria):
    productos = Seed.consultarCategoria(categoria)
    return productos

def buscarProducto(request, texto):
    productos = Seed.buscarProducto(request, texto)
    return productos

def insertarProducto(nombre, precio, descripcion, categoria, imagen):
    Seed.insertarProducto(nombre, precio, descripcion, categoria, imagen)
    return True