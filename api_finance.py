"""
API Mock: Verificación Presupuestaria (Finance mock)
Agente que la usa: Finance Agent
Simula la consulta al sistema financiero / ERP de presupuestos.
"""

PRESUPUESTOS_DB = {
    "IT":        {"total": 50000, "gastado": 45000, "disponible": 5000,  "limite_compra_autonoma": 2000},
    "RRHH":      {"total": 20000, "gastado": 18500, "disponible": 1500,  "limite_compra_autonoma": 1500},
    "LEGAL":     {"total": 15000, "gastado": 10000, "disponible": 5000,  "limite_compra_autonoma": 3000},
    "COMPRAS":   {"total": 80000, "gastado": 55000, "disponible": 25000, "limite_compra_autonoma": 5000},
    "FACILITIES":{"total": 30000, "gastado": 26800, "disponible": 3200,  "limite_compra_autonoma": 2000},
    "MARKETING": {"total": 25000, "gastado": 22000, "disponible": 3000,  "limite_compra_autonoma": 1000},
    "DIRECCION": {"total": 200000,"gastado": 80000, "disponible": 120000,"limite_compra_autonoma": 50000},
}

# Límites globales de aprobación por rol
LIMITES_APROBACION = {
    "autonomo":       2000,    # Agente aprueba solo
    "finance_agent":  10000,   # Finance Agent puede aprobar
    "director":       50000,   # Requiere aprobación de dirección
    "consejo":        999999,  # Requiere aprobación de consejo
}


def verificar_presupuesto(departamento: str, importe: float) -> dict:
    """
    Verifica si un departamento tiene presupuesto suficiente
    y qué nivel de aprobación requiere.
    """
    if departamento not in PRESUPUESTOS_DB:
        return {
            "valido": False,
            "mensaje": f"Departamento '{departamento}' no encontrado en el sistema financiero."
        }

    dept = PRESUPUESTOS_DB[departamento]
    disponible = dept["disponible"]
    tiene_fondos = disponible >= importe

    # Determinar nivel de aprobación requerido
    if importe <= LIMITES_APROBACION["autonomo"]:
        nivel_aprobacion = "autonomo"
        aprobador = "Sistema automático"
    elif importe <= LIMITES_APROBACION["finance_agent"]:
        nivel_aprobacion = "finance_agent"
        aprobador = "Finance Agent"
    elif importe <= LIMITES_APROBACION["director"]:
        nivel_aprobacion = "director"
        aprobador = "Director de departamento"
    else:
        nivel_aprobacion = "consejo"
        aprobador = "Consejo de dirección"

    resultado = {
        "departamento": departamento,
        "importe_solicitado": importe,
        "presupuesto_disponible": disponible,
        "presupuesto_total": dept["total"],
        "presupuesto_gastado": dept["gastado"],
        "tiene_fondos": tiene_fondos,
        "nivel_aprobacion_requerido": nivel_aprobacion,
        "aprobador": aprobador,
        "aprobado": tiene_fondos,
    }

    if not tiene_fondos:
        deficit = importe - disponible
        resultado["deficit"] = deficit
        resultado["mensaje"] = (
            f"Fondos insuficientes. Déficit de {deficit:.2f}€. "
            f"Opciones: reasignación presupuestaria, fraccionamiento de compra, o rechazo."
        )
        resultado["opciones"] = ["reasignacion_presupuestaria", "fraccionamiento", "rechazo"]
    else:
        resultado["mensaje"] = f"Presupuesto disponible. Nivel de aprobación: {nivel_aprobacion}."

    return resultado


def aprobar_gasto(departamento: str, importe: float, solicitud_id: str) -> dict:
    """
    Registra el gasto aprobado y descuenta del presupuesto disponible.
    """
    if departamento not in PRESUPUESTOS_DB:
        return {"aprobado": False, "mensaje": "Departamento no encontrado."}

    dept = PRESUPUESTOS_DB[departamento]
    if dept["disponible"] < importe:
        return {
            "aprobado": False,
            "solicitud_id": solicitud_id,
            "mensaje": "No se puede aprobar: fondos insuficientes en el momento del registro."
        }

    # Simular descuento (en producción esto sería una escritura en BD)
    dept["gastado"] += importe
    dept["disponible"] -= importe

    return {
        "aprobado": True,
        "solicitud_id": solicitud_id,
        "departamento": departamento,
        "importe_aprobado": importe,
        "presupuesto_restante": dept["disponible"],
        "mensaje": f"Gasto de {importe}€ aprobado y registrado. Presupuesto restante: {dept['disponible']}€"
    }


def proponer_reasignacion(departamento_origen: str, departamento_destino: str, importe: float) -> dict:
    """
    Propone una reasignación presupuestaria entre departamentos.
    Requiere aprobación humana para ejecutarse.
    """
    origen = PRESUPUESTOS_DB.get(departamento_origen, {})
    destino = PRESUPUESTOS_DB.get(departamento_destino, {})

    if not origen or not destino:
        return {"viable": False, "mensaje": "Uno o ambos departamentos no encontrados."}

    viable = origen.get("disponible", 0) >= importe

    return {
        "viable": viable,
        "departamento_origen": departamento_origen,
        "departamento_destino": departamento_destino,
        "importe_reasignar": importe,
        "disponible_en_origen": origen.get("disponible", 0),
        "mensaje": (
            f"Reasignación viable: {importe}€ de {departamento_origen} a {departamento_destino}."
            if viable else
            f"Reasignación no viable: {departamento_origen} solo tiene {origen.get('disponible', 0)}€ disponibles."
        ),
        "requiere_aprobacion_humana": True,
        "accion_requerida": "escalacion_director" if viable else "buscar_otra_fuente"
    }
