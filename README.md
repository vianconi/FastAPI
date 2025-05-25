# API de Reseñas de Películas

Este proyecto es una API desarrollada con **FastAPI** y **Peewee** para gestionar reseñas de películas, usuarios y más. Permite a los usuarios registrarse, autenticarse, crear reseñas de películas, consultar y modificar información relacionada.

## Características

- Registro y autenticación de usuarios
- Creación y consulta de películas
- Creación, consulta, actualización y eliminación de reseñas
- Autenticación basada en JWT
- Uso de base de datos PostgreSQL mediante Peewee ORM

## Estructura del Proyecto

```
project/
    routers/
    common/
    database.py
    schemas.py
    __init__.py
main.py
client.py
client3.py
requirements.txt
.env
```

## Requisitos

- Python 3.11+
- PostgreSQL

## Instalación

1. **Clona el repositorio:**

   ```sh
   git clone https://github.com/tu-usuario/tu-repo.git
   cd tu-repo
   ```

2. **Crea un entorno virtual (opcional pero recomendado):**

   ```sh
   python -m venv .venv
   source .venv/bin/activate  # En Windows: .venv\Scripts\activate
   ```

3. **Instala las dependencias:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Configura las variables de entorno:**

   Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido (ajusta los valores según tu configuración):

   ```
   DB_NAME=nombre_de_tu_db
   DB_USER=usuario
   DB_PASSWORD=contraseña
   DB_HOST=localhost
   DB_PORT=5432
   SECRET_KEY=tu_clave_secreta
   ```

5. **Ejecuta la aplicación:**

   ```sh
   uvicorn main:app --reload
   ```

   La API estará disponible en [http://localhost:8000](http://localhost:8000).

## Uso

Puedes probar los endpoints usando herramientas como **curl**, **Postman** o los clientes incluidos (`client.py`, `client3.py`). También puedes acceder a la documentación interactiva en [http://localhost:8000/docs](http://localhost:8000/docs).

---