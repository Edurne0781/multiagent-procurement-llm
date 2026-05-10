# Multi-Agent LLM Framework for Autonomous Business Process Automation

**Universidad Alfonso X el Sabio · Máster Big Data · Prácticas de Empresa · PROJENER.AI SL · 2026**

---

## Descripción

Framework multi-agente basado en LLMs para la automatización end-to-end de procesos empresariales complejos. Cinco procesos evaluados: Procurement, Incident Management, Onboarding de Clientes, Compliance Check y Financial Analysis.

## Resultados — resumen cross-process

| Proceso | M2 ARR | M2 HDA | M4 ARR | M4 HDA |
|---------|--------|--------|--------|--------|
| Procurement (50 casos) | 92% | 10.3% | 98.7% | 5.1% |
| Incident Management (20) | 40% | 100% | 45% | 100% |
| Onboarding (20) | 75% | 83.3% | 70% | 100% |
| Compliance Check (20) | 70% | 83.3% | 65% | 100% |
| Financial Analysis (20) | 100% | 0% | 70% | 100% |

**M4 alcanza HDA=100% en 4 de 5 procesos.**

## Hallazgo principal — Gradiente de señales

HDA varía según la explicitud semántica de las señales de riesgo del dominio:
- Financial (señales estratégicas complejas): M2 HDA=0%
- Procurement (señales regulatorias implícitas): M2 HDA=30.8%
- Compliance/Onboarding (señales mixtas): M2 HDA=83.3%
- Incident Management (flags binarios): M2 HDA=100%

## Requisitos

- Python 3.12, Jupyter Lab
- API key gratuita en [console.groq.com](https://console.groq.com)

```bash
git clone https://github.com/Edurne0781/multiagent-procurement-llm.git
pip install crewai groq
```

## Estructura

```
├── projener_01_experimento_principal.ipynb
├── projener_02_incident_management.ipynb
├── projener_03_onboarding.ipynb
├── projener_04_compliance.ipynb
├── projener_05_financial.ipynb
├── casos_procurement.json
├── casos_incident_management.json
├── casos_onboarding.json
├── casos_compliance.json
├── casos_financial.json
├── resultados/
├── resultados_incident/
├── resultados_onboarding/
├── resultados_compliance/
└── resultados_financial/
```

## Referencia

Martínez de Contrasta, E. (2026). A Multi-Agent LLM Framework for Autonomous Business Process Automation. Prácticas de Empresa, Máster Big Data, UAX. PROJENER.AI SL, Madrid.

## Licencia

MIT License

---
*PROJENER.AI SL · Madrid · 2026*
