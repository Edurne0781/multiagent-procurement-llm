"""
API Mock: Base Regulatoria (Compliance mock)
Agente que la usa: Compliance Agent
Simula la consulta a una base de normativas aplicables.
"""

# Países con adecuación GDPR reconocida por la UE
PAISES_ADECUACION_GDPR = [
    "ES", "DE", "FR", "IT", "PT", "NL", "BE", "AT", "SE", "FI",
    "DK", "NO", "IS", "LI", "CH", "UK", "CA", "JP", "KR", "NZ", "AR"
]

# Normativas por categoría de compra
NORMATIVAS = {
    "datos_personales": {
        "nombre": "GDPR (Reglamento General de Protección de Datos)",
        "referencia": "Reglamento UE 2016/679",
        "requisitos": ["proveedor_en_pais_adecuacion", "clausulas_contractuales_tipo", "dpa_firmado"],
        "riesgo_incumplimiento": "multa hasta 20M€ o 4% facturación global"
    },
    "equipos_electronicos": {
        "nombre": "Directiva CE / Marcado CE",
        "referencia": "Directiva 2014/30/UE + 2014/35/UE",
        "requisitos": ["marcado_ce", "declaracion_conformidad", "proveedor_autorizado_ue"],
        "riesgo_incumplimiento": "retirada del mercado, responsabilidad civil"
    },
    "productos_quimicos": {
        "nombre": "Reglamento REACH + PRL",
        "referencia": "Reglamento CE 1907/2006 + Ley 31/1995",
        "requisitos": ["ficha_seguridad_sds", "registro_reach", "formacion_manipulacion"],
        "riesgo_incumplimiento": "sanción hasta 500.000€, responsabilidad penal"
    },
    "equipos_medicos": {
        "nombre": "Reglamento Productos Sanitarios",
        "referencia": "Reglamento UE 2017/745",
        "requisitos": ["marcado_ce_sanitario", "homologacion_aemps", "udi_registrado"],
        "riesgo_incumplimiento": "prohibición de uso, sanción grave"
    },
    "drones_aeronaves": {
        "nombre": "Normativa AESA / EASA",
        "referencia": "Reglamento UE 2019/945 + 2019/947",
        "requisitos": ["licencia_operador_registrado", "seguro_obligatorio", "categoria_operacion"],
        "riesgo_incumplimiento": "sanción hasta 225.000€, responsabilidad penal"
    },
    "software_vigilancia": {
        "nombre": "Normativa privacidad laboral + GDPR",
        "referencia": "Art. 87 LOPDGDD + GDPR Art. 6",
        "requisitos": ["informacion_previa_trabajadores", "base_juridica_legitima", "evaluacion_impacto"],
        "riesgo_incumplimiento": "infracción grave AEPD, hasta 300.000€"
    },
    "estandar": {
        "nombre": "Sin normativa especial aplicable",
        "referencia": "N/A",
        "requisitos": [],
        "riesgo_incumplimiento": "ninguno específico"
    }
}


def verificar_normativa(categoria_compra: str, pais_proveedor: str,
                         tiene_certificacion: bool = False,
                         documentos_aportados: list = None) -> dict:
    """
    Verifica si una compra cumple la normativa aplicable.
    Devuelve nivel de riesgo y acción requerida.
    """
    if documentos_aportados is None:
        documentos_aportados = []

    normativa = NORMATIVAS.get(categoria_compra, NORMATIVAS["estandar"])
    requisitos = normativa["requisitos"]

    # Comprobaciones específicas
    incumplimientos = []

    if "proveedor_en_pais_adecuacion" in requisitos:
        if pais_proveedor not in PAISES_ADECUACION_GDPR:
            incumplimientos.append({
                "requisito": "proveedor_en_pais_adecuacion",
                "estado": "INCUMPLE",
                "detalle": f"País '{pais_proveedor}' sin adecuación GDPR reconocida por la UE.",
                "solucion": "Firmar Cláusulas Contractuales Tipo (CCT) de la Comisión Europea."
            })

    if "marcado_ce" in requisitos and not tiene_certificacion:
        incumplimientos.append({
            "requisito": "marcado_ce",
            "estado": "INCUMPLE",
            "detalle": "Equipo sin certificación CE verificada.",
            "solucion": "Solicitar declaración de conformidad CE al proveedor o buscar alternativa certificada."
        })

    if "ficha_seguridad_sds" in requisitos and "sds" not in documentos_aportados:
        incumplimientos.append({
            "requisito": "ficha_seguridad_sds",
            "estado": "INCUMPLE",
            "detalle": "No se ha aportado ficha de datos de seguridad (SDS).",
            "solucion": "Solicitar ficha SDS al proveedor antes de aprobar la compra."
        })

    if "homologacion_aemps" in requisitos and not tiene_certificacion:
        incumplimientos.append({
            "requisito": "homologacion_aemps",
            "estado": "INCUMPLE",
            "detalle": "Equipo médico sin homologación AEMPS.",
            "solucion": "Acreditar registro en AEMPS antes de adquisición."
        })

    if "licencia_operador_registrado" in requisitos and "licencia" not in documentos_aportados:
        incumplimientos.append({
            "requisito": "licencia_operador_registrado",
            "estado": "INCUMPLE",
            "detalle": "No se dispone de licencia de operador AESA registrada.",
            "solucion": "Registrarse como operador en AESA antes de operar drones."
        })

    if "informacion_previa_trabajadores" in requisitos and "inform_trabajadores" not in documentos_aportados:
        incumplimientos.append({
            "requisito": "informacion_previa_trabajadores",
            "estado": "INCUMPLE",
            "detalle": "Trabajadores no informados sobre sistema de vigilancia.",
            "solucion": "Informar previamente a empleados y representantes legales."
        })

    # Calcular nivel de riesgo
    if len(incumplimientos) == 0:
        nivel_riesgo = "bajo"
        cumple = True
        accion = "aprobacion_directa"
    elif len(incumplimientos) == 1:
        nivel_riesgo = "medio"
        cumple = False
        accion = "subsanar_y_reenviar"
    else:
        nivel_riesgo = "alto"
        cumple = False
        accion = "bloqueo_hasta_subsanacion"

    return {
        "categoria_compra": categoria_compra,
        "normativa_aplicable": normativa["nombre"],
        "referencia_legal": normativa["referencia"],
        "pais_proveedor": pais_proveedor,
        "cumple_normativa": cumple,
        "nivel_riesgo": nivel_riesgo,
        "incumplimientos": incumplimientos,
        "num_incumplimientos": len(incumplimientos),
        "accion_requerida": accion,
        "riesgo_incumplimiento": normativa["riesgo_incumplimiento"],
        "requiere_escalacion_hil": nivel_riesgo == "alto"
    }


def detectar_conflicto_interes(proveedor_id: str, solicitante: str) -> dict:
    """
    Detecta si existe conflicto de interés entre el solicitante y el proveedor.
    """
    # Simulación de vínculos conocidos
    vinculos = {
        "PRV-012": {"persona_vinculada": "Director Compras", "tipo": "vinculo_familiar"},
    }

    if proveedor_id in vinculos:
        vinculo = vinculos[proveedor_id]
        return {
            "conflicto_detectado": True,
            "proveedor_id": proveedor_id,
            "tipo_conflicto": vinculo["tipo"],
            "persona_vinculada": vinculo["persona_vinculada"],
            "solicitante": solicitante,
            "nivel_riesgo": "critico",
            "accion_requerida": "escalacion_obligatoria_hil",
            "mensaje": (
                f"ALERTA: Conflicto de interés detectado. El proveedor está vinculado con "
                f"'{vinculo['persona_vinculada']}'. Escalación HiL obligatoria."
            )
        }

    return {
        "conflicto_detectado": False,
        "proveedor_id": proveedor_id,
        "solicitante": solicitante,
        "nivel_riesgo": "bajo",
        "mensaje": "No se detectaron conflictos de interés."
    }
