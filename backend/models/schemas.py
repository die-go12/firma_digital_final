from pydantic import BaseModel
from datetime import datetime

#ESQUEMAS PARA USUARIOS 

#base: datos comunes
class UsuarioBase(BaseModel):
    nombre: str
    email: str

# create: lo que recibimos al crear (solo nombre y email)
class UsuarioCreate(UsuarioBase):
    pass

# out: lo que devolvemos al usuario (incluye ID y Fecha, pero NO la llave privada)
class UsuarioOut(UsuarioBase):
    id: int
    fecha_creacion: datetime
    # public_key: bytes  
    
    class Config:
        from_attributes = True # obligatorio para leer de sqlalchemy

# ESQUEMAS PARA DOCUMENTOS 

class DocumentoOut(BaseModel):
    id: int
    nombre_archivo: str
    fecha_firma: datetime
    hash_documento: str
    ruta_storage: str
    
    class Config:
        from_attributes = True