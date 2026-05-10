# Multi-Agent LLM Framework for Autonomous Business Process Automation

**Universidad Alfonso X el Sabio · Máster Big Data · Prácticas de Empresa · PROJENER.AI SL · 2026**

---

## Descripción

Framework multi-agente basado en LLMs para la automatización end-to-end de procesos empresariales complejos. El sistema implementa agentes especializados con roles empresariales orquestados con CrewAI, cada uno con acceso a APIs mock que simulan sistemas ERP, CRM y bases regulatorias.

**Tres procesos evaluados:**
- **Experimento 01** — Procurement (50 casos, 9 modelos)
- **Experimento 02** — Incident Management IT (20 casos, 3 modelos)
- **Experimento 03** — Onboarding de Clientes (20 casos, 3 modelos)

## Resultados principales

### Experimento 01 — Procurement

| Modelo | ARR | HDA | DER | PT (s) |
|--------|-----|-----|-----|--------|
| M1 — RPA Baseline | 100% ±0.0pp | 0% ±0.0pp | 34% ±0.0pp | ~0 |
| M2 — Single Agent | 92% ±11.3pp | 10.3% ±14.5pp | 27.3% ±3.8pp | 0.31 |
| M4 — Multi-Agent Mixto | 98.7% ±0.9pp | 5.1% ±3.6pp | 27.3% ±0.9pp | 1.69 |
| M5b — Clasificador HiL | 94% | 23.1% | 22% | 2.85 |

### Experimento 02 — Incident Management

| Modelo | ARR | HDA | DER | PT (s) |
|--------|-----|-----|-----|--------|
| M1 — RPA Baseline | 100% | 0% | 15% | ~0 |
| M2 — Single Agent 8b | 40% | 100% | 0% | 0.54 |
| M4 — Multi-Agent Mixto | 45% | 100% | 0% | 5.04 |

### Experimento 03 — Onboarding de Clientes

| Modelo | ARR | HDA | DER | PT (s) |
|--------|-----|-----|-----|--------|
| M1 — RPA Baseline | 100% | 0% | 70% | ~0 |
| M2 — Single Agent 8b | 75% | 83.3% | 45% | 0.60 |
| M4 — Multi-Agent Mixto | 70% | 100% | 40% | 4.68 |

## Hallazgos principales

1. **Compute equivalence:** el agente único con contexto expandido (M2x: ARR=84%) supera al sistema multi-agente homogéneo con el mismo presupuesto de tokens (M3: ARR=68%)
2. **Diversidad de modelos:** mayor salto del experimento (+32pp ARR de M3 a M4)
3. **Trade-off automatización/riesgo:** eliminar agentes Legal y Procurement sube ARR +20pp pero destruye HDA
4. **Gradiente de señales:** HDA aumenta monotónicamente según la explicitud de las señales de riesgo del dominio — 30.8% (señales regulatorias implícitas) → 83.3% (señales mixtas AML/PEP) → 100% (flags binarios explícitos)
5. **Estabilidad:** M4 σARR=0.9pp vs M2 σARR=11.3pp

## Reproducir el experimento en 30 minutos

### Requisitos
- Python 3.12
- Jupyter Lab
- Cuenta gratuita en [Groq](https://console.groq.com) para API key

### Instalación

```bash
git clone https://github.com/Edurne0781/multiagent-procurement-llm.git
cd multiagent-procurement-llm
pip install crewai groq
```

### Configuración

```python
import os
os.environ['GROQ_API_KEY'] = 'tu_api_key_de_groq'
os.environ['OTEL_SDK_DISABLED'] = 'true'
```

## Estructura del proyecto

```
multiagent-procurement-llm/
├── api_proveedores.py
├── api_finance.py
├── api_compliance.py
├── api_legal.py
├── api_requester.py
├── api_hil.py
├── procurement_apis.py
├── casos_procurement.json
├── casos_incident_management.json
├── casos_onboarding.json
├── projener_01_experimento_principal.ipynb
├── projener_02_incident_management.ipynb
├── projener_03_onboarding.ipynb
├── resultados/
│   ├── resultados_m1.json ... resultados_m5b.json
│   ├── resultados_a1.json, resultados_a2.json
│   ├── estadisticas_m1.json, estadisticas_m2.json, estadisticas_m4.json
│   └── m2_replica2.json, m2_replica3.json, m4_replica2.json, m4_replica3.json
├── resultados_incident/
│   ├── resultados_inc_m1.json
│   ├── resultados_inc_m2.json
│   └── resultados_inc_m4.json
└── resultados_onboarding/
    ├── resultados_onb_m1.json
    ├── resultados_onb_m2.json
    └── resultados_onb_m4.json
```

## Los agentes por proceso

### Experimento 01 — Procurement (5 agentes)

| Agente | Rol | API |
|--------|-----|-----|
| Requester | Registra solicitudes | api_requester.py |
| Procurement | Valida proveedores | api_proveedores.py |
| Finance | Verifica presupuesto | api_finance.py |
| Legal | Revisa contratos | api_legal.py |
| Compliance | Verifica normativa y decide | api_compliance.py |

### Experimento 02 — Incident Management (5 agentes)
Reporter · Technical · Security · Operations · Resolver (70b)

### Experimento 03 — Onboarding (4 agentes)
Comercial · Legal · Finanzas · Compliance/KYC (70b)

## Los 9 modelos del Experimento 01

| ID | Nombre | LLM | Agentes |
|----|--------|-----|---------|
| M1 | Baseline RPA | Ninguno | 1 proceso |
| M2 | Single Agent | llama-3.1-8b | 1 |
| M2x | Single expandido | llama-3.1-8b | 1 |
| M3 | Multi homogéneo | llama-3.1-8b ×5 | 5 |
| M3b | Ablation 3ag | llama-3.1-8b ×3 | 3 |
| M4 | Multi mixto (**óptimo**) | llama-3.1-8b ×4 + llama-3.3-70b ×1 | 5 |
| M4b | Multi potente | llama-3.3-70b ×5 | 5 |
| M5 | Multi + HiL | llama-3.1-8b ×5 | 5 |
| M5b | Clasificador HiL | llama-3.1-8b | 2 etapas |

## Referencia

```
Martínez de Contrasta, E. (2026). A Multi-Agent LLM Framework for
Autonomous Business Process Automation: A Procurement Case Study.
Prácticas de Empresa, Máster Big Data, Universidad Alfonso X el Sabio.
PROJENER.AI SL, Madrid, España.
```

## Licencia

MIT License — libre para uso académico y de investigación.

---
*Desarrollado en PROJENER.AI SL · Madrid, España · 2026*
