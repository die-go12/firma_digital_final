from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.db.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    
    # guardamos las llaves criptograficas como bytes (LargeBinary)
    public_key = Column(LargeBinary) 
    private_key = Column(LargeBinary) 

    # relacion: un usuario tiene muchos documentos
    documentos = relationship("Documento", back_populates="propietario")

class Documento(Base):
    __tablename__ = "documentos"

    id = Column(Integer, primary_key=True, index=True)
    nombre_archivo = Column(String)
    ruta_storage = Column(String) # donde se guarda el pdf firmado
    hash_documento = Column(String) # huella digital del archivo
    firma_digital = Column(LargeBinary) # La firma en bytes
    fecha_firma = Column(DateTime, default=datetime.utcnow)
    
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    # relacion: un documento pertenece a un usuario
    propietario = relationship("Usuario", back_populates="documentos")