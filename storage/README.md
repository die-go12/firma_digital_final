## Storage - Almacenamiento Local
Este directorio actúa como el sistema de archivos local para la persistencia temporal de la aplicación.

Advertencia de Seguridad
NUNCA subir archivos sensibles a este repositorio. El contenido de las subcarpetas aquí listadas está configurado en .gitignore para evitar fugas de información, ya que en un entorno real aquí residirían llaves privadas y documentos confidenciales.

Estructura Interna
Este directorio debe contener las siguientes subcarpetas para el correcto funcionamiento del Backend:

keys/: Almacena las llaves privadas (encriptadas) y públicas generadas.
    certs/: Almacena los certificados JSON emitidos por la CA simulada.
    signed_pdfs/: Destino de los archivos PDF firmados y sus firmas (.bin).
    temp/: Directorio para carga temporal de archivos durante el procesamiento de la API.

