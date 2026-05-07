"""
API Mock: Escalación Human-in-the-Loop (HiL mock)
Agente que la usa: Orchestrator / cualquier agente que detecte que no puede resolver
Esta API es la más importante del sistema: registra cuándo el sistema
reconoce sus límites y escala correctamente al humano.
Para el artículo científico, la HiL Detection Accuracy (HDA) mide
si el sistema escala los casos correctos (ni de más ni de menos).
"""
import datetime

ESCALACIONES_DB = {}
_contador_escalaciones = 0

# Razones válidas de escalación (el agente debe identificar la correcta)
RAZONES_ESCALACION = {
    "conflicto_interes":         {"sla_horas": 2,  "asignado_a": "Director General",       "prioridad": "critica"},
    "incumplimiento_gdpr":       {"sla_horas": 4,  "asignado_a": "DPO (Data Protection)",   "prioridad": "alta"},
    "incumplimiento_normativa":  {"sla_horas": 8,  "asignado_a": "Director Compras",        "prioridad": "alta"},
    "importe_consejo":           {"sla_horas": 48, "asignado_a": "Consejo de Dirección",    "prioridad": "normal"},
    "importe_direccion":         {"sla_horas": 24, "asignado_a": "Director de área",        "prioridad": "normal"},
    "proveedor_sla_incumplido":  {"sla_horas": 12, "asignado_a": "Director Compras",        "prioridad": "media"},
    "clausula_critica_contrato": {"sla_horas": 8,  "asignado_a": "Asesoría Legal externa",  "prioridad": "alta"},
    "proyecto_estrategico":      {"sla_horas": 48, "asignado_a": "Comité de Dirección",     "prioridad": "alta"},
    "sin_resolver_agente":       {"sla_horas": 4,  "asignado_a": "Responsable Compras",     "prioridad": "media"},
}


def escalar_a_humano(solicitud_id: str, razon: str, agente_que_escala: str,
                     resumen: str, opciones: list, recomendacion: str,
                     contexto_adicional: dict = None) -> dict:
    """
    Escala un caso al humano con toda la información necesaria para decidir.

    Esta función es la medida de calidad del sistema:
    - Si escala cuando no debería → falso positivo (penaliza ARR)
    - Si no escala cuando debería → falso negativo (penaliza HDA)
    - Si escala con la razón correcta y contexto completo → HDA correcta

    Parámetros:
        solicitud_id:      ID de la solicitud de compra
        razon:             Categoría de la escalación (debe estar en RAZONES_ESCALACION)
        agente_que_escala: Nombre del agente que detectó la necesidad
        resumen:           Resumen ejecutivo del caso en lenguaje natural
        opciones:          Lista de opciones que el humano puede elegir
        recomendacion:     Opción que el sistema recomienda
        contexto_adicional: Datos extra relevantes para la decisión
    """
    global _contador_escalaciones
    _contador_escalaciones += 1
    escalacion_id = f"ESC-2026-{_contador_escalaciones:03d}"
    timestamp = datetime.datetime.now().isoformat()

    # Validar que la razón es conocida
    razon_valida = razon in RAZONES_ESCALACION
    config = RAZONES_ESCALACION.get(razon, RAZONES_ESCALACION["sin_resolver_agente"])

    escalacion = {
        "escalacion_id": escalacion_id,
        "solicitud_id": solicitud_id,
        "razon": razon,
        "razon_valida": razon_valida,
        "agente_que_escala": agente_que_escala,
        "asignado_a": config["asignado_a"],
        "prioridad": config["prioridad"],
        "sla_horas": config["sla_horas"],
        "resumen": resumen,
        "opciones_para_humano": opciones,
        "recomendacion_sistema": recomendacion,
        "contexto_adicional": contexto_adicional or {},
        "estado": "pendiente_humano",
        "timestamp_creacion": timestamp,
        "timestamp_limite": (
            datetime.datetime.now() + datetime.timedelta(hours=config["sla_horas"])
        ).isoformat()
    }

    ESCALACIONES_DB[escalacion_id] = escalacion

    return {
        "escalacion_id": escalacion_id,
        "solicitud_id": solicitud_id,
        "estado": "pendiente_humano",
        "asignado_a": config["asignado_a"],
        "prioridad": config["prioridad"],
        "sla_respuesta_horas": config["sla_horas"],
        "razon_valida": razon_valida,
        "mensaje": (
            f"Caso escalado correctamente a '{config['asignado_a']}'. "
            f"SLA de respuesta: {config['sla_horas']}h. "
            f"Prioridad: {config['prioridad'].upper()}."
        ),
        "timestamp": timestamp
    }


def simular_decision_humana(escalacion_id: str, decision: str, justificacion: str) -> dict:
    """
    Simula la respuesta del humano a una escalación.
    Se usa en el experimento para calcular métricas de forma automática.

    Decisiones posibles: "aprobar", "rechazar", "solicitar_mas_info",
                         "renegociar", "buscar_alternativa"
    """
    if escalacion_id not in ESCALACIONES_DB:
        return {"procesado": False, "mensaje": "Escalación no encontrada."}

    escalacion = ESCALACIONES_DB[escalacion_id]
    timestamp = datetime.datetime.now().isoformat()
    escalacion["estado"] = "resuelta_por_humano"
    escalacion["decision_humana"] = decision
    escalacion["justificacion_humana"] = justificacion
    escalacion["timestamp_resolucion"] = timestamp

    tiempo_resolucion = (
        datetime.datetime.fromisoformat(timestamp) -
        datetime.datetime.fromisoformat(escalacion["timestamp_creacion"])
    ).seconds / 3600  # en horas

    return {
        "escalacion_id": escalacion_id,
        "solicitud_id": escalacion["solicitud_id"],
        "decision": decision,
        "justificacion": justificacion,
        "tiempo_resolucion_horas": round(tiempo_resolucion, 2),
        "dentro_sla": tiempo_resolucion <= escalacion["sla_horas"],
        "timestamp": timestamp,
        "mensaje": f"Humano decidió: '{decision}'. El sistema retoma el proceso con esta decisión."
    }


def obtener_estadisticas_hil() -> dict:
    """
    Devuelve estadísticas de escalaciones para calcular la métrica HDA.
    Se usa al final del experimento para evaluar la calidad de detección.
    """
    total = len(ESCALACIONES_DB)
    resueltas = sum(1 for e in ESCALACIONES_DB.values() if e["estado"] == "resuelta_por_humano")
    pendientes = total - resueltas

    razones_usadas = {}
    for e in ESCALACIONES_DB.values():
        razones_usadas[e["razon"]] = razones_usadas.get(e["razon"], 0) + 1

    return {
        "total_escalaciones": total,
        "resueltas": resueltas,
        "pendientes": pendientes,
        "razones_mas_frecuentes": sorted(razones_usadas.items(), key=lambda x: x[1], reverse=True),
        "mensaje": f"{total} escalaciones registradas. {resueltas} resueltas por humano."
    }
