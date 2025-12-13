# src/plotting.py

"""
Módulo de Plotagem.
Contém funções para gerar todas as visualizações de dados astronômicos.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from astropy import units as u
from matplotlib.dates import DateFormatter
import seaborn as sns
from astropy.coordinates import SkyCoord, AltAz

def plot_target_visibility(df_visible, target_name, analysis_date, min_altitude_deg):
    """
    Gera um gráfico da altitude do alvo ao longo do tempo para uma noite.
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    if not df_visible.empty:
        ax.plot(df_visible['time'], df_visible['altitude'], label=f'Altitude de {target_name}', color='royalblue')
        ax.fill_between(df_visible['time'], min_altitude_deg, df_visible['altitude'],
                        where=(df_visible['altitude'] >= min_altitude_deg),
                        color='green', alpha=0.3, label=f'Janela de Observação (>{min_altitude_deg}°)')

    ax.axhline(min_altitude_deg, color='red', linestyle='--', label=f'Elevação Mínima ({min_altitude_deg}°)')
    ax.set_ylim(0, 90)
    ax.set_xlabel(f'Hora (UTC) em {analysis_date.strftime("%Y-%m-%d")}')
    ax.set_ylabel('Altitude (graus)')
    ax.set_title(f'Visibilidade de {target_name}')
    ax.legend()
    ax.grid(True, linestyle=':', alpha=0.7)

    # Formatação do eixo de tempo
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
    fig.autofmt_xdate()

    return fig

def plot_sky_map(targets_coords, observer_location, time):
    """
    Gera um mapa do céu (plot polar) mostrando a posição dos alvos em um tempo específico.
    """
    frame = AltAz(obstime=time, location=observer_location)

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection': 'polar'})

    for name, coord in targets_coords.items():
        altaz = coord.transform_to(frame)
        if altaz.alt > 0: # Apenas plotar objetos acima do horizonte
            ax.plot(altaz.az.radian, 90 - altaz.alt.deg, 'o', label=name, markersize=10)

    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_rlim(0, 90)
    ax.set_yticks([0, 30, 60, 90])  # Definir posições dos ticks
    ax.set_yticklabels(['90° (Zênite)', '60°', '30°', '0° (Horizonte)'])
    ax.set_title(f'Mapa do Céu em {time.to_datetime():%Y-%m-%d %H:%M} UTC')
    ax.legend(bbox_to_anchor=(1.1, 1.1))
    ax.grid(True)

    return fig

def plot_yearly_visibility(df_year, target_name, year):
    """
    Gera um mapa de calor para visualizar a visibilidade de um alvo ao longo do ano.
    """
    if df_year.empty:
        print(f"Nenhum dado de visibilidade para plotar para {target_name} em {year}.")
        return None # Retornar None se não houver dados

    # Preparar os dados para o heatmap
    df_year['month'] = pd.to_datetime(df_year['date']).dt.month
    df_year['day'] = pd.to_datetime(df_year['date']).dt.day

    heatmap_data = df_year.pivot_table(index='month', columns='day', values='duration_hours')

    fig, ax = plt.subplots(figsize=(18, 7))
    sns.heatmap(heatmap_data, cmap='viridis', robust=True, ax=ax, cbar_kws={'label': 'Horas de Visibilidade'})

    ax.set_title(f'Calendário de Visibilidade para {target_name} em {year} (horas > {df_year.get("min_alt", 30)}°)')
    ax.set_xlabel('Dia do Mês')
    ax.set_ylabel('Mês')
    ax.set_yticks(ticks=np.arange(12) + 0.5, labels=[
        'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
        'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'
    ], rotation=0)

    return fig

print("Módulo de Plotagem (src/plotting.py) carregado e aprimorado.")
