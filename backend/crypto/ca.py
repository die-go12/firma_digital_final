import os
import json
from datetime import datetime, timedelta
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

#CONFIGURACION
CERTS_PATH = "storage/certs"
CA_PRIVATE_KEY = f"{CERTS_PATH}/ca_private.pem"
CA_PUBLIC_KEY = f"{CERTS_PATH}/ca_public.pem"

class CertificadoInvalido(Exception):
    """Excepción personalizada para fallos de validación"""
    pass

class AutoridadCertificadora:
    """
    Clase principal que maneja TANTO la emisión COMO la validación de certificados.
    Actúa como la autoridad central del sistema.
    """
    def __init__(self):
        # Aseguramos carpetas
        os.makedirs(CERTS_PATH, exist_ok=True)
        
        # Generar llaves maestras si no existen
        if not os.path.exists(CA_PRIVATE_KEY):
            self._crear_llaves_ca()

        # Cargar llave PRIVADA (para firmar nuevos certificados)
        with open(CA_PRIVATE_KEY, "rb") as f:
            self.private_key = RSA.import_key(f.read())
        
        # Cargar llave PÚBLICA (para verificar certificados existentes)
        with open(CA_PUBLIC_KEY, "rb") as f:
            self.public_key = RSA.import_key(f.read())

    def _crear_llaves_ca(self):
        """Genera llaves RSA maestras (Solo se ejecuta la primera vez)"""
        print(" Generando nuevas llaves maestras para la CA...")
        key = RSA.generate(2048)
        with open(CA_PRIVATE_KEY, "wb") as f: f.write(key.export_key())
        with open(CA_PUBLIC_KEY, "wb") as f: f.write(key.publickey().export_key())

    #EMISIÓN 
    
    def emitir_certificado(self, nombre_usuario: str, public_key_str: str) -> dict:
        """Genera un certificado firmado y retorna el diccionario (JSON)."""
        certificado = {
            "subject": nombre_usuario,
            "public_key": public_key_str,
            "issuer": "CA-Simulada-Backend",
            "valid_from": datetime.utcnow().isoformat(),
            "valid_to": (datetime.utcnow() + timedelta(days=365)).isoformat(),
            "serial_number": int(datetime.utcnow().timestamp())
        }

        # Firmar
        payload_bytes = json.dumps(certificado, sort_keys=True).encode('utf-8')
        h = SHA256.new(payload_bytes)
        firma = pkcs1_15.new(self.private_key).sign(h)
        
        certificado["firma_ca"] = firma.hex()
        return certificado

    # VALIDACIÓN 

    def validar_certificado(self, cert_dict: dict) -> bool:
        """
        Verifica que el certificado no haya sido alterado y esté vigente.
        """
        # A. Validar fechas
        ahora = datetime.utcnow().isoformat()
        if not (cert_dict["valid_from"] <= ahora <= cert_dict["valid_to"]):
            raise CertificadoInvalido("El certificado ha expirado o aún no es válido.")

        # B. Validar firma de la CA
        firma_hex = cert_dict.get("firma_ca")
        if not firma_hex:
            raise CertificadoInvalido("El certificado no tiene firma.")
            
        firma = bytes.fromhex(firma_hex)

        # Copia del certificado SIN la firma (para recalcular el hash original)
        cert_sin_firma = cert_dict.copy()
        del cert_sin_firma["firma_ca"]

        h = SHA256.new(json.dumps(cert_sin_firma, sort_keys=True).encode())

        try:
            # Usamos la llave PÚBLICA de la CA para verificar
            pkcs1_15.new(self.public_key).verify(h, firma)
        except (ValueError, TypeError):
            raise CertificadoInvalido("Firma digital del certificado INVÁLIDA. El certificado ha sido adulterado.")

        return True

    def obtener_public_key_del_certificado(self, cert_dict: dict):
        """Extrae el objeto RSA key del certificado validado"""
        self.validar_certificado(cert_dict) # Validar antes de entregar
        return RSA.import_key(cert_dict["public_key"].encode())