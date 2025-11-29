/* frontend/js/api.js */

// ⚠️ IMPORTANTE: Asegúrate de que este puerto coincida con tu terminal Backend (8000 o 8001)
const API_URL = "http://127.0.0.1:8000";

async function handleResponse(response) {
    if (!response.ok) {
        // Intentamos leer el JSON de error del backend
        let errorMsg = "Error desconocido";
        try {
            const errorData = await response.json();
            // Si es un error de validación (400/422), mostramos el detalle
            // Si es un error del servidor (500), ocultamos el detalle técnico por seguridad
            if (response.status >= 500) {
                errorMsg = "Error interno del servidor. Intente más tarde.";
            } else {
                errorMsg = errorData.detail || JSON.stringify(errorData);
            }
        } catch (e) {
            errorMsg = `Error HTTP ${response.status}`;
        }
        throw new Error(errorMsg);
    }
    
    // Si la respuesta es un archivo (Blob), lo devolvemos tal cual
    const contentType = response.headers.get("content-type");
    if (contentType && contentType.includes("application/octet-stream")) {
        return response.blob();
    }
    
    return response.json();
}

// Envoltorio seguro para fetch que atrapa errores de "servidor apagado"
async function safeFetch(url, options) {
    try {
        const response = await fetch(url, options);
        return handleResponse(response);
    } catch (error) {
        if (error.message === "Failed to fetch") {
            throw new Error("No se pudo conectar con el servidor. Verifica que el Backend esté corriendo y el puerto sea correcto.");
        }
        throw error;
    }
}

export async function crearUsuario(nombre, email) {
    return safeFetch(`${API_URL}/usuarios/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre, email })
    });
}

export async function emitirCertificado(usuarioId) {
    return safeFetch(`${API_URL}/emitir-certificado/?usuario_id=${usuarioId}`, {
        method: 'POST'
    });
}

export async function firmarPDF(usuarioId, file) {
    const formData = new FormData();
    formData.append('usuario_id', usuarioId);
    formData.append('archivo', file);

    return safeFetch(`${API_URL}/firmar-pdf/`, {
        method: 'POST',
        body: formData
    });
}

export async function verificarFirma(usuarioId, archivoOriginal, archivoFirma) {
    const formData = new FormData();
    formData.append('usuario_id', usuarioId);
    formData.append('archivo_original', archivoOriginal);
    formData.append('archivo_firma', archivoFirma);

    return safeFetch(`${API_URL}/verificar-firma/`, {
        method: 'POST',
        body: formData
    });
}
///////////////////////////////////////////////////////////////////////////////////////////////////////////

/* --- AGREGAR AL FINAL DE api.js (FUERA DE OTRAS FUNCIONES) --- */

export async function verificarFirmaExterna(archivoOriginal, archivoFirma, archivoLlavePublica) {
    const formData = new FormData();
    formData.append('archivo_original', archivoOriginal);
    formData.append('archivo_firma', archivoFirma);
    formData.append('archivo_llave_publica', archivoLlavePublica); 

    // Opción segura: Usamos (+) en lugar de backticks para evitar errores de sintaxis
    const url = API_URL + "/verificar-externo/";

    return safeFetch(url, {
        method: 'POST',
        body: formData
    });
}
