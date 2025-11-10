# src/analysis.py

"""
Módulo de Análise Astronômica.

Contém as funções principais para calcular a visibilidade dos alvos,
tanto para uma única noite quanto ao longo de um ano inteiro.
"""

from .config import (
    np, pd, tqdm, u, AltAz, Time,
    get_sun, get_moon, GET_SUN_MOON_USABLE,
    datetime, timedelta, date
)

def find_event_time(altitudes_array, times_array, target_altitude, direction="rising"):
    """
    Encontra o tempo exato em que um corpo celeste cruza uma altitude específica.
    """
    # Garante que a altitude alvo seja uma quantidade da Astropy
    if not isinstance(target_altitude, u.Quantity):
        target_altitude = target_altitude * u.deg

    is_above_target = altitudes_array > target_altitude
    crossing_indices = np.where(np.diff(is_above_target))[0]

    for idx in crossing_indices:
        correct_direction = (direction == "rising" and not is_above_target[idx] and is_above_target[idx+1]) or \
                            (direction == "setting" and is_above_target[idx] and not is_above_target[idx+1])

        if correct_direction:
            t1, t2 = times_array[idx], times_array[idx+1]
            alt1, alt2 = altitudes_array[idx], altitudes_array[idx+1]

            # Interpolação linear para encontrar o tempo exato
            if (alt2 - alt1).value != 0:
                fraction = (target_altitude - alt1) / (alt2 - alt1)
                return t1 + (t2 - t1) * fraction
            else:
                return t2
    return None # Retorna None se o evento não for encontrado

def calculate_nightly_events(analysis_date, observer_location, observer_timezone):
    """
    Calcula os principais eventos da noite (pôr do sol, crepúsculos, etc.).
    """
    if not GET_SUN_MOON_USABLE:
        print("AVISO: Funções para Sol/Lua não estão disponíveis. Não é possível calcular os eventos da noite.")
        return {}

    midnight_local = observer_timezone.localize(datetime.combine(analysis_date, datetime.min.time()))
    time_grid = Time(midnight_local) + np.linspace(-12, 12, 300) * u.hour

    altaz_frame = AltAz(obstime=time_grid, location=observer_location)
    sun_altaz = get_sun(time_grid).transform_to(altaz_frame)

    events = {
        'sunset': find_event_time(sun_altaz.alt, time_grid, 0*u.deg, direction="setting"),
        'sunrise': find_event_time(sun_altaz.alt, time_grid, 0*u.deg, direction="rising"),
        'evening_astro_twilight': find_event_time(sun_altaz.alt, time_grid, -18*u.deg, direction="setting"),
        'morning_astro_twilight': find_event_time(sun_altaz.alt, time_grid, -18*u.deg, direction="rising")
    }
    return events

def analyze_target_visibility_for_night(target_coord, night_start_utc, night_end_utc, observer_location):
    """
    Calcula a trajetória de um único alvo durante uma noite.
    """
    if night_start_utc is None or night_end_utc is None or night_end_utc <= night_start_utc:
        return None, None

    night_duration = (night_end_utc - night_start_utc).to(u.hour)
    time_grid = night_start_utc + np.linspace(0, night_duration.value, 100) * u.hour

    altaz_frame = AltAz(obstime=time_grid, location=observer_location)
    target_altaz = target_coord.transform_to(altaz_frame)

    return time_grid, target_altaz

print("Módulo de Análise (src/analysis.py) carregado.")
