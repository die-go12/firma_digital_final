#  Módulo de Criptografía

Este directorio contiene el núcleo lógico de seguridad del proyecto. Aquí residen las implementaciones matemáticas de los algoritmos RSA y SHA-256.

## Archivos del Módulo

* **`keygen.py`**: Generación de pares de llaves RSA (2048 bits).
* **`signer.py`**: Lógica de firma digital. Calcula el hash SHA-256 del documento y lo encripta con la llave privada (previamente desencriptada usando Sal+Pimienta).
* **`verifier.py`**: Lógica de verificación. Desencripta la firma con la llave pública y compara hashes para garantizar integridad.
* **`ca.py`**: Simulador de Autoridad Certificadora (CA). Emite certificados firmados localmente.

##  Librerías
Utiliza `PyCryptodome` para operaciones de bajo nivel.