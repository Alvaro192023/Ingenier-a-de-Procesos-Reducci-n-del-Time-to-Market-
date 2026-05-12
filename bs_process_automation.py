"""
================================================================================
PROCESS EXCELLENCE - AUTOMATION SCRIPT
================================================================================
Descripción: Script para automatizar el procesamiento de datos y validación
             de la etapa crítica de Development en el Time to Market.
             Incluye detección de anomalías y sistema de alertas tempranas.
Autor: Alvaro Villakoba
Stack: Python (Pandas, SciPy, NumPy)
================================================================================

Este script realiza:
1. Carga y validación de datos del time_to_market_database
2. Cálculo automático de métricas clave
3. Detección de anomalías en la disponibilidad del equipo
4. Alertas tempranas de deterioro del indicador
5. Generación de reporte ejecutivo automático

Uso: python bcp_process_automation.py
"""

import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


class ProcessAnalyzer:
    """Clase principal para análisis de Process Excellence"""

    def __init__(self, excel_path: str):
        self.excel_path = excel_path
        self.df = None
        self.monthly_stats = None
        self.alerts = []

    def load_data(self) -> pd.DataFrame:
        """Cargar y validar datos del Excel"""
        print(f"[INFO] Cargando datos desde {self.excel_path}...")
        self.df = pd.read_excel(self.excel_path)
        self.df['Release Date'] = pd.to_datetime(self.df['Release Date'])
        self.df['Mes'] = self.df['Release Date'].dt.to_period('M')

        null_counts = self.df.isnull().sum()
        if null_counts.any():
            print(f"[WARNING] Valores nulos: "
                  f"{null_counts[null_counts > 0].to_dict()}")
        else:
            print(f"[OK] Datos cargados: {len(self.df):,} registros")

        return self.df

    def calculate_kpis(self) -> dict:
        """Calcular KPIs principales del proceso"""
        print("\n[INFO] Calculando KPIs principales...")

        kpis = {
            'total_releases': len(self.df),
            'avg_cycle_duration': self.df['Cycle Duration (days)'].mean(),
            'std_cycle_duration': self.df['Cycle Duration (days)'].std(),
            'median_cycle_duration': self.df['Cycle Duration (days)'].median(),
            'avg_incidents': self.df['Number of Incidents'].mean(),
            'total_incidents': self.df['Number of Incidents'].sum(),
            'avg_availability': self.df['Team Availability'].mean(),
            'clean_releases_pct': (
                (self.df['Number of Incidents'] == 0).mean() * 100
            ),
        }

        print(f"  - Total Releases: {kpis['total_releases']:,}")
        print(f"  - Avg Cycle Duration: {kpis['avg_cycle_duration']:.2f} días")
        print(f"  - Avg Incidents: {kpis['avg_incidents']:.2f}")
        print(f"  - Clean Releases: {kpis['clean_releases_pct']:.1f}%")

        return kpis

    def analyze_monthly_trend(self) -> pd.DataFrame:
        """Analizar tendencia mensual para detectar deterioro"""
        print("\n[INFO] Analizando tendencia mensual...")

        self.monthly_stats = self.df.groupby('Mes').agg({
            'Cycle Duration (days)': ['mean', 'std'],
            'Team Availability': 'mean',
            'Number of Incidents': 'mean',
            'Release Date': 'count'
        }).round(2)

        self.monthly_stats.columns = ['Duration_Mean', 'Duration_Std',
                                       'Availability', 'Incidents', 'Releases']

        for mes, row in self.monthly_stats.iterrows():
            if row['Duration_Mean'] > 25:
                self.alerts.append({
                    'type': 'CRITICAL',
                    'month': str(mes),
                    'message': f"Duration > 25 días: "
                               f"{row['Duration_Mean']:.2f}d",
                    'availability': row['Availability']
                })
            elif row['Duration_Mean'] > 20:
                self.alerts.append({
                    'type': 'WARNING',
                    'month': str(mes),
                    'message': f"Duration > 20 días: "
                               f"{row['Duration_Mean']:.2f}d",
                    'availability': row['Availability']
                })

        print(f"  - Se generaron {len(self.alerts)} alertas")
        return self.monthly_stats

    def detect_availability_anomalies(self, threshold: float = 0.70):
        """Detectar releases con disponibilidad bajo threshold"""
        print(f"\n[INFO] Detectando anomalías "
              f"(threshold availability < {threshold:.0%})...")

        anomaly_df = self.df[self.df['Team Availability'] < threshold].copy()
        anomaly_count = len(anomaly_df)
        anomaly_pct = anomaly_count / len(self.df) * 100

        print(f"  - Releases con baja disponibilidad: "
              f"{anomaly_count:,} ({anomaly_pct:.1f}%)")

        if anomaly_count > 0:
            avg_duration_anomaly = anomaly_df['Cycle Duration (days)'].mean()
            avg_duration_normal = self.df[
                self.df['Team Availability'] >= threshold
            ]['Cycle Duration (days)'].mean()
            impact = avg_duration_anomaly - avg_duration_normal
            print(f"  - Impacto en duration: +{impact:.2f} días promedio")

            self.alerts.append({
                'type': 'ANOMALY',
                'metric': 'Team Availability',
                'affected_releases': anomaly_count,
                'impact_days': round(impact, 2)
            })

        return anomaly_df

    def run_regression_analysis(self) -> dict:
        """Ejecutar regresión lineal para modelo predictivo"""
        print("\n[INFO] Ejecutando análisis de regresión...")

        slope, intercept, r_value, p_value, std_err = stats.linregress(
            self.df['Team Availability'],
            self.df['Cycle Duration (days)']
        )

        model = {
            'slope': slope,
            'intercept': intercept,
            'r_squared': r_value ** 2,
            'p_value': p_value,
            'equation': f"Duration = {intercept:.2f} + "
                        f"({slope:.2f}) × Availability"
        }

        print(f"  - Ecuación: {model['equation']}")
        print(f"  - R²: {model['r_squared']:.3f} "
              f"({model['r_squared']*100:.1f}% variabilidad explicada)")
        print(f"  - P-value: {p_value:.2e}")

        return model

    def generate_executive_summary(self) -> str:
        """Generar resumen ejecutivo"""
        print("\n" + "=" * 80)
        print("RESUMEN EJECUTIVO AUTOMÁTICO")
        print("=" * 80)

        kpis = self.calculate_kpis()
        self.analyze_monthly_trend()
        model = self.run_regression_analysis()

        summary = f"""
{'='*80}
PROCESS EXCELLENCE - RESUMEN EJECUTIVO
Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*80}

1. SITUACIÓN ACTUAL
-------------------
- Total de releases analizados: {kpis['total_releases']:,}
- Cycle Duration promedio: {kpis['avg_cycle_duration']:.2f} días
- Incidentes promedio por release: {kpis['avg_incidents']:.2f}
- Disponibilidad promedio: {kpis['avg_availability']:.1%}
- Clean Releases: {kpis['clean_releases_pct']:.1f}%

2. ALERTAS DETECTADAS
---------------------"""
        for alert in self.alerts:
            summary += (f"\n   [{alert['type']}] "
                        f"{alert.get('month', '')} - "
                        f"{alert.get('message', '')}")

        summary += f"""

3. MODELO PREDICTIVO
--------------------
{model['equation']}
R² = {model['r_squared']:.3f}

Interpretación: Por cada 10% adicional de disponibilidad del equipo,
el cycle duration se reduce en {abs(model['slope'] * 0.10):.2f} días.

4. RECOMENDACIÓN PRIORITARIA
----------------------------
Maximizar la disponibilidad del equipo (>85%) es la palanca con mayor
impacto comprobado estadísticamente en la reducción del Time to Market.
{'='*80}
"""
        print(summary)
        return summary

    def export_alerts_to_csv(self, output_path: str = 'alerts_output.csv'):
        """Exportar alertas a CSV"""
        if self.alerts:
            alerts_df = pd.DataFrame(self.alerts)
            alerts_df.to_csv(output_path, index=False, encoding='utf-8-sig')
            print(f"\n[INFO] Alertas exportadas a {output_path}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("PROCESS EXCELLENCE - AUTOMATION SCRIPT")
    print("=" * 80)

    analyzer = ProcessAnalyzer('../data/02_time_to_market_database.xlsx')
    analyzer.load_data()
    analyzer.generate_executive_summary()
    analyzer.detect_availability_anomalies(threshold=0.70)
    analyzer.export_alerts_to_csv('alerts_output.csv')

    print("\n" + "=" * 80)
    print("[OK] PROCESO DE AUTOMATIZACIÓN COMPLETADO")
    print("=" * 80)
