# src/plotting.py

"""
Módulo de Plotagem.

Contém funções para gerar os gráficos de visibilidade e mapas celestes.
"""

from .config import plt, np, u
from matplotlib.dates import DateFormatter

def plot_target_visibility(
    target_name,
    times_local,
    target_altaz,
    night_events,
    observer_location,
    observer_timezone
):
    """
    Gera o gráfico de visibilidade (Altitude/Airmass) para um único alvo.
    """
    fig, ax1 = plt.subplots(figsize=(15, 7))

    altitudes = target_altaz.alt
    airmass = target_altaz.secz

    # --- Plotagem da Altitude ---
    color_alt = 'crimson'
    ax1.set_xlabel(f"Horário Local ({observer_timezone.zone})")
    ax1.set_ylabel('Altitude (Graus)', color=color_alt)
    ax1.plot(times_local, altitudes, color=color_alt, label=f'Altitude de {target_name}')
    ax1.tick_params(axis='y', labelcolor=color_alt)
    ax1.set_ylim(0, 90)
    ax1.grid(True, linestyle=':', alpha=0.7)

    # --- Plotagem da Airmass ---
    ax2 = ax1.twinx()
    color_air = 'dodgerblue'
    ax2.set_ylabel('Airmass', color=color_air)
    ax2.plot(times_local, airmass, color=color_air, label=f'Airmass de {target_name}')
    ax2.tick_params(axis='y', labelcolor=color_air)
    ax2.set_ylim(1, 4) # Limite razoável para airmass
    ax2.invert_yaxis()

    # --- Linhas de Eventos e Sombreamento ---
    if night_events.get('evening_astro_twilight') and night_events.get('morning_astro_twilight'):
        start_night = night_events['evening_astro_twilight'].to_datetime(observer_timezone)
        end_night = night_events['morning_astro_twilight'].to_datetime(observer_timezone)
        ax1.axvspan(start_night, end_night, alpha=0.2, color='gray', label='Noite Astronômica')

    # Formatação do eixo X
    ax1.xaxis.set_major_formatter(DateFormatter('%H:%M', tz=observer_timezone))
    fig.autofmt_xdate()

    # Título e Legenda
    analysis_date_str = times_local[0].strftime('%Y-%m-%d')
    plt.title(f"Plano de Observação para {target_name} em {analysis_date_str}", fontsize=16)
    fig.legend(loc='upper right', bbox_to_anchor=(0.9, 0.9))

    plt.show()

print("Módulo de Plotagem (src/plotting.py) carregado.")
