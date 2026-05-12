# Business Case — Reduccion del Time to Market

Diagnostico data-driven sobre el deterioro del indicador Time to Market en un proceso de desarrollo de software. Analisis estadistico de +6,000 releases identificando la disponibilidad del equipo como causa raiz (correlacion -0.79, R2 = 0.628). Mapeo de Value Stream con clasificacion AV/NAV que revelo 34.8% de actividades sin valor agregado. Propuesta de estado To Be con reduccion del 51% en Lead Time (46d a 22.5d) mediante automatizacion de testing, parallel processing y zero-touch deployment. Stack: Python (Pandas, SciPy, Matplotlib), n8n, Jenkins, JIRA.

---

## Estructura del Repositorio

```
Process-Champion-TTM-Reduction/
|
|-- data/                           # Datos del proyecto
|   |-- 02_time_to_market_database.xlsx   # Base de datos de +6,000 releases
|   |-- as_is_process.csv                 # Proceso actual (As Is) con clasificacion AV/NAV
|   |-- to_be_process.csv                 # Proceso propuesto (To Be)
|
|-- scripts/                        # Scripts de analisis
|   |-- analisis_completo.py              # Analisis estadistico completo
|   |-- informe_ejecutivo.py              # Informe ejecutivo con causas raiz y plan de accion
|   |-- bcp_process_automation.py         # Clase de automatizacion con deteccion de anomalias
|   |-- generate_charts.py               # Generacion de visualizaciones
|
|-- charts/                         # Visualizaciones generadas
|   |-- chart_trend.png                   # Tendencia mensual (Duration vs Availability)
|   |-- chart_regression.png              # Scatter + Regresion lineal (R2 = 0.628)
|   |-- chart_segments.png               # Impacto por nivel de disponibilidad
|   |-- chart_vsm.png                    # Comparacion VSM As Is vs To Be
|   |-- chart_pareto.png                 # Pareto de actividades NAV
|
|-- presentation/                   # Presentacion ejecutiva
|   |-- create_presentation.js            # Script PptxGenJS (13 slides)
|
|-- docs/                           # Documentacion adicional
|   |-- hallazgos_clave.md               # Resumen de hallazgos principales
|
|-- requirements.txt                # Dependencias Python
```

## Hallazgos Principales

| Metrica | Valor |
|---------|-------|
| Releases analizados | 6,000 |
| Periodo | Enero - Junio 2023 |
| Degradacion TTM | +65.2% (17.1d a 28.3d) |
| Causa raiz | Team Availability (r = -0.792) |
| R2 del modelo | 0.628 (62.8% variabilidad explicada) |
| Impacto por +10% availability | -2.72 dias en cycle duration |
| Lead Time As Is | 46 dias |
| Lead Time To Be | 22.5 dias (-51.1%) |
| Actividades NAV | 34.8% del proceso (16 dias) |
| Muda dominante | Inspeccion (10d, 21.7% del proceso) |

## Visualizaciones

### Tendencia Mensual del Deterioro
![Tendencia Mensual](charts/chart_trend.png)

### Modelo Predictivo: Team Availability vs Cycle Duration
![Regresion](charts/chart_regression.png)

### Impacto por Nivel de Disponibilidad
![Segmentos](charts/chart_segments.png)

### Value Stream Map: As Is vs To Be
![VSM](charts/chart_vsm.png)

### Pareto de Desperdicios (NAV)
![Pareto](charts/chart_pareto.png)

## Propuesta de Mejora (To Be)

| Etapa | As Is | To Be | Reduccion | Herramienta |
|-------|-------|-------|-----------|-------------|
| Requirement Gathering | 5d | 2d | 60% | JIRA + Automation |
| Technical Design | 10d | 5d | 50% | Confluence Templates |
| Development | 20d | 12d | 40% | Git + CI/CD + Pair Programming |
| Testing (Func. + QA) | 10d | 3d | 70% | Selenium + Jenkins |
| Deployment | 1d | 0.5d | 50% | Jenkins Pipeline |
| **TOTAL** | **46d** | **22.5d** | **51.1%** | |

## Roadmap de Implementacion

- **Fase 1 (0-30 dias):** Maximizar Team Availability >85%, implementar metricas de monitoreo
- **Fase 2 (30-60 dias):** Parallel processing en requerimientos, templates de diseno tecnico
- **Fase 3 (60-90 dias):** Automatizacion de testing con Selenium, zero-touch deployment con Jenkins

## Stack Tecnologico

- **Analisis de datos:** Python (Pandas, SciPy, NumPy, Matplotlib)
- **Automatizacion de workflows:** n8n
- **CI/CD y deployment:** Jenkins
- **Gestion de requerimientos:** JIRA + Confluence
- **Presentacion ejecutiva:** PptxGenJS (Node.js)

## Como Ejecutar

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar analisis completo
cd scripts/
python analisis_completo.py

# Generar informe ejecutivo
python informe_ejecutivo.py

# Ejecutar automatizacion con alertas
python bs_process_automation.py

# Generar visualizaciones
python generate_charts.py

# Generar presentacion PPTX (requiere Node.js)
cd ../presentation/
npm install pptxgenjs
node create_presentation.js
```

## Autor

**Alvaro Villakoba** — Business Analytics Consultant
