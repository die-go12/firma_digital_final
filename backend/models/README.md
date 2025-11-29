# Modelos y Esquemas de Datos

Este directorio define cómo se estructuran los datos tanto en la base de datos como en la API.

## Archivos

* **`models.py` (SQLAlchemy)**:
    * Define las tablas reales de la Base de Datos (`Tablas: Usuarios, Documentos`).
    * Mapea las relaciones entre usuarios y sus documentos firmados.

* **`schemas.py` (Pydantic)**:
    * Define las reglas de validación para los datos que entran y salen de la API.
    * Asegura que los JSONs de respuesta no expongan datos sensibles (como la llave privada encriptada) a menos que sea necesario.