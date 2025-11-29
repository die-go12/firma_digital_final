from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from backend.config import PIMIENTA_SECRETA  

def _derivar_password_unico(email_usuario: str) -> str:
    """
    Reconstruye la contraseña única (Sal + Pimienta) para poder desencriptar la llave.
    Debe ser EXACTAMENTE igual a la función de keygen.py
    """
    combinacion = email_usuario + PIMIENTA_SECRETA
    h = SHA256.new(combinacion.encode())
    return h.hexdigest()

def sign_pdf_bytes(pdf_bytes: bytes, private_key_encrypted_bytes: bytes, email_usuario: str) -> bytes:
    """
    Firma digitalmente el PDF.
    
    Args:
        pdf_bytes: El archivo PDF.
        private_key_encrypted_bytes: La llave privada ENCRIPTADA (viene de la BD).
        email_usuario: El email del usuario (se usa como SAL para desbloquear la llave).
    """
    try:
        password_unico = _derivar_password_unico(email_usuario)

        private_key = RSA.import_key(private_key_encrypted_bytes, passphrase=password_unico)

        h = SHA256.new(pdf_bytes)

        firma = pkcs1_15.new(private_key).sign(h)

        return firma

    except ValueError:
        raise Exception("SEGURIDAD: No se pudo desencriptar la llave privada. Contraseña incorrecta.")
