from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from backend.config import PIMIENTA_SECRETA

def _derivar_password_unico(email_usuario: str) -> str:

    combinacion = email_usuario + PIMIENTA_SECRETA
    h = SHA256.new(combinacion.encode())
    return h.hexdigest()

def generate_keys_bytes(email_usuario: str): 

    key = RSA.generate(2048)
    
    password_unico = _derivar_password_unico(email_usuario)
    
    private_key_encrypted = key.export_key(
        format='PEM', 
        passphrase=password_unico, 
        pkcs=8, 
        protection="scryptAndAES128-CBC"
    )
    
    public_key = key.publickey().export_key()
    
    return private_key_encrypted, public_key

if __name__ == "_main_":
    print("Probando generación segura...")
    priv, pub = generate_keys_bytes("test@demo.com")
    print(f"Llave privada ENCRIPTADA generada ({len(priv)} bytes)")
    print(f"Llave pública generada ({len(pub)} bytes)")