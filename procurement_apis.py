"""
procurement_apis.py
===================
Módulo principal que centraliza todas las mock APIs del sistema multi-agente.

USO EN AUTOGEN:
    from procurement_apis import TOOLS
    # Pasa TOOLS al agente correspondiente al crear sus function_map en AutoGen

ESTRUCTURA:
    api_proveedores.py  → Catálogo ERP (Procurement Agent)
    api_finance.py      → Presupuestos (Finance Agent)
    api_compliance.py   → Normativas (Compliance Agent)
    api_legal.py        → Contratos (Legal Agent)
    api_requester.py    → Solicitudes (Requester Agent)
    api_hil.py          → Escalación HiL (Orchestrator)
    casos_procurement.json → 50 casos de evaluación con ground truth
"""

import json
import os

# Importar todas las APIs
from api_proveedores import get_proveedor, registrar_proveedor, buscar_alternativas
from api_finance    import verificar_presupuesto, aprobar_gasto, proponer_reasignacion
from api_compliance import verificar_normativa, detectar_conflicto_interes
from api_legal      import validar_contrato, validar_nuevo_proveedor, verificar_nda
from api_requester  import crear_solicitud, actualizar_estado_solicitud, obtener_solicitud
from api_hil        import escalar_a_humano, simular_decision_humana, obtener_estadisticas_hil

# ──────────────────────────────────────────────────────────────
# MAPA DE HERRAMIENTAS POR AGENTE (para usar en AutoGen)
# ──────────────────────────────────────────────────────────────

TOOLS_REQUESTER = {
    "crear_solicitud":            crear_solicitud,
    "actualizar_estado_solicitud": actualizar_estado_solicitud,
    "obtener_solicitud":          obtener_solicitud,
}

TOOLS_PROCUREMENT = {
    "get_proveedor":        get_proveedor,
    "registrar_proveedor":  registrar_proveedor,
    "buscar_alternativas":  buscar_alternativas,
}

TOOLS_FINANCE = {
    "verificar_presupuesto":   verificar_presupuesto,
    "aprobar_gasto":           aprobar_gasto,
    "proponer_reasignacion":   proponer_reasignacion,
}

TOOLS_COMPLIANCE = {
    "verificar_normativa":       verificar_normativa,
    "detectar_conflicto_interes": detectar_conflicto_interes,
}

TOOLS_LEGAL = {
    "validar_contrato":          validar_contrato,
    "validar_nuevo_proveedor":   validar_nuevo_proveedor,
    "verificar_nda":             verificar_nda,
}

TOOLS_HIL = {
    "escalar_a_humano":        escalar_a_humano,
    "simular_decision_humana": simular_decision_humana,
    "obtener_estadisticas_hil": obtener_estadisticas_hil,
}

# Todas las herramientas (para el orquestador)
TOOLS_ALL = {
    **TOOLS_REQUESTER,
    **TOOLS_PROCUREMENT,
    **TOOLS_FINANCE,
    **TOOLS_COMPLIANCE,
    **TOOLS_LEGAL,
    **TOOLS_HIL,
}


def cargar_casos() -> list:
    """Carga los 50 casos de procurement desde el JSON."""
    ruta = os.path.join(os.path.dirname(__file__), "casos_procurement.json")
    with open(ruta, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["casos"]


def cargar_casos_por_nivel(nivel: str) -> list:
    """Filtra casos por nivel: 'Simple', 'Medio' o 'Complejo'."""
    return [c for c in cargar_casos() if c["nivel"] == nivel]


# ──────────────────────────────────────────────────────────────
# TEST RÁPIDO: ejecuta python procurement_apis.py para verificar
# ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("TEST DE MOCK APIs — Sistema Multi-Agente Procurement")
    print("=" * 60)

    print("\n[1] Proveedor aprobado (PRV-001):")
    r = get_proveedor("PRV-001")
    print(f"    Nombre: {r['nombre']} | Estado: {r['estado']} | Puede operar: {r['puede_operar']}")

    print("\n[2] Proveedor no aprobado (PRV-007):")
    r = get_proveedor("PRV-007")
    print(f"    Nombre: {r['nombre']} | Estado: {r['estado']} | Puede operar: {r['puede_operar']}")

    print("\n[3] Verificación presupuesto IT para 3.500€:")
    r = verificar_presupuesto("IT", 3500)
    print(f"    Disponible: {r['presupuesto_disponible']}€ | Aprobado: {r['aprobado']} | Nivel: {r['nivel_aprobacion_requerido']}")

    print("\n[4] Normativa para datos_personales desde US:")
    r = verificar_normativa("datos_personales", "US")
    print(f"    Cumple: {r['cumple_normativa']} | Riesgo: {r['nivel_riesgo']} | HiL: {r['requiere_escalacion_hil']}")

    print("\n[5] Contrato con cláusula de exclusividad por 5.000€:")
    r = validar_contrato("mantenimiento", ["exclusividad", "renovacion_automatica"], 5000, 12)
    print(f"    Puede firmar: {r['puede_firmar']} | Riesgo: {r['nivel_riesgo_global']} | Decision: {r['decision']}")

    print("\n[6] Conflicto de interés con PRV-012:")
    r = detectar_conflicto_interes("PRV-012", "Ana López")
    print(f"    Conflicto: {r['conflicto_detectado']} | Tipo: {r.get('tipo_conflicto','N/A')} | HiL: {r['accion_requerida']}")

    print("\n[7] Crear solicitud C01:")
    r = crear_solicitud("María García", "IT", "10 ratones USB", 150, "PRV-001")
    print(f"    ID: {r['solicitud_id']} | Estado: {r['estado']}")

    print("\n[8] Escalación HiL por conflicto de interés:")
    r = escalar_a_humano(
        solicitud_id="SOL-2026-001",
        razon="conflicto_interes",
        agente_que_escala="Compliance Agent",
        resumen="Compra de 20.000€ a empresa vinculada con Director de Compras.",
        opciones=["rechazar", "buscar_alternativa", "auditar"],
        recomendacion="buscar_alternativa"
    )
    print(f"    Escalacion ID: {r['escalacion_id']} | Asignado a: {r['asignado_a']} | SLA: {r['sla_respuesta_horas']}h")

    print("\n[9] Casos cargados por nivel:")
    casos = cargar_casos()
    niveles = {}
    for c in casos:
        niveles[c["nivel"]] = niveles.get(c["nivel"], 0) + 1
    for nivel, n in niveles.items():
        print(f"    {nivel}: {n} casos")

    print("\n" + "=" * 60)
    print("✅ Todas las APIs funcionan correctamente.")
    print("=" * 60)
