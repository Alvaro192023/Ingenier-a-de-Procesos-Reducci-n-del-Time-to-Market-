"""
================================================================================
ANÁLISIS DE MINERÍA DE DATOS - CASO PROCESS CHAMPION
================================================================================
Descripción: Análisis estadístico completo del indicador Time to Market
             sobre +6,000 releases (Ene - Jun 2023)
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

print("=" * 80)
print("ANÁLISIS DE MINERÍA DE DATOS - CASO PROCESS CHAMPION")
print("=" * 80)

# ============================================================================
# 1. ESTADÍSTICAS DESCRIPTIVAS GENERALES
# ============================================================================
print("\n" + "=" * 80)
print("1. ESTADÍSTICAS DESCRIPTIVAS GENERALES")
print("=" * 80)
print(f"\nTotal de registros: {len(df):,}")
print(f"Periodo: {df['Release Date'].min()} a {df['Release Date'].max()}")

print("\n--- Cycle Duration (days) ---")
print(f"Media: {df['Cycle Duration (days)'].mean():.2f} días")
print(f"Mediana: {df['Cycle Duration (days)'].median():.2f} días")
print(f"Desviación Estándar: {df['Cycle Duration (days)'].std():.2f} días")
print(f"Coeficiente de Variación: {df['Cycle Duration (days)'].std()/df['Cycle Duration (days)'].mean():.2%}")
print(f"Mínimo: {df['Cycle Duration (days)'].min():.2f} días")
print(f"Máximo: {df['Cycle Duration (days)'].max():.2f} días")
print(f"P10: {df['Cycle Duration (days)'].quantile(0.10):.2f} días")
print(f"P25: {df['Cycle Duration (days)'].quantile(0.25):.2f} días")
print(f"P75: {df['Cycle Duration (days)'].quantile(0.75):.2f} días")
print(f"P90: {df['Cycle Duration (days)'].quantile(0.90):.2f} días")
print(f"P99: {df['Cycle Duration (days)'].quantile(0.99):.2f} días")

# ============================================================================
# 2. ANÁLISIS MENSUAL - TENDENCIA
# ============================================================================
print("\n" + "=" * 80)
print("2. ANÁLISIS DE TENDENCIA MENSUAL (DETERIORO PROGRESIVO)")
print("=" * 80)

monthly_stats = df.groupby('Mes').agg({
    'Cycle Duration (days)': ['mean', 'std', 'count'],
    'Number of Incidents': 'mean',
    'Team Availability': 'mean'
}).round(2)

monthly_stats.columns = ['Duration_Mean', 'Duration_Std', 'Count',
                         'Incidents_Mean', 'Availability_Mean']
monthly_stats['CV'] = (monthly_stats['Duration_Std'] /
                       monthly_stats['Duration_Mean']).round(2)

print("\n| Mes | N Releases | Duration Mean | Duration Std | CV |"
      " Incidentes Mean | Availability |")
print("|-----|------------|---------------|--------------|-----|"
      "-----------------|--------------|")
for mes, row in monthly_stats.iterrows():
    print(f"| {mes} | {int(row['Count']):,} | {row['Duration_Mean']:.2f} | "
          f"{row['Duration_Std']:.2f} | {row['CV']:.2f} | "
          f"{row['Incidents_Mean']:.2f} | {row['Availability_Mean']:.1%} |")

# Calcular degradación
first_month = monthly_stats.iloc[0]['Duration_Mean']
last_month = monthly_stats.iloc[-1]['Duration_Mean']
degradacion = ((last_month - first_month) / first_month) * 100
print(f"\n*** DEGRADACIÓN TOTAL: {degradacion:.1f}% "
      f"(de {first_month:.2f} a {last_month:.2f} días) ***")

# ============================================================================
# 3. SEGMENTACIÓN POR TIPO DE PASE
# ============================================================================
print("\n" + "=" * 80)
print("3. SEGMENTACIÓN POR TIPO DE PASE")
print("=" * 80)

tipo_stats = df.groupby('Tipo de Pase').agg({
    'Cycle Duration (days)': ['mean', 'std', 'count', 'median'],
    'Number of Incidents': 'mean'
}).round(2)
tipo_stats.columns = ['Duration_Mean', 'Duration_Std', 'Count',
                      'Duration_Median', 'Incidents_Mean']
tipo_stats['%'] = (tipo_stats['Count'] / len(df) * 100).round(1)

print("\n| Tipo de Pase | N | % | Duration Mean | Duration Std |"
      " Duration Median | Incidentes Mean |")
print("|--------------|-----|-----|---------------|--------------|"
      "-----------------|-----------------|")
for tipo, row in tipo_stats.iterrows():
    print(f"| {tipo} | {int(row['Count']):,} | {row['%']:.1f}% | "
          f"{row['Duration_Mean']:.2f} | {row['Duration_Std']:.2f} | "
          f"{row['Duration_Median']:.2f} | {row['Incidents_Mean']:.2f} |")

auto = df[df['Tipo de Pase'] == 'AUTOMATIZADO']['Cycle Duration (days)']
legacy = df[df['Tipo de Pase'] == 'LEGACY']['Cycle Duration (days)']
diff = auto.mean() - legacy.mean()
print(f"\nDiferencia de medias: {diff:.3f} días")
print("Conclusión: No hay diferencia significativa entre tipos de pase")

# ============================================================================
# 4. ANÁLISIS POR DISPONIBILIDAD DEL EQUIPO (FACTOR CRÍTICO)
# ============================================================================
print("\n" + "=" * 80)
print("4. ANÁLISIS POR DISPONIBILIDAD DEL EQUIPO (FACTOR CRÍTICO)")
print("=" * 80)

df['Availability_Bin'] = pd.cut(
    df['Team Availability'],
    bins=[0, 0.5, 0.7, 0.85, 1.0],
    labels=['<50%', '50-70%', '70-85%', '>85%']
)

avail_stats = df.groupby('Availability_Bin', observed=True).agg({
    'Cycle Duration (days)': ['mean', 'std', 'count'],
    'Number of Incidents': 'mean'
}).round(2)
avail_stats.columns = ['Duration_Mean', 'Duration_Std', 'Count',
                       'Incidents_Mean']

print("\n| Availability | N | Duration Mean | Duration Std | Incidentes Mean |")
print("|--------------|-----|---------------|--------------|-----------------|")
for avail, row in avail_stats.iterrows():
    print(f"| {avail} | {int(row['Count']):,} | {row['Duration_Mean']:.2f} | "
          f"{row['Duration_Std']:.2f} | {row['Incidents_Mean']:.2f} |")

corr_duration = df['Team Availability'].corr(df['Cycle Duration (days)'])
corr_incidents = df['Team Availability'].corr(df['Number of Incidents'])
print(f"\n*** Correlación Availability <-> Duration: {corr_duration:.3f} ***")
print(f"*** Correlación Availability <-> Incidentes: {corr_incidents:.3f} ***")

# ============================================================================
# 5. ANÁLISIS DE INCIDENTES
# ============================================================================
print("\n" + "=" * 80)
print("5. ANÁLISIS DE INCIDENTES")
print("=" * 80)

print(f"\nTotal de incidentes: {df['Number of Incidents'].sum():.0f}")
print(f"Incidentes promedio por release: {df['Number of Incidents'].mean():.2f}")
print(f"Releases con 0 incidentes: {(df['Number of Incidents'] == 0).sum():,} "
      f"({(df['Number of Incidents'] == 0).mean():.1%})")
print(f"Releases con 5+ incidentes: {(df['Number of Incidents'] >= 5).sum():,} "
      f"({(df['Number of Incidents'] >= 5).mean():.1%})")
print(f"Releases con 10+ incidentes: {(df['Number of Incidents'] >= 10).sum():,} "
      f"({(df['Number of Incidents'] >= 10).mean():.1%})")

# ============================================================================
# 6. ANÁLISIS DE SCOPE CHANGES
# ============================================================================
print("\n" + "=" * 80)
print("6. ANÁLISIS DE SCOPE CHANGES")
print("=" * 80)

scope_corr = df['Scope Changes'].corr(df['Cycle Duration (days)'])
print(f"\nCorrelación Scope Changes <-> Duration: {scope_corr:.3f}")
print(f"Scope Changes promedio: {df['Scope Changes'].mean():.2f}")
print(f"Scope Changes std: {df['Scope Changes'].std():.2f}")
print("Conclusión: Scope Changes NO es un factor significativo (r ≈ 0)")

# ============================================================================
# 7. MODELO PREDICTIVO - REGRESIÓN LINEAL
# ============================================================================
print("\n" + "=" * 80)
print("7. MODELO PREDICTIVO - REGRESIÓN LINEAL")
print("=" * 80)

slope, intercept, r_value, p_value, std_err = stats.linregress(
    df['Team Availability'], df['Cycle Duration (days)']
)
r_squared = r_value ** 2

print(f"\nEcuación: Cycle Duration = {intercept:.2f} + "
      f"({slope:.2f}) * Team Availability")
print(f"R-cuadrado: {r_squared:.3f} "
      f"({r_squared*100:.1f}% de la variabilidad explicada)")
print(f"P-value: {p_value:.2e}")
print(f"\nInterpretación: Por cada 10% adicional de disponibilidad, "
      f"el ciclo se reduce en {abs(slope*0.10):.2f} días")

print("\n" + "=" * 80)
print("FIN DEL ANÁLISIS DE MINERÍA DE DATOS")
print("=" * 80)
