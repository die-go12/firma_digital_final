
import os
import shutil
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.responses import Response  #COMENTARIO

# IMPORTACIONES DE LA ARQUITECTURA
from backend.db import database
from backend.models import models, schemas
# Importamos TODOS los módulos de criptografia
from backend.crypto import keygen, signer, ca, verifier

# Inicializar Base de Datos
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Sistema de Firma Digital - Equipo Cripto")

# CONFIGURACIÓN DE SEGURIDAD (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas de almacenamiento
STORAGE_PDF_PATH = "storage/signed_pdfs"
CERTS_PATH = "storage/certs"
os.makedirs(STORAGE_PDF_PATH, exist_ok=True)
os.makedirs(CERTS_PATH, exist_ok=True)

# Dependencia de BD
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"mensaje": "API Activa. Sistema listo para operar."}



# 1. GESTIÓN DE USUARIOS (Generación de Llaves Segura)

@app.post("/usuarios/", response_model=schemas.UsuarioOut)
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    # Verificar duplicados
    db_user = db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    # GENERAR LLAVES (Llamada a keygen.py)
    try:
        # ✅ CAMBIO SEGURIDAD: Pasamos el email para usarlo como SAL
        priv, pub = keygen.generate_keys_bytes(usuario.email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando llaves: {e}")

    # Guardar en BD
    nuevo_usuario = models.Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        public_key=pub,
        private_key=priv
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


# 2. FIRMA DE DOCUMENTOS (Desencriptado Seguro)

@app.post("/firmar-pdf/")
async def firmar_documento(
    usuario_id: int = Form(...),
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Buscar usuario
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Leer PDF en memoria
    contenido_pdf = await archivo.read()

    # FIRMAR (Llamada a signer.py)
    try:
        # el email para poder desencriptar la llave privada
        firma_digital = signer.sign_pdf_bytes(contenido_pdf, usuario.private_key, usuario.email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error firmando: {e}")

    # A. Guardar PDF firmado físico
    nombre_pdf = f"firmado_{usuario.nombre}_{archivo.filename}"
    ruta_pdf = os.path.join(STORAGE_PDF_PATH, nombre_pdf)
    
    await archivo.seek(0)
    with open(ruta_pdf, "wb") as buffer:
        shutil.copyfileobj(archivo.file, buffer)

    # B. Guardar archivo de FIRMA (.bin)
    nombre_firma = f"{nombre_pdf}.bin"
    ruta_firma = os.path.join(STORAGE_PDF_PATH, nombre_firma)
    with open(ruta_firma, "wb") as f:
        f.write(firma_digital)

    # C. Registrar en BD
    nuevo_doc = models.Documento(
        nombre_archivo=archivo.filename,
        ruta_storage=ruta_pdf,
        hash_documento="SHA256-Calculado",
        firma_digital=firma_digital,
        usuario_id=usuario.id
    )
    db.add(nuevo_doc)
    db.commit()
    db.refresh(nuevo_doc)

    # Devolver archivo .bin para descarga directa
    return FileResponse(
        path=ruta_firma, 
        filename=nombre_firma, 
        media_type='application/octet-stream'
    )


# 3. VERIFICACION DE FIRMAS (El Juez)


@app.post("/verificar-firma/")
async def verificar_firma(
    usuario_id: int = Form(...),
    archivo_original: UploadFile = File(...),
    archivo_firma: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    pdf_bytes = await archivo_original.read()
    firma_bytes = await archivo_firma.read()

    es_valida = verifier.verify_signature_bytes(
        pdf_bytes=pdf_bytes,
        signature_bytes=firma_bytes,
        public_key_bytes=usuario.public_key
    )

    if es_valida:
        return {"resultado": "VALIDO", "detalle": "La firma es AUTÉNTICA y el documento NO ha sido alterado."}
    else:
        return {"resultado": "INVALIDO", "detalle": "La firma NO corresponde o el documento fue modificado."}



# 4. CERTIFICADOS

@app.post("/emitir-certificado/")
def emitir_certificado_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    autoridad = ca.AutoridadCertificadora()
    try:
        pub_key_str = usuario.public_key.decode('utf-8')
        cert = autoridad.emitir_certificado(usuario.nombre, pub_key_str)
        
        ruta_json = os.path.join(CERTS_PATH, f"{usuario.nombre}_cert.json")
        import json
        with open(ruta_json, "w") as f:
            json.dump(cert, f, indent=4)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error CA: {e}")
        
    return cert

@app.get("/listar-certificados-locales")
def listar_certs():
    if not os.path.exists(CERTS_PATH):
        return []
    return [f for f in os.listdir(CERTS_PATH) if f.endswith(".json")]


# 5. VERIFICACIÓN UNIVERSAL (Auditoría Externa)

@app.post("/verificar-externo/")
async def verificar_con_llave_publica(
    archivo_original: UploadFile = File(...),
    archivo_firma: UploadFile = File(...),
    archivo_llave_publica: UploadFile = File(...) 
):
    """
    Endpoint de Auditoría Forense:
    Verifica una firma subiendo explícitamente la llave pública (.pem o .key).
    NO consulta la base de datos interna. Sirve para validar firmas offline.
    """
    try:
        # 1. Leemos los tres archivos en memoria (bytes)
        pdf_bytes = await archivo_original.read()
        firma_bytes = await archivo_firma.read()
        public_key_bytes = await archivo_llave_publica.read()

        # 2. Usamos el verificador puro (sin depender de usuarios ni IDs de la BD)
        es_valida = verifier.verify_signature_bytes(
            pdf_bytes=pdf_bytes,
            signature_bytes=firma_bytes,
            public_key_bytes=public_key_bytes
        )

        if es_valida:
            return {
                "resultado": "VALIDO", 
                "detalle": "La firma corresponde matemáticamente a la llave pública proporcionada."
            }
        else:
            return {
                "resultado": "INVALIDO", 
                "detalle": "La firma NO corresponde a esta llave pública o el documento fue alterado."
            }
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error procesando archivos: {str(e)}")
    

# 6. DESCARGA DE LLAVE PUBLICA (Para Auditoría)

@app.get("/descargar-publica/{usuario_id}")  
def descargar_key(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Limpiamos el nombre de espacios para evitar errores en la descarga
    nombre_safe = usuario.nombre.replace(" ", "_")
    
    # Devolvemos los bytes directos como archivo
    return Response(
        content=usuario.public_key,
        media_type="application/x-pem-file",
        headers={"Content-Disposition": f"attachment; filename=public_key_{nombre_safe}.pem"}
    )