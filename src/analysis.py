# src/analysis.py

"""
Módulo de Análise Astronômica.
... (comentários como antes) ...
"""
from astroplan import Observer
from .config import (
    np, pd, u, AltAz, Time, requests, get_sun, get_body,
    datetime, timedelta, date, moon_illumination, tqdm, erfa
)

def calculate_nightly_events(analysis_date, observer_location, observer_timezone):
    """
    Calcula os horários do pôr do sol, crepúsculo astronômico e nascer do sol.
    """
    try:
        observer = Observer(location=observer_location, timezone=observer_timezone)
        time_midday = Time(f"{analysis_date.strftime('%Y-%m-%d')} 12:00:00")

        # CORREÇÃO: Remover a chamada .astimezone(). O Observer já retorna o tempo no fuso correto.
        sunset_time = observer.sun_set_time(time_midday, which='next')
        sunrise_time = observer.sun_rise_time(time_midday, which='next')
        evening_astro_twilight = observer.twilight_evening_astronomical(time_midday, which='next')
        morning_astro_twilight = observer.twilight_morning_astronomical(time_midday, which='next')
        midnight_time = observer.midnight(time_midday, which='next')

        return {
            "inicio_noite": evening_astro_twilight,
            "fim_noite": morning_astro_twilight,
            "por_do_sol": sunset_time,
            "nascer_do_sol": sunrise_time,
            "meia_noite_real": midnight_time
        }
    except Exception as e:
        print(f"Aviso: Não foi possível calcular os eventos noturnos para {analysis_date}. Erro: {e}")
        return {}

def analyze_target_visibility_for_night(start_time, end_time, observer_location, target_coord, min_altitude):
    """
    Calcula a altitude de um alvo ao longo de uma noite.
    """
    time_range = pd.date_range(start=start_time.to_datetime(), end=end_time.to_datetime(), freq='5min')
    if time_range.empty:
        return pd.DataFrame()

    times_astro = Time(time_range)
    frame = AltAz(obstime=times_astro, location=observer_location)
    target_altaz = target_coord.transform_to(frame)

    df = pd.DataFrame({'time': time_range, 'altitude': target_altaz.alt.deg})
    df_visible = df[df['altitude'] >= min_altitude.value].copy()
    return df_visible

def check_hemisphere_visibility(observer_location, target_coord):
    """
    Verifica se um alvo é potencialmente visível do hemisfério do observador.
    """
    observer_lat = observer_location.lat.deg
    target_dec = target_coord.dec.deg
    if (observer_lat > 0 and target_dec < -30) or (observer_lat < 0 and target_dec > 30):
        return False
    return True

def analyze_moon_impact(time, observer_location, target_coord):
    """
    Calcula a iluminação da Lua e sua separação angular de um alvo.
    """
    moon = get_body("moon", time, location=observer_location)
    frame = AltAz(obstime=time, location=observer_location)

    illum = moon_illumination(time) * 100
    separation = moon.separation(target_coord)

    return {
        "moon_illumination": illum,
        "moon_separation": separation
    }

def get_weather_forecast(lat, lon):
    """
    Obtém a previsão do tempo para 7 dias usando a API Open-Meteo.
    """
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=cloudcover&forecast_days=2"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        hourly_data = pd.DataFrame(data['hourly'])
        hourly_data['time'] = pd.to_datetime(hourly_data['time'])

        now = datetime.now()
        start_night = datetime(now.year, now.month, now.day, 18)
        if now.hour > 18: start_night += timedelta(days=1)
        end_night = start_night + timedelta(hours=12)

        night_forecast = hourly_data[(hourly_data['time'] >= start_night) & (hourly_data['time'] <= end_night)]

        if not night_forecast.empty:
            avg_cloud_cover = night_forecast['cloudcover'].mean()
            return f"{avg_cloud_cover:.1f}%"
    except Exception:
        return "N/A"
    return "N/A"

def analyze_year_visibility(year, observer_location, observer_timezone, target_coord, min_altitude):
    """
    Analisa a visibilidade de um alvo para cada noite de um ano inteiro.
    """
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)
    results = []

    for day_offset in tqdm(range((end_date - start_date).days + 1), desc=f"Analisando {year}", unit="dia"):
        current_date = start_date + timedelta(days=day_offset)
        with np.errstate(all='ignore'):
            night_events = calculate_nightly_events(current_date, observer_location, observer_timezone)

        if not night_events or not night_events.get("inicio_noite") or not night_events.get("fim_noite"): continue
        start_night, end_night = night_events["inicio_noite"], night_events["fim_noite"]
        if start_night >= end_night: continue

        df_visible = analyze_target_visibility_for_night(start_night, end_night, observer_location, target_coord, min_altitude)

        if not df_visible.empty:
            duration = (df_visible['time'].iloc[-1] - df_visible['time'].iloc[0]).total_seconds() / 3600.0
            results.append({
                'date': pd.to_datetime(current_date),
                'start_time': df_visible['time'].iloc[0],
                'end_time': df_visible['time'].iloc[-1],
                'duration_hours': duration
            })
    return pd.DataFrame(results)

print("Módulo de Análise (src/analysis.py) carregado e aprimorado.")
