from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

def verify_signature_bytes(pdf_bytes: bytes, signature_bytes: bytes, public_key_bytes: bytes) -> bool:
    """
    Verifica criptográficamente si una firma corresponde a un PDF y a un usuario.
    
    Args:
        pdf_bytes (bytes): El contenido binario del archivo original.
        signature_bytes (bytes): El contenido binario de la firma (.bin).
        public_key_bytes (bytes): La llave pública del usuario (sacada de la BD).
        
    Returns:
        bool: True si es válida, False si no.
    """
    try:
        # 1. Importar la llave pública (que viene de la Base de Datos)
        public_key = RSA.import_key(public_key_bytes)
        
        # 2. Calcular el Hash del PDF original que nos están enviando
        # IMPORTANTE: Hasheamos el archivo entero, no solo el texto.
        h = SHA256.new(pdf_bytes)
        
        # 3. Verificar la firma contra ese Hash
        # Si la firma no coincide, esta función lanza una excepción (ValueError)
        pkcs1_15.new(public_key).verify(h, signature_bytes)
        
        return True
        
    except (ValueError, TypeError):
        # Esto ocurre si la firma es falsa o el documento fue alterado
        return False
    except Exception as e:
        print(f"Error inesperado en verificación: {e}")
        return False