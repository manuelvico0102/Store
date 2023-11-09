# Seed.py
from pydantic import BaseModel, FilePath, Field, EmailStr
from pymongo import MongoClient
from datetime import datetime
from typing import Any
import requests
import os
import subprocess
from datetime import datetime
		
# https://requests.readthedocs.io/en/latest/
# Función para obtener los productos de la API, así como las compras
def getProductos(api):
	response = requests.get(api)
	return response.json()

## Función para descargar imágenes
def descargarImagen(url, directorio, nombre):
	respuesta = requests.get(url)
	with open(os.path.join(directorio, nombre), 'wb') as f:
		f.write(respuesta.content)
	return nombre

# guardar una imagen subida al formulario en una carpeta
def guardarImagen(imagen):
	imagenNombre = imagen.name

	# Generar un nombre de archivo único basado en la hora actual
	timestap = datetime.now().strftime("%Y%m%d%H%M%S%f") # AñoMesDíaHoraMinutoSegundoMicrosegundo
	nombre_unido = f"{timestap}_{imagenNombre}"

	with open(os.path.join('./static/images', nombre_unido), 'wb') as f:
		f.write(imagen.file.read())
	return nombre_unido

def copiaSeguridad():
	# copia de seguridad usando mongodump
	timestap = datetime.now().strftime("%Y%m%d%H%M%S")
	backup_file = f"{'tienda'}_copiaSeguridad_{timestap}"
	mongoDatos = [
		"mongodump",
		"--host", "mongo",
		"--port", "27017",
		"--db", "tienda",
		"--out", f"./backups/{backup_file}"
	]

	subprocess.run(mongoDatos, check=True)


				
# Esquema de la BD
# https://docs.pydantic.dev/latest/
# con anotaciones de tipo https://docs.python.org/3/library/typing.html
# https://docs.pydantic.dev/latest/usage/fields/

class Nota(BaseModel):
	puntuación: float = Field(ge=0., lt=5.)
	cuenta: int = Field(ge=1)
				
class Producto(BaseModel):
	_id: Any
	nombre: str
	precio: float
	descripción: str
	categoría: str
	imágen: str | None
	rating: Nota

class listaCompras(BaseModel):
    idProducto: Any
    cantidad: int

class Compra(BaseModel):
	_id: Any
	usuario: EmailStr
	fecha: datetime
	productos: list

# Conexión con la BD				
# https://pymongo.readthedocs.io/en/stable/tutorial.html
client = MongoClient('mongo', 27017)

tienda_db = client.tienda                   # Base de Datos
productos_collection = tienda_db.productos  # Colección  
compras_collection = tienda_db.compras  # Colección

def guardarProductos():
	## Obtenemos los productos y los insertamos en la BD	
	productos = getProductos('https://fakestoreapi.com/products')
	for p in productos:
		dato = {
		'nombre': p['title'], 
		'precio': p['price'], 
		'descripción': p['description'],
		'categoría': p['category'],
		'imágen': p['image'].split("/")[-1], 
		'rating': {'puntuación': p['rating']['rate'], 'cuenta': p['rating']['count']}
		}
		# Nos aseguramos que el nombre empieza en mayuscula
		if not dato['nombre'][0].islower():
			# Si no existe un producto con el mismo nombre, lo insertamos
			if productos_collection.find_one({'nombre': dato['nombre']}) == None:
				descargarImagen(p['image'], './static/images', dato['imágen'])
				producto = Producto(**dato)
				productos_collection.insert_one(producto.model_dump())

def guardarCompras():
	## Obtenemos las compras y las insertamos en la BD
	## En este caso, he puesto que las compras las realiza siempre el mismo usuario
	## otra forma sería obtener los usuarios de la API, pero por simplicidad, lo he hecho así
	compras = getProductos('https://fakestoreapi.com/carts')
	for c in compras:
		productos = []
		for p in c['products']:
			producto = {
				'idProducto': p['productId'],
				'cantidad': p['quantity']
			}
			productos.append(producto)

		dato = {
			'usuario': 'fulanito@correo.com',
			'fecha': c['date'],
			'productos': productos
		}
		
		compra = Compra(**dato)
		compras_collection.insert_one(compra.model_dump())

def consultarProductos():
	resultado = productos_collection.find()
	productos = []
	for result in resultado:
		productos.append(result)
	return productos

def consultarCategoria(categoria):
	if(categoria == "mens clothing"):
		categoria = "men's clothing"
	elif(categoria == "womens clothing"):
		categoria = "women's clothing"

	resultado = productos_collection.find({'categoría': categoria})
	productos = []
	for result in resultado:
		productos.append(result)
	return productos

def buscarProducto(nombre):
	resultado = productos_collection.find({'nombre': {'$regex': nombre, '$options': 'i'}})
	productos = []
	
	for result in resultado:
		print(nombre)
		productos.append(result)
	return productos

def insertarProducto(nombre, precio, descripcion, categoria, imagen):
	if(categoria == "mens clothing"):
		categoria = "men's clothing"
	elif(categoria == "womens clothing"):
		categoria = "women's clothing"

	imagenNombre = guardarImagen(imagen)

	dato = {
		'nombre': nombre, 
		'precio': precio, 
		'descripción': descripcion,
		'categoría': categoria,
		'imágen': imagenNombre,
		'rating': {'puntuación': 0, 'cuenta': 1}
	}
	producto = Producto(**dato)
	productos_collection.insert_one(producto.model_dump())

def copia_de_seguridad():
	## Hacemos una copia de seguridad
	respuesta = input("\n¿Quiere hacer una copia de seguridad? (s/n): ")
	if respuesta == 's':
		copiaSeguridad()
		print("\nCopia de seguridad realizada")
