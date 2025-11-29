from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

def verify_signature_bytes(pdf_bytes: bytes, signature_bytes: bytes, public_key_bytes: bytes) -> bool:
    try:
        public_key = RSA.import_key(public_key_bytes)
        
        h = SHA256.new(pdf_bytes)

        pkcs1_15.new(public_key).verify(h, signature_bytes)
        
        return True
        
    except (ValueError, TypeError):
        return False
    except Exception as e:
        print(f"Error inesperado en verificación: {e}")
        return False