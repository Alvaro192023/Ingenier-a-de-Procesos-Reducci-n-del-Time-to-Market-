"""
================================================================================
INFORME EJECUTIVO INTEGRAL - CASO PROCESS CHAMPION
================================================================================
Descripción: Informe completo con análisis de causas raíz, mapeo AV/NAV,
             propuesta To Be y plan de acción
Autor: Alvaro Villakoba
Stack: Python (Pandas, SciPy, NumPy, Matplotlib)
================================================================================
"""

import pandas as pd
import numpy as np
from scipy import stats

# Cargar datos
df = pd.read_excel('../data/02_time_to_market_database.xlsx')
df['Release Date'] = pd.to_datetime(df['Release Date'])
df['Mes'] = df['Release Date'].dt.to_period('M')

# Leer proceso As Is
process_df = pd.read_csv('../data/as_is_process.csv')

print("=" * 80)
print("INFORME EJECUTIVO INTEGRAL - CASO PROCESS CHAMPION")
print("=" * 80)

# ============================================================================
# SECCIÓN 1: ANÁLISIS DE CAUSAS RAÍZ DEL DETERIORO
# ============================================================================
print("\n" + "=" * 80)
print("SECCIÓN 1: CAUSAS RAÍZ DEL DETERIORO DEL TIME TO MARKET")
print("=" * 80)

print("\n--- MATRIZ DE CORRELACIONES ---\n")
corr_matrix = df[['Cycle Duration (days)', 'Team Availability',
                  'Number of Incidents', 'Scope Changes']].corr()
print(corr_matrix.round(3))

print("\n*** HALLAZGO PRINCIPAL ***")
print("La variable 'Team Availability' tiene correlación de -0.79 con "
      "Cycle Duration,")
print("explicando el 62.8% de la variabilidad (R² = 0.628)")

slope, intercept, r_value, p_value, std_err = stats.linregress(
    df['Team Availability'], df['Cycle Duration (days)'])
print(f"\nModelo: Duration = {intercept:.2f} + ({slope:.2f}) × Availability")

# Análisis mensual
print("\n--- EVOLUCIÓN MENSUAL DEL DETERIORO ---")
monthly = df.groupby('Mes').agg({
    'Cycle Duration (days)': 'mean',
    'Team Availability': 'mean',
    'Number of Incidents': 'mean'
})

for mes, row in monthly.iterrows():
    if row['Cycle Duration (days)'] > 25:
        estado = "CRITICO"
    elif row['Cycle Duration (days)'] > 20:
        estado = "ALERTA"
    else:
        estado = "NORMAL"
    print(f"[{estado}] {mes}: Duration={row['Cycle Duration (days)']:.2f}d, "
          f"Availability={row['Team Availability']:.0%}, "
          f"Incidents={row['Number of Incidents']:.2f}")

# ============================================================================
# SECCIÓN 2: MAPEO DE DESPERDICIOS AV/NAV
# ============================================================================
print("\n" + "=" * 80)
print("SECCIÓN 2: MAPEO DE DESPERDICIOS - ANÁLISIS AV/NAV")
print("=" * 80)

total_process = process_df['Duration (days)'].sum()
av_total = process_df[process_df['Value Type'] == 'AV']['Duration (days)'].sum()
nav_total = process_df[process_df['Value Type'] == 'NAV']['Duration (days)'].sum()

print(f"\n--- VALUE STREAM MAP ACTUAL (AS IS) ---")
print(f"Lead Time Total: {total_process} días")
print(f"Value Added (AV): {av_total} días ({av_total/total_process*100:.1f}%)")
print(f"Non-Value Added (NAV): {nav_total} días "
      f"({nav_total/total_process*100:.1f}%)")

print("\n--- DETALLE DE ETAPAS NAV (DESPERDICIOS) ---")
nav_steps = process_df[process_df['Value Type'] == 'NAV']
for _, row in nav_steps.iterrows():
    print(f"  - {row['Process Step']}: {row['Duration (days)']} días "
          f"- Muda: {row['Muda Type']}")

print("\n--- MUDAS IDENTIFICADAS ---")
muda_summary = nav_steps.groupby('Muda Type')['Duration (days)'].sum()
for muda, duration in muda_summary.items():
    print(f"  {muda}: {duration} días ({duration/total_process*100:.1f}% "
          f"del proceso)")

# ============================================================================
# SECCIÓN 3: PROPUESTA DE ESTADO TO-BE
# ============================================================================
print("\n" + "=" * 80)
print("SECCIÓN 3: PROPUESTA DE ESTADO TO-BE")
print("=" * 80)

to_be_process = pd.DataFrame([
    {'Process Step': 'Requirement Gathering', 'Duration (days)': 2,
     'Tool Used': 'JIRA + Automation', 'Improvement': 'Parallel processing'},
    {'Process Step': 'Technical Design', 'Duration (days)': 5,
     'Tool Used': 'Confluence Templates', 'Improvement': 'Standardization'},
    {'Process Step': 'Development', 'Duration (days)': 12,
     'Tool Used': 'Git + CI/CD', 'Improvement': 'Pair programming + automation'},
    {'Process Step': 'Automated Testing', 'Duration (days)': 3,
     'Tool Used': 'Selenium + Jenkins', 'Improvement': 'Test automation'},
    {'Process Step': 'Production Deployment', 'Duration (days)': 0.5,
     'Tool Used': 'Jenkins Pipeline', 'Improvement': 'Zero-touch deployment'}
])

to_be_total = to_be_process['Duration (days)'].sum()

print(f"\n--- VALUE STREAM MAP PROPUESTO (TO BE) ---")
print(f"Lead Time Total: {to_be_total} días")

print(f"\n--- COMPARACIÓN AS IS vs TO BE ---")
print(f"{'Métrica':<30} {'As Is':<12} {'To Be':<12} {'Mejora':<12}")
print("-" * 66)
print(f"{'Lead Time Total':<30} {total_process:<12.1f} {to_be_total:<12.1f} "
      f"{((total_process-to_be_total)/total_process*100):.1f}%")

print("\n--- MEJORAS PROPUESTAS POR ETAPA ---")
for _, row in to_be_process.iterrows():
    as_is_row = process_df[process_df['Process Step'] == row['Process Step']]
    if len(as_is_row) > 0:
        as_is_duration = as_is_row['Duration (days)'].values[0]
        mejora = ((as_is_duration - row['Duration (days)']) /
                  as_is_duration) * 100
        print(f"  - {row['Process Step']}: {as_is_duration}d -> "
              f"{row['Duration (days)']}d ({mejora:.0f}% reducción)")
        print(f"    Herramienta: {row['Tool Used']} | {row['Improvement']}")

# ============================================================================
# SECCIÓN 4: PLAN DE ACCIÓN RECOMENDADO
# ============================================================================
print("\n" + "=" * 80)
print("SECCIÓN 4: PLAN DE ACCIÓN RECOMENDADO")
print("=" * 80)

acciones = [
    {'Prioridad': 'ALTA', 'Acción': 'Maximizar Team Availability (>85%)',
     'Impacto': 'Reducción de 12 días en cycle duration',
     'Timeline': 'Inmediato (0-30 días)'},
    {'Prioridad': 'ALTA', 'Acción': 'Parallel processing en Req. Gathering',
     'Impacto': 'Reducción de 5 a 2 días (60%)',
     'Timeline': 'Corto plazo (30-60 días)'},
    {'Prioridad': 'ALTA', 'Acción': 'Automatización de testing (Selenium)',
     'Impacto': 'Reducción de 7 a 3 días (57%)',
     'Timeline': 'Mediano plazo (60-90 días)'},
    {'Prioridad': 'MEDIA', 'Acción': 'Templates de Technical Design',
     'Impacto': 'Reducción de 10 a 5 días (50%)',
     'Timeline': 'Corto plazo (30-60 días)'},
    {'Prioridad': 'MEDIA', 'Acción': 'Zero-touch deployment (Jenkins)',
     'Impacto': 'Reducción de 1 a 0.5 días (50%)',
     'Timeline': 'Mediano plazo (60-90 días)'},
]

print("\n| Prioridad | Acción | Impacto | Timeline |")
print("|-----------|--------|---------|----------|")
for acc in acciones:
    print(f"| {acc['Prioridad']} | {acc['Acción']} | "
          f"{acc['Impacto']} | {acc['Timeline']} |")

print(f"\n--- IMPACTO TOTAL ESPERADO ---")
print(f"Lead Time Actual: {total_process} días")
print(f"Lead Time Propuesto: {to_be_total} días")
print(f"Reducción Absoluta: {total_process - to_be_total:.1f} días")
print(f"Reducción Relativa: "
      f"{(total_process - to_be_total)/total_process*100:.1f}%")

print("\n" + "=" * 80)
print("FIN DEL INFORME EJECUTIVO")
print("=" * 80)
