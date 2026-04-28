"""
API Mock: Validación Contractual (Legal mock)
Agente que la usa: Legal Agent
Simula el análisis de contratos y validación de nuevos proveedores.
"""

# Cláusulas con riesgo conocido
CLAUSULAS_RIESGO = {
    "exclusividad": {
        "nivel": "alto",
        "descripcion": "Obliga a la empresa a comprar únicamente a este proveedor.",
        "recomendacion": "Eliminar o limitar a categoría/periodo específico."
    },
    "renovacion_automatica": {
        "nivel": "medio",
        "descripcion": "El contrato se renueva automáticamente sin aviso.",
        "recomendacion": "Añadir cláusula de preaviso mínimo de 90 días para no renovación."
    },
    "penalizacion_salida": {
        "nivel": "alto",
        "descripcion": "Penalización elevada por resolución anticipada del contrato.",
        "recomendacion": "Negociar reducción de penalización o establecer causas de resolución sin penalización."
    },
    "cesion_ip": {
        "nivel": "critico",
        "descripcion": "El proveedor retiene derechos de propiedad intelectual sobre el trabajo entregado.",
        "recomendacion": "Modificar para que toda IP generada sea propiedad de la empresa."
    },
    "limitacion_responsabilidad_baja": {
        "nivel": "alto",
        "descripcion": "El proveedor limita su responsabilidad a una cantidad insuficiente.",
        "recomendacion": "Negociar límite de responsabilidad equivalente al valor del contrato."
    },
    "arbitraje_extranjero": {
        "nivel": "medio",
        "descripcion": "Disputas sometidas a arbitraje en jurisdicción extranjera.",
        "recomendacion": "Cambiar a arbitraje en España o tribunales españoles."
    },
    "confidencialidad_indefinida": {
        "nivel": "bajo",
        "descripcion": "Obligación de confidencialidad sin límite temporal.",
        "recomendacion": "Estándar aceptable; revisar que sea recíproca."
    },
    "garantia_estandar": {
        "nivel": "bajo",
        "descripcion": "Garantía dentro de los términos habituales del mercado.",
        "recomendacion": "Aceptable. Documentar condiciones de activación."
    },
}

# Documentos requeridos según tipo de proveedor
DOCS_REQUERIDOS = {
    "nuevo_proveedor_estandar": ["NIF_CIF", "alta_IAE", "certificado_SS_corriente"],
    "nuevo_proveedor_servicio": ["NIF_CIF", "alta_IAE", "certificado_SS_corriente", "NDA", "seguro_RC"],
    "nuevo_proveedor_datos":    ["NIF_CIF", "alta_IAE", "NDA", "DPA", "clausulas_contractuales_tipo"],
    "nuevo_proveedor_critico":  ["NIF_CIF", "alta_IAE", "certificado_SS_corriente", "NDA", "seguro_RC", "auditoria_seguridad"],
    "proveedor_aprobado":       [],  # Ya validado previamente
}


def validar_contrato(tipo_contrato: str, clausulas: list, importe: float, duracion_meses: int) -> dict:
    """
    Analiza las cláusulas contractuales y devuelve riesgos y recomendaciones.
    """
    clausulas_problematicas = []
    nivel_riesgo_global = "bajo"

    for clausula in clausulas:
        if clausula in CLAUSULAS_RIESGO:
            info = CLAUSULAS_RIESGO[clausula]
            clausulas_problematicas.append({
                "clausula": clausula,
                "nivel_riesgo": info["nivel"],
                "descripcion": info["descripcion"],
                "recomendacion": info["recomendacion"]
            })
            # Escalar el nivel de riesgo global
            if info["nivel"] == "critico":
                nivel_riesgo_global = "critico"
            elif info["nivel"] == "alto" and nivel_riesgo_global != "critico":
                nivel_riesgo_global = "alto"
            elif info["nivel"] == "medio" and nivel_riesgo_global == "bajo":
                nivel_riesgo_global = "medio"

    # Alertas adicionales por importe y duración
    alertas_adicionales = []
    if importe > 10000 and duracion_meses > 12:
        alertas_adicionales.append("Contrato de alto valor y larga duración: requiere aprobación de dirección.")
    if importe > 50000:
        alertas_adicionales.append("Importe superior a 50.000€: requiere proceso de licitación o aprobación de consejo.")

    # Decisión final
    if nivel_riesgo_global in ["critico", "alto"]:
        decision = "revision_obligatoria"
        puede_firmar = False
        mensaje = "Contrato con cláusulas de riesgo alto/crítico. No firmar hasta revisión y negociación."
    elif nivel_riesgo_global == "medio":
        decision = "revision_recomendada"
        puede_firmar = True
        mensaje = "Contrato con riesgos moderados. Se recomienda negociar mejoras antes de firmar."
    else:
        decision = "apto_para_firma"
        puede_firmar = True
        mensaje = "Contrato sin cláusulas problemáticas significativas. Apto para firma."

    return {
        "tipo_contrato": tipo_contrato,
        "importe": importe,
        "duracion_meses": duracion_meses,
        "clausulas_analizadas": clausulas,
        "clausulas_problematicas": clausulas_problematicas,
        "num_problemas": len(clausulas_problematicas),
        "nivel_riesgo_global": nivel_riesgo_global,
        "decision": decision,
        "puede_firmar": puede_firmar,
        "alertas_adicionales": alertas_adicionales,
        "mensaje": mensaje,
        "requiere_escalacion_hil": nivel_riesgo_global == "critico" or importe > 50000
    }


def validar_nuevo_proveedor(tipo_proveedor: str, documentos_aportados: list,
                             pais: str, sector: str) -> dict:
    """
    Valida si un nuevo proveedor aporta toda la documentación requerida
    para ser registrado en el sistema.
    """
    docs_requeridos = DOCS_REQUERIDOS.get(tipo_proveedor, DOCS_REQUERIDOS["nuevo_proveedor_estandar"])
    docs_faltantes = [d for d in docs_requeridos if d not in documentos_aportados]

    puede_aprobar = len(docs_faltantes) == 0

    # Requisitos adicionales por país
    alertas_pais = []
    if pais not in ["ES", "DE", "FR", "IT", "PT", "NL", "BE", "AT"]:
        alertas_pais.append(f"Proveedor de país '{pais}': verificar normativa de importación y GDPR.")

    return {
        "tipo_proveedor": tipo_proveedor,
        "pais": pais,
        "sector": sector,
        "documentos_requeridos": docs_requeridos,
        "documentos_aportados": documentos_aportados,
        "documentos_faltantes": docs_faltantes,
        "puede_aprobar": puede_aprobar,
        "alertas_pais": alertas_pais,
        "estado_resultante": "aprobado" if puede_aprobar else "pendiente_documentacion",
        "mensaje": (
            "Proveedor validado. Puede ser registrado como aprobado."
            if puede_aprobar else
            f"Faltan {len(docs_faltantes)} documento(s): {', '.join(docs_faltantes)}. No se puede aprobar hasta recibirlos."
        )
    }


def verificar_nda(proveedor_id: str, tipo_informacion: str) -> dict:
    """
    Verifica si existe NDA firmado con un proveedor para un tipo de información.
    """
    # Simulación: algunos proveedores tienen NDA, otros no
    ndas_activos = {
        "PRV-003": ["codigo_fuente", "datos_clientes", "estrategia"],
        "PRV-005": ["datos_clientes", "infraestructura"],
    }

    ndas_proveedor = ndas_activos.get(proveedor_id, [])
    tiene_nda = tipo_informacion in ndas_proveedor or "todos" in ndas_proveedor

    return {
        "proveedor_id": proveedor_id,
        "tipo_informacion": tipo_informacion,
        "nda_activo": tiene_nda,
        "coberturas_nda": ndas_proveedor,
        "accion_requerida": "ninguna" if tiene_nda else "firmar_nda_antes_de_compartir",
        "mensaje": (
            f"NDA activo para '{tipo_informacion}'. Puede compartirse información."
            if tiene_nda else
            f"No hay NDA para '{tipo_informacion}' con este proveedor. Firmar antes de proceder."
        )
    }
