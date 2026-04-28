"""
API Mock: Catálogo de Proveedores (ERP mock)
Agente que la usa: Procurement Agent
Simula la consulta a un ERP de gestión de proveedores.
"""

PROVEEDORES_DB = {
    "PRV-001": {"nombre": "TechSupply SL",        "estado": "aprobado",     "limite_credito": 5000,  "categorias": ["IT", "hardware"],        "pais": "ES"},
    "PRV-002": {"nombre": "OfiPaper SAU",          "estado": "aprobado",     "limite_credito": 2000,  "categorias": ["oficina", "consumibles"], "pais": "ES"},
    "PRV-003": {"nombre": "CloudSoft Europe",      "estado": "aprobado",     "limite_credito": 20000, "categorias": ["software", "licencias"], "pais": "IE"},
    "PRV-004": {"nombre": "ErgoMobel GmbH",        "estado": "aprobado",     "limite_credito": 8000,  "categorias": ["mobiliario", "oficina"],  "pais": "DE"},
    "PRV-005": {"nombre": "SecurityPro SL",        "estado": "aprobado",     "limite_credito": 50000, "categorias": ["seguridad", "IT"],        "pais": "ES"},
    "PRV-006": {"nombre": "CateringPlus SL",       "estado": "no_aprobado",  "limite_credito": 0,     "categorias": ["catering"],              "pais": "ES"},
    "PRV-007": {"nombre": "DesignAgency freelance","estado": "no_aprobado",  "limite_credito": 0,     "categorias": ["diseño", "marketing"],   "pais": "ES"},
    "PRV-008": {"nombre": "DataProc US LLC",       "estado": "no_aprobado",  "limite_credito": 0,     "categorias": ["datos", "cloud"],         "pais": "US"},
    "PRV-009": {"nombre": "QuickFix Urgencias SL", "estado": "no_aprobado",  "limite_credito": 0,     "categorias": ["mantenimiento", "IT"],    "pais": "ES"},
    "PRV-010": {"nombre": "MedEquip SA",           "estado": "no_aprobado",  "limite_credito": 0,     "categorias": ["médico", "salud"],        "pais": "ES"},
    "PRV-011": {"nombre": "LegalTrans SL",         "estado": "no_aprobado",  "limite_credito": 0,     "categorias": ["traducción", "legal"],    "pais": "ES"},
    "PRV-012": {"nombre": "Familiar Tech SL",      "estado": "aprobado",     "limite_credito": 30000, "categorias": ["IT", "hardware"],         "pais": "ES",
                "alerta": "conflicto_interes", "vinculado_con": "Director Compras"},
    "PRV-013": {"nombre": "NetworkFix Express",    "estado": "no_aprobado",  "limite_credito": 0,     "categorias": ["redes", "IT"],            "pais": "ES"},
    "PRV-014": {"nombre": "OldContract SL",        "estado": "aprobado",     "limite_credito": 10000, "categorias": ["IT", "servicios"],        "pais": "ES",
                "historial_sla": {"incumplimientos_pct": 40, "periodo": "12_meses"}},
}


def get_proveedor(proveedor_id: str) -> dict:
    """
    Consulta un proveedor por su ID.
    Devuelve estado, límite de crédito, categorías y alertas si las hay.
    """
    if proveedor_id not in PROVEEDORES_DB:
        return {
            "encontrado": False,
            "proveedor_id": proveedor_id,
            "mensaje": "Proveedor no encontrado en el sistema. Debe registrarse antes de operar.",
            "accion_requerida": "registro_nuevo_proveedor"
        }

    prov = PROVEEDORES_DB[proveedor_id]
    resultado = {
        "encontrado": True,
        "proveedor_id": proveedor_id,
        "nombre": prov["nombre"],
        "estado": prov["estado"],
        "limite_credito": prov["limite_credito"],
        "categorias": prov["categorias"],
        "pais": prov["pais"],
        "puede_operar": prov["estado"] == "aprobado",
    }

    if "alerta" in prov:
        resultado["alerta"] = prov["alerta"]
        resultado["detalle_alerta"] = prov.get("vinculado_con", "")
        resultado["accion_requerida"] = "escalacion_obligatoria_hil"

    if "historial_sla" in prov:
        sla = prov["historial_sla"]
        resultado["historial_sla"] = sla
        if sla["incumplimientos_pct"] > 30:
            resultado["alerta_sla"] = f"Proveedor incumplió SLA el {sla['incumplimientos_pct']}% en los últimos {sla['periodo']}"
            resultado["accion_requerida"] = "revision_contrato_o_cambio_proveedor"

    return resultado


def registrar_proveedor(nombre: str, categorias: list, pais: str, contacto: str) -> dict:
    """
    Registra un nuevo proveedor en estado 'pendiente_validacion'.
    El agente Legal debe validarlo antes de que pase a 'aprobado'.
    """
    nuevo_id = f"PRV-{900 + len(PROVEEDORES_DB):03d}"
    return {
        "proveedor_id": nuevo_id,
        "nombre": nombre,
        "estado": "pendiente_validacion",
        "mensaje": "Proveedor registrado. Pendiente de validación por Legal Agent antes de operar.",
        "siguiente_paso": "validacion_legal",
        "categorias": categorias,
        "pais": pais,
        "contacto": contacto
    }


def buscar_alternativas(categoria: str, presupuesto_max: float) -> dict:
    """
    Busca proveedores aprobados alternativos en una categoría y dentro de un presupuesto.
    """
    alternativas = []
    for pid, prov in PROVEEDORES_DB.items():
        if (prov["estado"] == "aprobado"
                and categoria in prov["categorias"]
                and prov["limite_credito"] >= presupuesto_max
                and "alerta" not in prov):
            alternativas.append({
                "proveedor_id": pid,
                "nombre": prov["nombre"],
                "pais": prov["pais"],
                "limite_credito": prov["limite_credito"]
            })

    return {
        "categoria": categoria,
        "presupuesto_max": presupuesto_max,
        "alternativas_encontradas": len(alternativas),
        "alternativas": alternativas,
        "mensaje": f"Se encontraron {len(alternativas)} proveedores aprobados en categoría '{categoria}'"
                   if alternativas else f"No hay proveedores aprobados en '{categoria}' dentro del presupuesto."
    }
