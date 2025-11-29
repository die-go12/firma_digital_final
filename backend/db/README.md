# Database Configuration

Este directorio maneja la conexión y configuración de la base de datos SQLite.

## Archivos

* **`database.py`**:
    * Configura el motor de base de datos (`SQLAlchemy Engine`).
    * Define la sesión (`SessionLocal`) que se inyecta en cada petición de la API.
    * Establece la clase base (`Base`) para los modelos ORM.

## Configuración
Por defecto, la base de datos se crea en la raíz del proyecto como un archivo `sql_app.db`.