from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 1.definimos la ruta de la base de datos

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# 2.creamos el motor (engine)
# connect_args={"check_same_thread": False} es necesario SOLO para sqlite 
# porque sqlite por defecto solo permite un hilo a la vez, y fastapi usa varios
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3.creamos la sesion (SessionLocal)
# esta sera la "fabrica" de sesiones de base de datos.cada peticion tendra su propia sesion.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4.creamos la clase base
Base = declarative_base()

# 5.dependencia (utilidad para obtener la db en otros archivos)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()