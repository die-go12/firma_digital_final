import os
import json
from datetime import datetime, timedelta
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

CERTS_PATH = "storage/certs"
CA_PRIVATE_KEY = f"{CERTS_PATH}/ca_private.pem"
CA_PUBLIC_KEY = f"{CERTS_PATH}/ca_public.pem"

class CertificadoInvalido(Exception):
    pass

class AutoridadCertificadora:
    def __init__(self):
        os.makedirs(CERTS_PATH, exist_ok=True)
        
        if not os.path.exists(CA_PRIVATE_KEY):
            self._crear_llaves_ca()

        with open(CA_PRIVATE_KEY, "rb") as f:
            self.private_key = RSA.import_key(f.read())
        
        with open(CA_PUBLIC_KEY, "rb") as f:
            self.public_key = RSA.import_key(f.read())

    def _crear_llaves_ca(self):
        print("Generando nuevas llaves maestras para la CA.")
        key = RSA.generate(2048)
        with open(CA_PRIVATE_KEY, "wb") as f: f.write(key.export_key())
        with open(CA_PUBLIC_KEY, "wb") as f: f.write(key.publickey().export_key())
    
    def emitir_certificado(self, nombre_usuario: str, public_key_str: str) -> dict:
        certificado = {
            "subject": nombre_usuario,
            "public_key": public_key_str,
            "issuer": "CA-Simulada-Backend",
            "valid_from": datetime.utcnow().isoformat(),
            "valid_to": (datetime.utcnow() + timedelta(days=365)).isoformat(),
            "serial_number": int(datetime.utcnow().timestamp())
        }

        payload_bytes = json.dumps(certificado, sort_keys=True).encode('utf-8')
        h = SHA256.new(payload_bytes)
        firma = pkcs1_15.new(self.private_key).sign(h)
        
        certificado["firma_ca"] = firma.hex()
        return certificado

    def validar_certificado(self, cert_dict: dict) -> bool:

        ahora = datetime.utcnow().isoformat()
        if not (cert_dict["valid_from"] <= ahora <= cert_dict["valid_to"]):
            raise CertificadoInvalido("El certificado ha expirado o aún no es válido.")

        firma_hex = cert_dict.get("firma_ca")
        if not firma_hex:
            raise CertificadoInvalido("El certificado no tiene firma.")
            
        firma = bytes.fromhex(firma_hex)

        cert_sin_firma = cert_dict.copy()
        del cert_sin_firma["firma_ca"]

        h = SHA256.new(json.dumps(cert_sin_firma, sort_keys=True).encode())

        try:
            pkcs1_15.new(self.public_key).verify(h, firma)
        except (ValueError, TypeError):
            raise CertificadoInvalido("Firma digital del certificado inválida. El certificado ha sido adulterado.")

        return True

    def obtener_public_key_del_certificado(self, cert_dict: dict):
        self.validar_certificado(cert_dict)
        return RSA.import_key(cert_dict["public_key"].encode())