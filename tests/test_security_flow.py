import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_flujo_seguridad_con_imagenes():
    """
    Este test valida que el sistema detecte alteraciones no solo de texto,
    sino también de imagenes o datos binarios dentro del pdf.
    """
    
    email_usuario = "persona5_visual@test.com"
    nombre_usuario = "Tester Visual"
    
    # Imaginemos que los bytes representan una imagen JPG incrustada
    pdf_con_imagen_original = b"%PDF-1.5 Texto del contrato... [DATOS_BINARIOS_DE_FOTO_ORIGINAL_xFF_xD8]"
    
    # PDF HACKEADO 
    pdf_con_imagen_hackeada = b"%PDF-1.5 Texto del contrato... [DATOS_BINARIOS_DE_FOTO_FALSA_x00_x00]"

    print(f"\n INICIANDO PRUEBA DE INTEGRIDAD DE IMAGENES ")

    # CREAR USUARIO
    resp_registro = client.post("/usuarios/", json={"nombre": nombre_usuario, "email": email_usuario})
    if resp_registro.status_code == 200:
        user_id = resp_registro.json()["id"]
    else:
        user_id = 1 

    # FIRMAR EL PDF CON IMAGEN
    files = {'archivo': ('contrato_con_foto.pdf', pdf_con_imagen_original, 'application/pdf')}
    data = {'usuario_id': user_id}
    
    resp_firma = client.post("/firmar-pdf/", data=data, files=files)
    assert resp_firma.status_code == 200
    firma_digital = resp_firma.content
    print("[OK] Documento con imágenes firmado correctamente.")

    # INTENTO DE HACKEO DE IMAGEN
    files_hack = {
        'archivo_original': ('contrato_con_foto.pdf', pdf_con_imagen_hackeada, 'application/pdf'), 
        'archivo_firma': ('contrato_con_foto.pdf.bin', firma_digital, 'application/octet-stream')
    }
    data_verify = {'usuario_id': user_id}

    resp_hack = client.post("/verificar-firma/", data=data_verify, files=files_hack)
    resultado = resp_hack.json()["resultado"]

    # VALIDACION
    assert resultado == "INVALIDO"
    print(f"[EXITO] El sistema detecto la manipulación de la imagen. Resultado: {resultado}")