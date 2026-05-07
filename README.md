# Multi-Agent LLM Framework for Autonomous Business Process Automation
## A Procurement Case Study

**Universidad Alfonso X el Sabio · Máster Big Data · Prácticas de Empresa · PROJENER.AI SL · 2026**

---

## Descripción

Framework multi-agente basado en LLMs para la automatización end-to-end de procesos de procurement empresarial.
El sistema implementa 5 agentes especializados (Requester, Procurement, Finance, Legal, Compliance)
orquestados con CrewAI, cada uno con acceso exclusivo a 6 APIs mock que simulan sistemas ERP, CRM y bases regulatorias.

## Resultados principales

| Modelo | ARR | HDA | DER | PT (s) |
|--------|-----|-----|-----|--------|
| M1 — RPA Baseline | 100% ±0.0pp | 0% ±0.0pp | 34% ±0.0pp | ~0 |
| M2 — Single Agent | 92% ±11.3pp | 10.3% ±14.5pp | 27.3% ±3.8pp | 0.31 |
| M4 — Multi-Agent Mixto | 98.7% ±0.9pp | 5.1% ±3.6pp | 27.3% ±0.9pp | 1.69 |
| M5b — Clasificador HiL | 94% | 23.1% | 22% | 2.85 |

**Hallazgo principal:** la arquitectura multi-agente requiere modelos suficientemente potentes
(>=70B parámetros en el agente decisor) para superar al agente único.

## Reproducir el experimento en 30 minutos

### Requisitos
- Python 3.12
- Jupyter Lab
- Cuenta gratuita en Groq (https://console.groq.com) para API key

### Instalación

    git clone https://github.com/Edurne0781/multiagent-procurement-llm.git
    cd multiagent-procurement-llm
    pip install crewai groq

### Configuración

    import os
    os.environ['GROQ_API_KEY'] = 'tu_api_key_de_groq'
    os.environ['OTEL_SDK_DISABLED'] = 'true'

### Ejecutar

    from procurement_apis import cargar_casos
    casos = cargar_casos()
    print(f'✅ {len(casos)} casos cargados')

## Estructura del proyecto

    multiagent-procurement-llm/
    ├── api_proveedores.py
    ├── api_finance.py
    ├── api_compliance.py
    ├── api_legal.py
    ├── api_requester.py
    ├── api_hil.py
    ├── procurement_apis.py
    ├── casos_procurement.json
    ├── 01_experimento_principal.ipynb
    └── resultados/
        ├── resultados_m1.json
        ├── resultados_m2.json
        ├── resultados_m4.json
        ├── estadisticas_m1.json
        ├── estadisticas_m2.json
        └── estadisticas_m4.json

## Los 5 agentes y sus herramientas

| Agente | Rol | API |
|--------|-----|-----|
| Requester | Registra solicitudes | api_requester.py |
| Procurement | Valida proveedores | api_proveedores.py |
| Finance | Verifica presupuesto | api_finance.py |
| Legal | Revisa contratos | api_legal.py |
| Compliance | Verifica normativa y decide | api_compliance.py |

## Los 9 modelos del experimento

| ID | Nombre | LLM | Agentes |
|----|--------|-----|---------|
| M1 | Baseline RPA | Ninguno | 1 proceso |
| M2 | Single Agent | llama-3.1-8b | 1 agente |
| M2x | Single expandido | llama-3.1-8b | 1 agente |
| M3 | Multi homogeneo | llama-3.1-8b x5 | 5 agentes |
| M3b | Ablation 3ag | llama-3.1-8b x3 | 3 agentes |
| M4 | Multi mixto | llama-3.1-8b x4 + llama-3.3-70b x1 | 5 agentes |
| M4b | Multi potente | llama-3.3-70b x5 | 5 agentes |
| M5 | Multi + HiL | llama-3.1-8b x5 | 5 agentes |
| M5b | Clasificador HiL | llama-3.1-8b | 2 etapas |

## Referencia

    Martínez de Contrasta, E. (2026). A Multi-Agent LLM Framework for
    Autonomous Business Process Automation: A Procurement Case Study.
    Prácticas de Empresa, Máster Big Data, Universidad Alfonso X el Sabio.
    PROJENER.AI SL, Islas Canarias, España.

## Licencia

MIT License — libre para uso académico y de investigación.

---

*Desarrollado en PROJENER.AI SL · Islas Canarias, España · 2026*