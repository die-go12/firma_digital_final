Tests - Auditoría de Seguridad
Este directorio contiene los scripts de pruebas automatizadas diseñados para validar la integridad, funcionalidad y seguridad del sistema criptográfico.

Contenido
test_security_flow.py: Script de integración principal. Ejecuta una simulación completa de ataque y defensa para asegurar que la firma digital no sea vulnerada.

Cobertura de Pruebas
El script valida automáticamente los siguientes escenarios:

    Ciclo de Vida: Registro de usuario, generación de llaves encriptadas y firma de documentos.

    Soporte Multimedia: Verificación de integridad en PDFs que contienen texto e imágenes/datos binarios.

    Verificación Exitosa: Validación de documentos legítimos.

    Prueba de Integridad (Anti-Tampering):

        Simula la intervención de un "hacker" modificando el PDF firmado.
        Resultado: El sistema detecta la alteración de bits y rechaza la firma.


Cómo Ejecutar
Desde la carpeta raíz del proyecto (con el entorno virtual activo), ejecuta:
python -m pytest tests/test_security_flow.py -v -s


Interpretación de Resultados
    PASSED: El flujo es correcto y el sistema rechazó exitosamente los documentos alterados.

    FAILED: Fallo en la lógica criptográfica o vulnerabilidad detectada.