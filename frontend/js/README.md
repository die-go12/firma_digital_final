# Lógica de Cliente (JavaScript)

Este directorio contiene los scripts que manejan la interactividad del usuario y la comunicación con la API del Backend.

## Archivos

* **`api.js`**: Capa de servicio.
    * Contiene las funciones `fetch` para conectar con los endpoints (`/firmar-pdf`, `/verificar-firma`, etc.).
    * Maneja la configuración de cabeceras y la recepción de archivos binarios (Blobs).

* **`main.js`**: Controlador de interfaz.
    * Escucha los eventos del DOM (clicks en botones, carga de archivos).
    * Llama a las funciones de `api.js`.
    * Actualiza la pantalla con los resultados (alertas de éxito/error, descarga de archivos).

## Configuración
La URL base de la API está definida en `api.js` (por defecto `http://127.0.0.1:8000`).