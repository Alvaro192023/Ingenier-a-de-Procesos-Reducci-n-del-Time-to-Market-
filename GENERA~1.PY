"""
================================================================================
GENERACIÓN DE VISUALIZACIONES - CASO PROCESS CHAMPION
================================================================================
Descripción: Script para generar todos los gráficos del análisis TTM
Autor: Alvaro Villakoba
Stack: Python (Pandas, Matplotlib, SciPy)
Output: charts/ folder con 5 visualizaciones PNG
================================================================================
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import stats

# Cargar datos
df = pd.read_excel('../data/02_time_to_market_database.xlsx')
df['Release Date'] = pd.to_datetime(df['Release Date'])
df['Mes'] = df['Release Date'].dt.to_period('M')

# Paleta de colores
NAVY = '#0D1B2A'
BLUE = '#1B4965'
TEAL = '#5FA8D3'
ACCENT = '#F77F00'
LIGHT = '#CAE9FF'
WHITE = '#FFFFFF'
GRAY = '#94A3B8'

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 11

# =============================================
# CHART 1: Monthly Trend with dual axis
# =============================================
fig, ax1 = plt.subplots(figsize=(9, 4.5))
fig.patch.set_facecolor(WHITE)
ax1.set_facecolor(WHITE)

months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
durations = [17.13, 15.12, 18.30, 21.63, 24.96, 28.30]
availability = [95, 88, 79, 71, 63, 54]

bars = ax1.bar(
    months, durations,
    color=[TEAL if d < 20 else ACCENT if d < 25 else '#E63946'
           for d in durations],
    width=0.55, zorder=3
)
for bar, val in zip(bars, durations):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
             f'{val:.1f}d', ha='center', fontsize=10,
             fontweight='bold', color=NAVY)

ax2 = ax1.twinx()
ax2.plot(months, availability, color=ACCENT, marker='o',
         linewidth=2.5, markersize=8, zorder=5)
for m, a in zip(months, availability):
    ax2.annotate(f'{a}%', (m, a), textcoords='offset points',
                 xytext=(0, 12), ha='center', fontsize=9,
                 color=ACCENT, fontweight='bold')

ax1.set_ylabel('Cycle Duration (días)', color=NAVY, fontsize=11)
ax2.set_ylabel('Team Availability (%)', color=ACCENT, fontsize=11)
ax1.set_ylim(0, 35)
ax2.set_ylim(40, 105)
ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax1.grid(axis='y', alpha=0.2)
ax1.set_axisbelow(True)

plt.tight_layout()
plt.savefig('../charts/chart_trend.png', dpi=200,
            bbox_inches='tight', facecolor=WHITE)
plt.close()
print("[OK] chart_trend.png generado")

# =============================================
# CHART 2: Scatter + Regression
# =============================================
fig, ax = plt.subplots(figsize=(8, 4.5))
fig.patch.set_facecolor(WHITE)
ax.set_facecolor(WHITE)

sample = df.sample(800, random_state=42)
ax.scatter(sample['Team Availability']*100,
           sample['Cycle Duration (days)'],
           alpha=0.25, s=15, color=TEAL, zorder=3)

slope, intercept, r_value, p_value, std_err = stats.linregress(
    df['Team Availability'], df['Cycle Duration (days)'])
x_line = np.linspace(0.4, 1.0, 100)
y_line = intercept + slope * x_line
ax.plot(x_line*100, y_line, color='#E63946', linewidth=2.5,
        zorder=5, label=f'R² = 0.628')
ax.legend(fontsize=11, loc='upper right')

ax.set_xlabel('Team Availability (%)', fontsize=11, color=NAVY)
ax.set_ylabel('Cycle Duration (días)', fontsize=11, color=NAVY)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(alpha=0.2)

plt.tight_layout()
plt.savefig('../charts/chart_regression.png', dpi=200,
            bbox_inches='tight', facecolor=WHITE)
plt.close()
print("[OK] chart_regression.png generado")

# =============================================
# CHART 3: Availability Segments Bar
# =============================================
fig, ax = plt.subplots(figsize=(7, 4))
fig.patch.set_facecolor(WHITE)
ax.set_facecolor(WHITE)

segments = ['<50%', '50-70%', '70-85%', '>85%']
seg_durations = [28.69, 25.34, 19.10, 16.46]
colors = ['#E63946', ACCENT, TEAL, '#2A9D8F']

bars = ax.barh(segments, seg_durations, color=colors, height=0.55)
for bar, val in zip(bars, seg_durations):
    ax.text(val + 0.3, bar.get_y() + bar.get_height()/2,
            f'{val:.1f}d', va='center', fontsize=11,
            fontweight='bold', color=NAVY)

ax.set_xlabel('Cycle Duration Promedio (días)', fontsize=11, color=NAVY)
ax.set_xlim(0, 34)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='x', alpha=0.2)
ax.invert_yaxis()

plt.tight_layout()
plt.savefig('../charts/chart_segments.png', dpi=200,
            bbox_inches='tight', facecolor=WHITE)
plt.close()
print("[OK] chart_segments.png generado")

# =============================================
# CHART 4: VSM As Is vs To Be
# =============================================
fig, axes = plt.subplots(2, 1, figsize=(9, 4),
                          gridspec_kw={'height_ratios': [1, 1]})
fig.patch.set_facecolor(WHITE)

as_is_steps = ['Req. Gathering', 'Tech Design', 'Development',
               'Testing', 'QA Review', 'Deployment']
as_is_durations = [5, 10, 20, 7, 3, 1]
as_is_colors = ['#E63946', TEAL, TEAL, '#E63946', '#E63946', '#E63946']

to_be_steps = ['Req. Gathering', 'Tech Design', 'Development',
               'Auto Testing', 'Deployment', '']
to_be_durations = [2, 5, 12, 3, 0.5, 0]
to_be_colors = ['#E63946', TEAL, TEAL, '#E63946', '#E63946', WHITE]

for ax_idx, (ax, steps, durs, cols, label) in enumerate(zip(
    axes,
    [as_is_steps, to_be_steps],
    [as_is_durations, to_be_durations],
    [as_is_colors, to_be_colors],
    ['AS IS (46 días)', 'TO BE (22.5 días)']
)):
    ax.set_facecolor(WHITE)
    left = 0
    for step, dur, col in zip(steps, durs, cols):
        if dur > 0:
            ax.barh(0, dur, left=left, color=col, height=0.5,
                    edgecolor=WHITE, linewidth=1)
            if dur >= 2:
                ax.text(left + dur/2, 0, f'{step}\n{dur}d',
                        ha='center', va='center', fontsize=7,
                        color=WHITE, fontweight='bold')
        left += dur
    ax.set_xlim(0, 50)
    ax.set_yticks([0])
    ax.set_yticklabels([label], fontsize=10, fontweight='bold', color=NAVY)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    if ax_idx == 1:
        ax.set_xlabel('Días', fontsize=10, color=NAVY)
    else:
        ax.set_xticklabels([])

plt.tight_layout()
plt.savefig('../charts/chart_vsm.png', dpi=200,
            bbox_inches='tight', facecolor=WHITE)
plt.close()
print("[OK] chart_vsm.png generado")

# =============================================
# CHART 5: Pareto of NAV activities
# =============================================
fig, ax1 = plt.subplots(figsize=(7, 4))
fig.patch.set_facecolor(WHITE)
ax1.set_facecolor(WHITE)

nav_labels = ['Functional\nTesting', 'Requirement\nGathering',
              'Quality\nReview', 'Production\nDeployment']
nav_durations = [7, 5, 3, 1]
cumulative = np.cumsum(nav_durations) / sum(nav_durations) * 100

bars = ax1.bar(nav_labels, nav_durations,
               color=[ACCENT, ACCENT, TEAL, TEAL], width=0.55, zorder=3)
for bar, val in zip(bars, nav_durations):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.15,
             f'{val}d', ha='center', fontsize=10,
             fontweight='bold', color=NAVY)

ax2 = ax1.twinx()
ax2.plot(nav_labels, cumulative, color='#E63946', marker='D',
         linewidth=2, markersize=6, zorder=5)
ax2.set_ylim(0, 110)
ax2.set_ylabel('% Acumulado', color='#E63946', fontsize=10)

ax1.set_ylabel('Días NAV', fontsize=10, color=NAVY)
ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax1.grid(axis='y', alpha=0.2)

plt.tight_layout()
plt.savefig('../charts/chart_pareto.png', dpi=200,
            bbox_inches='tight', facecolor=WHITE)
plt.close()
print("[OK] chart_pareto.png generado")

print("\n[OK] Todas las visualizaciones generadas en ../charts/")
