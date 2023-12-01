# Seed.py
from pydantic import BaseModel, FilePath, Field, EmailStr
from pymongo import MongoClient
from datetime import datetime
from typing import Any
import requests
import os
import subprocess
from datetime import datetime
from django.contrib import messages
from bson import ObjectId
		
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
	rate: float = Field(ge=0., lt=5.)
	count: int = Field(ge=0)
				
class Producto(BaseModel):
	_id: Any
	title: str
	price: float
	description: str
	category: str
	image: str | None
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
		'title': p['title'], 
		'price': p['price'], 
		'description': p['description'],
		'category': p['category'],
		'image': p['image'].split("/")[-1], 
		'rating': {'rate': p['rating']['rate'], 'count': p['rating']['count']}
		}
		# Nos aseguramos que el nombre empieza en mayuscula
		if not dato['title'][0].islower():
			# Si no existe un producto con el mismo nombre, lo insertamos
			if productos_collection.find_one({'title': dato['title']}) == None:
				descargarImagen(p['image'], './static/images', dato['image'])
				productos_collection.insert_one(dato)

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
		compras_collection.insert_one(compra)

def consultarProductos():
	resultado = productos_collection.find()
	productos = []
	for result in resultado:
		result['id'] = str(result['_id'])
		productos.append(result)
	return productos

def consultarCategoria(categoria):
	if(categoria == "mens clothing"):
		categoria = "men's clothing"
	elif(categoria == "womens clothing"):
		categoria = "women's clothing"

	resultado = productos_collection.find({'category': categoria})
	productos = []
	for result in resultado:
		result['id'] = str(result['_id'])
		productos.append(result)
	return productos

def buscarProducto(request, nombre):
	resultado = productos_collection.find({'title': {'$regex': nombre, '$options': 'i'}})
	productos = []
	
	for result in resultado:
		print(nombre)
		productos.append(result)
	
	#Comprobar si los productos esta vacio
	if not productos:
		messages.error(request, 'No se ha encontrado ningún producto con ese nombre')
	else:
		messages.success(request, "Se han encontrado coincidencias")
	return productos

def buscarProductoPorId(producto_id):
	try:
		producto_id = ObjectId(producto_id)
		resultado = productos_collection.find_one({"_id": producto_id})
		if resultado:
			resultado['_id'] = str(resultado['_id'])
			return resultado
		else:
			messages.error("Producto no encontrado")
	except Exception as e:
		raise Exception(f"Error al buscar producto por ID: {str(e)}")
	
def insertarProducto(nombre, precio, descripcion, categoria, imagen):
	if(categoria == "mens clothing"):
		categoria = "men's clothing"
	elif(categoria == "womens clothing"):
		categoria = "women's clothing"

	imagenNombre = guardarImagen(imagen)

	dato = {
		'title': nombre, 
		'price': precio, 
		'description': descripcion,
		'category': categoria,
		'image': imagenNombre,
		'rating': {'rate': 0, 'count': 0}
	}
	producto = dict(Producto(**dato))
	producto['rating'] = dict(producto['rating'])
	productos_collection.insert_one(producto)

def modificarProducto(producto_id, datos_modificados):
    try:
        producto_id = ObjectId(producto_id)
        productos_collection.update_one({"_id": producto_id}, {"$set": datos_modificados})
    except Exception as e:
        raise Exception(f"Error al modificar producto: {str(e)}")
	
def eliminarProducto(producto_id):
    try:
        producto_id = ObjectId(producto_id)
        productos_collection.delete_one({"_id": producto_id})
    except Exception as e:
        raise Exception(f"Error al eliminar producto: {str(e)}")

def copia_de_seguridad():
	## Hacemos una copia de seguridad
	respuesta = input("\n¿Quiere hacer una copia de seguridad? (s/n): ")
	if respuesta == 's':
		copiaSeguridad()
		print("\nCopia de seguridad realizada")

# Borrar todos los productos de la BD
#productos_collection.delete_many({})
# Añadir productos
#guardarProductos()