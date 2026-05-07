"""
API Mock: Formulario de Solicitud (Requester mock)
Agente que la usa: Requester Agent
Registra y gestiona las solicitudes de compra entrantes.
"""
import datetime

# Simulación de base de datos de solicitudes
SOLICITUDES_DB = {}
_contador_solicitudes = 0


def crear_solicitud(solicitante: str, departamento: str, descripcion: str,
                    importe: float, proveedor_id: str = None,
                    urgente: bool = False, categoria_compra: str = "estandar") -> dict:
    """
    Registra una nueva solicitud de compra con todos sus metadatos.
    Devuelve un ID único y el estado inicial.
    """
    global _contador_solicitudes
    _contador_solicitudes += 1
    solicitud_id = f"SOL-2026-{_contador_solicitudes:03d}"
    timestamp = datetime.datetime.now().isoformat()

    solicitud = {
        "solicitud_id": solicitud_id,
        "solicitante": solicitante,
        "departamento": departamento,
        "descripcion": descripcion,
        "importe": importe,
        "proveedor_id": proveedor_id,
        "urgente": urgente,
        "categoria_compra": categoria_compra,
        "estado": "pendiente_validacion",
        "timestamp_creacion": timestamp,
        "historial": [
            {"accion": "creacion", "timestamp": timestamp, "actor": "Requester Agent"}
        ]
    }

    SOLICITUDES_DB[solicitud_id] = solicitud

    return {
        "solicitud_id": solicitud_id,
        "estado": "pendiente_validacion",
        "urgente": urgente,
        "mensaje": f"Solicitud {solicitud_id} registrada correctamente. Iniciando proceso de validación.",
        "siguiente_paso": "validacion_proveedor_y_presupuesto",
        "timestamp": timestamp
    }


def actualizar_estado_solicitud(solicitud_id: str, nuevo_estado: str, actor: str, comentario: str = "") -> dict:
    """
    Actualiza el estado de una solicitud y registra el cambio en el historial.
    Estados posibles: pendiente_validacion, en_revision_legal, en_revision_compliance,
                      pendiente_aprobacion_finance, aprobada, rechazada, escalada_hil.
    """
    if solicitud_id not in SOLICITUDES_DB:
        return {"actualizado": False, "mensaje": f"Solicitud {solicitud_id} no encontrada."}

    solicitud = SOLICITUDES_DB[solicitud_id]
    estado_anterior = solicitud["estado"]
    solicitud["estado"] = nuevo_estado
    timestamp = datetime.datetime.now().isoformat()
    solicitud["historial"].append({
        "accion": f"cambio_estado: {estado_anterior} -> {nuevo_estado}",
        "timestamp": timestamp,
        "actor": actor,
        "comentario": comentario
    })

    return {
        "actualizado": True,
        "solicitud_id": solicitud_id,
        "estado_anterior": estado_anterior,
        "estado_nuevo": nuevo_estado,
        "actor": actor,
        "timestamp": timestamp,
        "mensaje": f"Estado actualizado a '{nuevo_estado}' por {actor}."
    }


def obtener_solicitud(solicitud_id: str) -> dict:
    """
    Devuelve el detalle completo de una solicitud y su historial.
    """
    if solicitud_id not in SOLICITUDES_DB:
        return {"encontrada": False, "mensaje": f"Solicitud {solicitud_id} no encontrada."}

    sol = SOLICITUDES_DB[solicitud_id]
    return {"encontrada": True, **sol}
