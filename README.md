# Tienda
Esta es una aplicación web de catálogo de productos, para la asignatura de Desarrollo de Aplicaciones para Internet, que utiliza MongoDB como base de datos, Python como lenguaje principal, y Django como framework web. Además, se ha implementado una API con Ninja Extra para interactuar con la base de datos. La interfaz de usuario ha sido construida con Bootstrap, CSS, y HTML, con funcionalidades adicionales de evaluación de productos mediante estrellas implementadas en JavaScript.

Además, se ha desarrollado una versión paralela de la página web utilizando React con Vite, permitiendo así una comparativa entre ambas implementaciones.

## Características Principales
**Base de Datos**: MongoDB se utiliza como la base de datos principal para almacenar la información de los productos.

**Lenguaje de Programación**: Python es el lenguaje principal utilizado para el desarrollo de la aplicación.

**Framework Web**: Django se ha empleado como el framework web para la construcción de la aplicación, facilitando la gestión de rutas, vistas, y la integración de la API.

**API**: La API se ha construido con Ninja Extra, proporcionando un conjunto de endpoints para interactuar con la base de datos y realizar operaciones CRUD.

**Interfaz de Usuario**: La interfaz de usuario ha sido diseñada utilizando Bootstrap, CSS, y HTML. Además, se ha implementado JavaScript para permitir la evaluación de productos mediante estrellas.

**Versión Paralela en React**: Se ha creado una versión paralela de la página web utilizando React con Vite, permitiendo una comparación entre las implementaciones Django y React.

## Despliegue

Para desplegar la aplicación, sigue estos pasos:

1. Clona el repositorio:

```bash
git clone git@github.com:manuelvico0102/Tienda.git
```

2. Navega al directorio del proyecto:

```bash
cd Tienda
```

3. Ejecuta el siguiente comando para construir las imágenes de Docker:

```bash
docker-compose -f ./docker-compose-prod.yml build
```

4. Luego, inicia los contenedores:

```bash
docker-compose -f ./docker-compose-prod.yml up
```

5. Ahora puedes acceder a la página web principal ingresando:

```bash
http://localhost/
```

6. Para acceder a la versión de React, utiliza:

```bash
http://localhost/react/
```
