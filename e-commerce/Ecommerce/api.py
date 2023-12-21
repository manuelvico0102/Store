from ninja_extra import NinjaExtraAPI, api_controller, http_get
from ninja import File, Schema, Form
from ninja.files import UploadedFile
from ninja.security import django_auth
from typing import List
import Seed
from bson import ObjectId

api = NinjaExtraAPI()

"""class Producto(Schema):
	nombre: str
	precio: float
	descripcion: str = None
	categoria: str"""

class Rate(Schema):
	rate: float
	count: int
	
class ProductSchema(Schema):
	id:    str
	title: str
	price: float
	description: str
	category: str
	image: str = None
	rating: Rate
	
	
class ProductSchemaIn(Schema):
	title: str
	price: float
	description: str
	category: str
	rating: Rate
	
	
class ErrorSchema(Schema):
	message: str

@api.get("/productos", tags=['CRUD'], response=List[ProductSchema])
def get_productos(request, desde: int = 0, hasta: int = 10):
	qs = Seed.consultarProductos()[desde:hasta]	
	qs_with_id = [{"id": item.pop("_id"), **item} for item in qs]
	return qs_with_id

@api.post("/productos", tags=['CRUD'])
def agregar_producto(request, payload:ProductSchemaIn, imagen: UploadedFile = File(...)):
	insertarProducto(payload, imagen)
	response = {"mensaje": "Producto agregado correctamente"}
	return response

def insertarProducto(payload:ProductSchemaIn, imagen):
	categoria =	payload.category
	if(categoria == "mens clothing"):
		categoria = "men's clothing"
	elif(categoria == "womens clothing"):
		categoria = "women's clothing"

	imagenNombre = Seed.guardarImagen(imagen)

	nuevo_producto = Seed.productos_collection.insert_one({})
	dato = {
		'id': str(nuevo_producto.inserted_id),
		'title': payload.title, 
		'price': payload.price, 
		'description': payload.description,
		'category': categoria,
		'image': imagenNombre,
		'rating': payload.rating
	}
	producto = ProductSchema(**dato)
	Seed.productos_collection.update_one({"_id": nuevo_producto.inserted_id}, {"$set": producto.dict()})

@api.get("/producto/{producto_id}", tags=['CRUD'], response=ProductSchema)
def get_producto_por_id(request, producto_id: str):
	producto = Seed.buscarProductoPorId(producto_id)
	if producto:
		producto["id"] = producto.pop("_id")
		return producto
	else:
		return {"error": "Producto no encontrado"}
	
@api.put("/productos/{id}", tags=['CRUD'], response = {202: ProductSchema, 404: ErrorSchema})
def Modifica_producto(request, id: str, payload: ProductSchemaIn):
	try:
		data = Seed.buscarProductoPorId(id)

		payload_dict = payload.dict(exclude={'id'})

		data.update(payload_dict)

		Seed.productos_collection.update_one({"_id": ObjectId(id)}, {"$set": payload_dict})
		return 202, data
	except:
		return 404, {"error": "Producto no encontrado"}
	
@api.put("/productos_rate/{id}/{rate}", tags=['CRUD'])
def modifica_rate(request, id: str, rate: int):
	if request.user.is_authenticated:
		try:
			data = Seed.buscarProductoPorId(id)
			rate_inicial = data['rating']['rate']
			count_inicial = data['rating']['count']
			count_final = count_inicial + 1
			rate_final = ((rate_inicial * count_inicial) + (rate * 1.0)) / count_final

			Seed.productos_collection.update_one({"_id": ObjectId(id)}, {"$set": {"rating.rate": rate_final, "rating.count": count_final}})
			return {"mensaje": "Rate modificado correctamente"}
		except:
			return {"error": "Producto no encontrado"}
	else:
		return {"error": "Usuario no autenticado"}

@api.delete("/producto/{producto_id}", tags=['CRUD'])
def borrar_producto(request, producto_id: str):
    try:
        if Seed.buscarProductoPorId(producto_id):
            Seed.eliminarProducto(producto_id)
            return {"mensaje": "Producto eliminado exitosamente"}
        return {"error": "Producto no encontrado"}
    except Exception as e:
        return {"error": f"Error al borrar producto: {str(e)}"}