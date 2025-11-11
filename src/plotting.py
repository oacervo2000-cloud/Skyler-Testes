# src/plotting.py

"""
Módulo de Plotagem.
... (comentários como antes) ...
"""

from .config import plt, np, u, AltAz, SkyCoord, pd
from matplotlib.dates import DateFormatter
import seaborn as sns

def plot_target_visibility(
    # ... (código da função como antes) ...
):
    # ... (código da função como antes) ...

def plot_sky_map(
    # ... (código da função como antes) ...
):
    # ... (código da função como antes) ...

def plot_yearly_visibility(df_year, target_name, year):
    """
    Gera um mapa de calor para visualizar a visibilidade de um alvo ao longo do ano.
    """
    if df_year.empty:
        print(f"Nenhum dado de visibilidade para plotar para {target_name} em {year}.")
        return

    # Preparar os dados para o heatmap
    df_year['month'] = df_year['date'].dt.month
    df_year['day'] = df_year['date'].dt.day

    # Pivotar a tabela para criar uma matriz [mês x dia]
    heatmap_data = df_year.pivot_table(index='month', columns='day', values='duration_hours')

    plt.figure(figsize=(15, 6))
    sns.heatmap(heatmap_data, cmap='viridis', robust=True)

    plt.title(f'Calendário de Visibilidade para {target_name} em {year} (horas > 30°)')
    plt.xlabel('Dia do Mês')
    plt.ylabel('Mês')
    plt.yticks(ticks=np.arange(12) + 0.5, labels=[
        'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
        'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'
    ], rotation=0)

    plt.show()

print("Módulo de Plotagem (src/plotting.py) carregado e aprimorado.")
