# Role Specialization and Context Fragmentation in Multi-Agent LLM Systems
## An Empirical Study on Procurement Automation

**Autora:** Edurne Martínez de Contrasta  
**Institución:** Máster en Big Data y Business Analytics, Universidad Alfonso X el Sabio (UAX), Campus Mare Nostrum  
**Empresa:** PROJENER.AI SL, Madrid  
**Año:** 2026  

**Paper:** *Role Specialization and Context Fragmentation in Multi-Agent LLM Systems: An Empirical Study on Procurement Automation* — enviado a Expert Systems with Applications (ESWA)

---

## Estructura del repositorio

```
📁 raíz/
├── 📁 notebooks/       — Jupyter notebooks de todos los experimentos
├── 📁 datos/           — Datasets JSON con ground truth anotado
├── 📁 resultados/      — JSONs de resultados por experimento
├── 📁 apis/            — APIs simuladas (mock) en Python
├── 📁 figuras/         — Figuras generadas por los notebooks (no usadas en el paper)
├── 📁 LaTeX Edurne/    — Fuente LaTeX del paper, figuras del paper y .bib
├── 📄 requirements.txt — Dependencias Python
├── 📄 .gitignore       — Archivos excluidos del control de versiones
├── 📄 LICENSE          — Licencia MIT
└── 📄 README.md        — Este archivo
```

---

## Instalación

```bash
pip install -r requirements.txt
```

Añadir la API key de Groq como variable de entorno:

```bash
export GROQ_API_KEY=tu_clave_aqui   # Linux/Mac
set GROQ_API_KEY=tu_clave_aqui      # Windows
```

---

## Notebooks

| Notebook | Descripción |
|---|---|
| `projener_01_experimento_principal.ipynb` | Experimento principal — 50 casos sintéticos de procurement, 9 variantes (RPA-Baseline, Single-Small, Single-Small-XL, Multi-Small, Multi-Small-Abl, Multi-Mixed, Multi-Large, Multi-Mixed-HiL, Multi-Mixed-HiL-Clf) |
| `projener_02_incident_management.ipynb` | Experimento 02 — Gestión de incidencias IT, 20 casos, ACME Industrial S.A. |
| `projener_03_onboarding.ipynb` | Experimento 03 — Onboarding de clientes B2B/B2C, 20 casos |
| `projener_04_compliance.ipynb` | Experimento 04 — Compliance check de proveedores, 20 casos |
| `projener_05_financial.ipynb` | Experimento 05 — Análisis financiero y aprobación de inversiones, 20 casos |
| `projener_06_bpi_challenge_2019.ipynb` | Validación sobre 50 casos reales del BPI Challenge 2019 |
| `projener_07_autogen_comparison.ipynb` | Comparación AutoGen 0.7.5 vs CrewAI sobre los 50 casos de procurement |
| `projener_08_taxonomia_kappa.ipynb` | Validación de taxonomía de señales de riesgo — Cohen's Kappa (autora vs LLM) |
| `projener_08b_kappa_multi_anotador.ipynb` | Kappa multi-anotador — 2 humanos + 4 LLMs, 23 señales |
| `projener_09_llm_as_judge.ipynb` | LLM-as-Judge — métrica SAT de calidad de justificaciones |
| `generar_figuras_paper.ipynb` | Generación de las 18 figuras del paper en PDF |

### Nomenclatura interna

Los notebooks usan nomenclatura interna M1-M5 que se corresponde con los nombres del paper:

| Código interno | Nombre paper |
|---|---|
| M1 | RPA-Baseline |
| M2 | Single-Small |
| M2x | Single-Small-XL |
| M3 | Multi-Small |
| M3b | Multi-Small-Abl |
| M4 | Multi-Mixed |
| M4b | Multi-Large |
| M5 | Multi-Mixed-HiL |
| M5b | Multi-Mixed-HiL-Clf |

---

## Datos

Carpeta `datos/` — datasets JSON con ground truth anotado:

| Archivo | Casos | HiL | Experimento |
|---|---|---|---|
| `casos_procurement.json` | 50 | 13 | Notebook 01 |
| `casos_onboarding.json` | 20 | 6 | Notebook 03 |
| `casos_incident_management.json` | 20 | 6 | Notebook 02 |
| `casos_financial.json` | 20 | 6 | Notebook 05 |
| `casos_compliance.json` | 20 | 6 | Notebook 04 |
| `casos_bpi_adaptados.json` | 50 | 11 | Notebook 06 |
| `casos_bpi_2019.json` | 50 | 11 | Notebook 06 |

---

## Resultados

Carpeta `resultados/` — JSONs de resultados verificados contra el paper (Tabla 3 y Tabla 4):

**Raíz de `resultados/` — Experimento 01 (procurement sintético):**

| Archivo | Modelo | ARR | HDA | DER |
|---|---|---|---|---|
| `resultados_m1.json` | RPA-Baseline Rep.1 | 100% | 0% | 34% |
| `resultados_m2.json` | Single-Small Rep.1 | 76% | 30.8% | 22% |
| `m2_replica2.json` | Single-Small Rep.2 | 100% | 0% | 30% |
| `m2_replica3.json` | Single-Small Rep.3 | 100% | 0% | 30% |
| `resultados_m2x.json` | Single-Small-XL Rep.1 | 84% | 23.1% | 28% |
| `resultados_m2x_r2.json` | Single-Small-XL Rep.2 | 76% | 53.8% | 24% |
| `resultados_m2x_r3.json` | Single-Small-XL Rep.3 | 76% | 30.8% | 14% |
| `resultados_m3.json` | Multi-Small Rep.1 | 68% | 30.8% | 28% |
| `resultados_m3_r2.json` | Multi-Small Rep.2 | 80% | 15.4% | 26% |
| `resultados_m3_r3.json` | Multi-Small Rep.3 | 88% | 15.4% | 26% |
| `resultados_m3b.json` | Multi-Small-Abl | 88% | 0% | 30% |
| `resultados_m4.json` | Multi-Mixed Rep.1 | 100% | 0% | 26% |
| `m4_replica2.json` | Multi-Mixed Rep.2 | 98% | 7.7% | 28% |
| `m4_replica3.json` | Multi-Mixed Rep.3 | 98% | 7.7% | 28% |
| `resultados_m4b.json` | Multi-Large | 98% | 0% | 26% |
| `resultados_m5.json` | Multi-Mixed-HiL | 98% | 0% | 28% |
| `resultados_m5b.json` | Multi-Mixed-HiL-Clf | 94% | 23.1% | 22% |
| `resultados_a1.json` | Ablation sin Legal | 88% | 38.5% | 86% |
| `resultados_a2.json` | Ablation sin Compliance | 74% | 53.8% | 74% |
| `estadisticas_m1.json` | RPA-Baseline media 3 reps | 100%±0.0 | 0%±0.0 | 34%±0.0 |
| `estadisticas_m2.json` | Single-Small media 3 reps | 92%±11.3 | 10.3%±14.5 | 27.3%±3.8 |
| `estadisticas_m4.json` | Multi-Mixed media 3 reps | 98.7%±0.9 | 5.1%±3.6 | 27.3%±0.9 |
| `kappa_taxonomia.json` | Kappa autora vs LLM | κ=1.0 | — | — |
| `kappa_multi_anotador.json` | Kappa 6 anotadores | κ=0.652 | — | — |
| `llm_judge_satisfaccion.json` | SAT por variante | Multi-Mixed=4.36 | — | — |

**Subcarpetas:**

| Carpeta | Contenido |
|---|---|
| `02_incident/` | `resultados_inc_m1.json`, `resultados_inc_m2.json`, `resultados_inc_m4.json` |
| `03_onboarding/` | `resultados_onb_m1.json`, `resultados_onb_m2.json`, `resultados_onb_m4.json` |
| `04_compliance/` | `resultados_comp_m1.json`, `resultados_comp_m2.json`, `resultados_comp_m4.json` |
| `05_financial/` | `resultados_fin_m1.json`, `resultados_fin_m2.json`, `resultados_fin_m4.json` |
| `06_bpi/` | `resultados_m1_bpi.json`, `resultados_m2_bpi.json`, `resultados_m3_bpi.json`, `resultados_m4_bpi.json`, `comparativa_bpi_2019.json` |
| `07_autogen/` | `resultados_autogen.json`, `comparativa_autogen_crewai.json` |

---

## APIs simuladas

Carpeta `apis/` — implementaciones mock de las APIs que usan los agentes:

| Archivo | Descripción |
|---|---|
| `procurement_apis.py` | Orquestación principal de APIs de procurement (experimentos sintéticos) |
| `procurement_apis_bpi.py` | Orquestación principal de APIs de procurement (BPI Challenge 2019) |
| `api_requester.py` | API del agente solicitante |
| `api_proveedores.py` | Validación de proveedores (experimentos sintéticos) |
| `api_proveedores_bpi.py` | Validación de proveedores (BPI Challenge 2019) |
| `api_legal.py` | Verificación legal y contractual |
| `api_hil.py` | Mecanismo de escalación Human-in-the-Loop |
| `api_finance.py` | Control presupuestario (experimentos sintéticos) |
| `api_finance_bpi.py` | Control presupuestario (BPI Challenge 2019) |
| `api_compliance.py` | Compliance y normativa (experimentos sintéticos) |
| `api_compliance_bpi.py` | Compliance y normativa (BPI Challenge 2019) |

---

## LaTeX

Carpeta `LaTeX Edurne/` — fuente del paper:

| Archivo | Descripción |
|---|---|
| `projener_multiagent_EN.tex` | Fuente LaTeX del paper en inglés (versión definitiva) |
| `highlights.tex` | Highlights para ESWA |
| `references_multiagent.bib` | Referencias bibliográficas |
| `projener_multiagente.pdf` | PDF compilado del paper |
| `figura1.pdf` | Comparativa métricas principales (usada en paper) |
| `figura2.pdf` | Curva eficiencia ARR vs PT (usada en paper) |
| `figura4.pdf` | Radar de perfiles (usada en paper) |
| `figura5.pdf` | ARR vs coste + tokens (usada en paper) |
| `figura_inc1_metrics.pdf` | Experimento 02 — Incident Management (usada en paper) |

---

## Reproducibilidad

**Stack tecnológico:** CrewAI 1.14.2, Python 3.12, Jupyter Lab, Windows 10  
**LLM auxiliar:** `llama-3.1-8b-instant` vía Groq API  
**LLM decisor (Mixed/Large):** `llama-3.3-70b-versatile` vía Groq API  
**Temperature:** 0.0  
**Pausa anti-rate-limit:** 4–8 s entre casos  

Para reproducir el experimento principal:
1. Clonar el repositorio
2. Instalar dependencias: `pip install -r requirements.txt`
3. Añadir API key de Groq como variable de entorno: `GROQ_API_KEY=tu_clave`
4. Ejecutar los notebooks en orden (01 → 09)

**Nota:** Las rutas del código están configuradas para Windows. En otro sistema operativo, ajustar `BASE_DIR` en la celda de configuración del notebook 01.

---

## Métricas principales

| Métrica | Definición | Objetivo |
|---|---|---|
| **ARR** | Autonomous Resolution Rate — % casos resueltos sin intervención humana | >70% |
| **HDA** | HiL Detection Accuracy — % casos que requieren escalación y son detectados | Exploratoria (n=13) |
| **DER** | Decision Error Rate — % decisiones incorrectas vs ground truth | <10% |
| **PT** | Processing Time — segundos por caso | — |

---

## Licencia

MIT License — Copyright (c) 2026 Edurne Martínez de Contrasta, PROJENER.AI SL. Ver archivo `LICENSE` para más detalles.

---

*Repositorio asociado al artículo científico enviado a ESWA — Junio 2026*
