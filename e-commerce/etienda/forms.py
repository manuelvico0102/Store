from django import forms
import logging

logger = logging.getLogger(__name__)

class ProductoForm(forms.Form):
	nombre = forms.CharField(
		label='Nombre', max_length=100, required=True, 
		error_messages={
			'required': 'El nombre es requerido', 
			'max_length': 'El nombre no puede tener más de 100 caracteres'
		}
	)
	precio = forms.DecimalField(
		label='Precio', required=True, 
		error_messages={
			'required': 'El precio es requerido',
			'invalid': 'El precio debe ser un número'
		}
	)
	descripcion = forms.CharField(
		label='Descripción', max_length=1000, required=True, 
		error_messages={
			'required': 'La descripción es requerida'
		}
	)
	categoria = forms.CharField(
		label='Categoría', max_length=100, required=True, 
		error_messages={
			'required': 'La categoría es requerida'
		}
	)
	imagen = forms.ImageField(
		label='Imagen', required=True, 
		error_messages={
			'required': 'La imagen es requerida'
		}
	)

	def clean_nombre(self):
		nombre = self.cleaned_data['nombre']
		if nombre[0].islower():
			raise forms.ValidationError('El nombre debe empezar con mayúscula')
		return nombre

	def clean_precio(self):
		precio = self.cleaned_data['precio']
		if precio <= 0:
			raise forms.ValidationError('El precio no puede ser menor a 0')
		return precio
	

	