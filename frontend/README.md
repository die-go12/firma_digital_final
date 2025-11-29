## Frontend - Interfaz de Usuario
Este directorio contiene la interfaz gráfica del proyecto, diseñada con tecnologías web estándar (HTML, CSS y JavaScript Vanilla) para garantizar ligereza y facilidad de despliegue.

Descripción
El Frontend actúa como cliente para consumir la API REST del Backend. Permite a los usuarios realizar todo el flujo de firma digital sin tocar código ni consola.

Estructura de Archivos
index.html: Página de inicio. Permite el registro de nuevos usuarios en el sistema.

dashboard.html: Panel principal. Aquí se suben los PDFs para ser firmados y se descargan las firmas (.bin).

verificar.html: Página pública de auditoría. Permite subir un PDF y su firma para validar su autenticidad e integridad.

js/api.js: Lógica de comunicación (Fetch API) con el Backend (localhost:8000).

css/styles.css: Estilos visuales para una experiencia de usuario limpia.

Cómo Ejecutar
No requiere instalación de node_modules ni compilación.

Asegúrate de que el Backend esté corriendo (uvicorn backend.main:app --reload).

Abre el archivo index.html directamente con tu navegador web favorito (Chrome, Edge, Firefox).

Navega entre las páginas usando los botones de la interfaz.

Conexión
Por defecto, este frontend está configurado para buscar la API en: http://127.0.0.1:8000

Nota: Si el backend cambia de puerto o IP, actualizar la constante API_URL en js/api.js.