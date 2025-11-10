# src/location.py

"""
Módulo de Localização.
... (comentários como antes) ...
"""

# CORREÇÃO: Importar dependências diretamente, não via config.
try:
    from geopy.geocoders import Nominatim
    from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
    GEOPY_USABLE = True
except ImportError:
    # Se o geopy não estiver instalado, define uma flag para desativar a funcionalidade
    Nominatim = None
    GeocoderTimedOut = None
    GeocoderUnavailable = None
    GEOPY_USABLE = False

import pytz
from astropy import units as u
from astropy.coordinates import EarthLocation

def get_location_from_city(city_name_input, altitude_meters=None):
    """
    Tenta transformar o nome de uma cidade em coordenadas geográficas usando um serviço online.
    ... (docstring como antes) ...
    """
    if not GEOPY_USABLE:
        print("AVISO: A biblioteca 'geopy' não está disponível. Não é possível buscar a cidade pelo nome.")
        return None

    print(f"Buscando coordenadas geográficas para: '{city_name_input}'...")
    try:
        geolocator = Nominatim(user_agent="astro_planner_modular/1.0")
        location_data = geolocator.geocode(city_name_input, timeout=10)

        if location_data:
            latitude = location_data.latitude
            longitude = location_data.longitude
            altitude = altitude_meters if altitude_meters is not None else 0

            print(f"  Localização encontrada: Latitude {latitude:.4f}°, Longitude {longitude:.4f}°")
            print(f"  Altitude definida como: {altitude}m")

            return EarthLocation(lat=latitude*u.deg, lon=longitude*u.deg, height=altitude*u.m)
        else:
            print(f"  Não foi possível encontrar coordenadas para '{city_name_input}'. Verifique o nome.")
            return None

    except (GeocoderTimedOut, GeocoderUnavailable) as e:
        print(f"  Serviço de geocodificação indisponível ou demorou para responder: {e}")
        return None
    except Exception as e:
        print(f"  Ocorreu um erro inesperado ao buscar as coordenadas da cidade: {e}")
        return None

def set_location_for_uberaba():
    """
    Função de conveniência para configurar rapidamente a localização para Uberaba, MG.
    ... (docstring como antes) ...
    """
    print("Configurando localização de teste para Uberaba, MG, Brasil.")
    uberaba_lat = -19.7485
    uberaba_lon = -47.9318
    uberaba_alt = 823
    return EarthLocation(lat=uberaba_lat*u.deg, lon=uberaba_lon*u.deg, height=uberaba_alt*u.m)

def set_timezone_for_sao_paulo(location):
    """
    Define o fuso horário como 'America/Sao_Paulo' se a localização estiver na área.
    """
    # Lógica simples para verificar se está na região de São Paulo
    if -53 < location.lon.deg < -34 and -34 < location.lat.deg < 5:
        return pytz.timezone('America/Sao_Paulo')
    return None # Retorna None se estiver fora da área


print("Módulo de Localização (src/location.py) carregado.")
