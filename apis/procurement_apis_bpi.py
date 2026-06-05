"""
procurement_apis_bpi.py
=======================
Módulo principal adaptado para BPI Challenge 2019.

Reemplaza procurement_apis.py usando datos reales del BPI Challenge 2019
(Purchase-to-Pay, empresa multinacional holandesa, ~251.734 casos).

Fuente: BPI Challenge 2019, Boudewijn van Dongen, TU/e
DOI: 10.4121/uuid:d06aff4b-79f0-45e6-8ec8-e19730c248f1
Licencia: CC BY 4.0

DIFERENCIAS vs versión mock original:
- Proveedores: IDs reales anonimizados del BPI (vendorID_XXXX)
- Umbrales financieros: basados en estadísticas reales del dataset
  (media=4.111€, P75=2.109€, max=8.833.459€)
- Categorías normativas: 3-way match, Consignment, 2-way match del BPI
- Actividades de riesgo: extraídas del event log real (Cancel, Change, Delete)
- Dataset de evaluación: 50 casos muestreados del BPI con ground truth

VALIDEZ EXTERNA:
Las APIs siguen siendo simuladas (no conectan a SAP/ERP real) pero
están parametrizadas con datos estadísticos y patrones reales del BPI 2019,
lo que incrementa la validez ecológica del experimento.
"""

import json
import os

# Importar APIs parametrizadas con BPI
from api_proveedores_bpi import get_proveedor, registrar_proveedor, buscar_alternativas
from api_finance_bpi import verificar_presupuesto, aprobar_gasto, proponer_reasignacion
from api_compliance_bpi import verificar_normativa, detectar_conflicto_interes

# Mantener APIs originales que no dependen del dataset
from api_legal import validar_contrato, validar_nuevo_proveedor, verificar_nda
from api_requester import crear_solicitud, actualizar_estado_solicitud, obtener_solicitud
from api_hil import escalar_a_humano, simular_decision_humana, obtener_estadisticas_hil

# ── Mapa de herramientas por agente ───────────────────────────

TOOLS_REQUESTER = {
    "crear_solicitud": crear_solicitud,
    "actualizar_estado_solicitud": actualizar_estado_solicitud,
    "obtener_solicitud": obtener_solicitud,
}

TOOLS_PROCUREMENT = {
    "get_proveedor": get_proveedor,
    "registrar_proveedor": registrar_proveedor,
    "buscar_alternativas": buscar_alternativas,
}

TOOLS_FINANCE = {
    "verificar_presupuesto": verificar_presupuesto,
    "aprobar_gasto": aprobar_gasto,
    "proponer_reasignacion": proponer_reasignacion,
}

TOOLS_COMPLIANCE = {
    "verificar_normativa": verificar_normativa,
    "detectar_conflicto_interes": detectar_conflicto_interes,
}

TOOLS_LEGAL = {
    "validar_contrato": validar_contrato,
    "validar_nuevo_proveedor": validar_nuevo_proveedor,
    "verificar_nda": verificar_nda,
}

TOOLS_HIL = {
    "escalar_a_humano": escalar_a_humano,
    "simular_decision_humana": simular_decision_humana,
    "obtener_estadisticas_hil": obtener_estadisticas_hil,
}

TOOLS_ALL = {
    **TOOLS_REQUESTER,
    **TOOLS_PROCUREMENT,
    **TOOLS_FINANCE,
    **TOOLS_COMPLIANCE,
    **TOOLS_LEGAL,
    **TOOLS_HIL,
}


def cargar_casos_bpi(ruta: str = "casos_bpi_2019.json") -> list:
    """
    Carga los 50 casos muestreados del BPI Challenge 2019.
    
    Formato de cada caso:
    {
        "id": "BPI_01",
        "caso_real": "4507032049_00010",     # ID real del BPI
        "descripcion": "Solicitud Standard PO por 3683.00 EUR",
        "proveedor": "vendorID_XXXX",         # Proveedor real anonimizado
        "importe": 3683.0,                    # Importe real en EUR
        "tipo_documento": "Standard PO",      # Tipo real del BPI
        "categoria": "3-way match, ...",      # Categoría real del BPI
        "actividades_reales": [...],          # Event log real del caso
        "complejidad": "Simple/Medio/Complejo",
        "requiere_hil": True/False            # Ground truth derivado del BPI
    }
    """
    ruta_abs = os.path.join(os.path.dirname(__file__), ruta)
    if not os.path.exists(ruta_abs):
        ruta_abs = ruta  # fallback a ruta relativa
    with open(ruta_abs, "r", encoding="utf-8") as f:
        return json.load(f)


def cargar_casos_por_nivel(nivel: str) -> list:
    """Filtra casos BPI por nivel de complejidad."""
    return [c for c in cargar_casos_bpi() if c["complejidad"] == nivel]


def get_estadisticas_dataset() -> dict:
    """Devuelve estadísticas del dataset BPI 2019 usado."""
    casos = cargar_casos_bpi()
    importes = [c["importe"] for c in casos]
    return {
        "fuente": "BPI Challenge 2019",
        "doi": "10.4121/uuid:d06aff4b-79f0-45e6-8ec8-e19730c248f1",
        "licencia": "CC BY 4.0",
        "total_casos_bpi": 251734,
        "casos_evaluacion": len(casos),
        "distribucion": {
            "Simple": len([c for c in casos if c["complejidad"] == "Simple"]),
            "Medio": len([c for c in casos if c["complejidad"] == "Medio"]),
            "Complejo": len([c for c in casos if c["complejidad"] == "Complejo"])
        },
        "casos_hil": sum(1 for c in casos if c["requiere_hil"]),
        "importe_medio": sum(importes) / len(importes),
        "importe_max": max(importes),
        "tipos_documento": list(set(c["tipo_documento"] for c in casos)),
        "categorias": list(set(c["categoria"] for c in casos))
    }


if __name__ == "__main__":
    print("=" * 60)
    print("TEST APIs BPI Challenge 2019")
    print("=" * 60)

    print("\n[1] Estadísticas del dataset:")
    stats = get_estadisticas_dataset()
    for k, v in stats.items():
        print(f"    {k}: {v}")

    print("\n[2] Proveedor BPI (vendorID_0226):")
    r = get_proveedor("vendorID_0226")
    print(f"    Estado: {r['estado']} | Puede operar: {r['puede_operar']}")

    print("\n[3] Presupuesto Standard PO 3683 EUR:")
    r = verificar_presupuesto("OPEX", 3683.0, "Standard PO")
    print(f"    Aprobado: {r['aprobado']} | Nivel: {r['nivel_aprobacion_requerido']}")

    print("\n[4] Compliance Consignment:")
    r = verificar_normativa("Consignment", True, [], 0)
    print(f"    Cumple: {r['cumple_normativa']} | Riesgo: {r['nivel_riesgo']} | HiL: {r['requiere_escalacion_hil']}")

    print("\n[5] Casos BPI cargados:")
    casos = cargar_casos_bpi()
    niveles = {}
    for c in casos:
        niveles[c["complejidad"]] = niveles.get(c["complejidad"], 0) + 1
    for nivel, n in niveles.items():
        print(f"    {nivel}: {n} casos")
    hil = sum(1 for c in casos if c["requiere_hil"])
    print(f"    Requieren HiL: {hil}")

    print("\n✅ APIs BPI Challenge 2019 funcionan correctamente.")
    print("=" * 60)
