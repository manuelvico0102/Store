# Seed.py
from pydantic import BaseModel, FilePath, Field, EmailStr
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime
from typing import Any
import requests
import os
import subprocess
		
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
			descargarImagen(p['image'], './imagenes', dato['imágen'])
			producto = Producto(**dato)
			productos_collection.insert_one(producto.model_dump())

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


## Consulta Electrónica entre 100 y 200€, ordenados por precio
resultado = productos_collection.find({'categoría': 'electronics', 'precio': {'$gte': 100, '$lte': 200}}).sort('precio', 1)

print("\nConsulta Electrónica entre 100 y 200€, ordenados por precio")
print("Nombre\t Precio")
for result in resultado:
    print(result['nombre'] + "\t " + str(result['precio']) + "€")
print("-" * 100)

## Productos que contengan la palabra 'pocket' en la descripción
resultado = productos_collection.find({'descripción': {'$regex': 'pocket'}})
print("\nProductos que contengan la palabra 'pocket' en la descripción")
print("Nombre")
for result in resultado:
    print(result['nombre'])
print("-" * 100)

## Productos con puntuación mayor de 4
resultado = productos_collection.find({'rating.puntuación': {'$gt': 4}})
print("\nProductos con puntuación mayor de 4")
print("Nombre\t Puntuación")
for result in resultado:
	print(result['nombre'] + "\t " + str(result['rating']['puntuación']))
print("-" * 100)	

## Ropa de hombre, ordenada por puntuación
resultado = productos_collection.find({'categoría': 'men\'s clothing'}).sort('rating.puntuación', -1)
print ("\nRopa de hombre, ordenada por puntuación")
print("Nombre\t Puntuación")
for result in resultado:
	print(result['nombre'] + "\t " + str(result['rating']['puntuación']))
print("-" * 100)

## Facturación total
resultados = compras_collection.find()
total = 0

for compra in resultados:
	for producto in compra['productos']:
		resultado = productos_collection.find()[producto['idProducto'] - 1]
		total += resultado['precio'] * producto['cantidad']

print("\nFacturación total: " + str(total) + "€")
print("-" * 100)

## Facturación por categoría
categorias = productos_collection.distinct('categoría')
for categoria in categorias:
	resultados = compras_collection.find()
	total = 0
	for compra in resultados:
		for producto in compra['productos']:
			resultado = productos_collection.find()[producto['idProducto'] - 1]
			if resultado['categoría'] == categoria:
				total += resultado['precio'] * producto['cantidad']
	print("\nFacturación de la categoría " + categoria + ": " + str(total) + "€")


## Hacemos una copia de seguridad
respuesta = input("\n¿Quiere hacer una copia de seguridad? (s/n): ")
if respuesta == 's':
	copiaSeguridad()
	print("\nCopia de seguridad realizada")

## borramos productos y compras
compras_collection.delete_many({})
productos_collection.delete_many({})