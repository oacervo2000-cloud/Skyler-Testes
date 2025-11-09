# src/location.py

"""
Módulo de Localização.

Este arquivo contém as funções para definir a localização do observador,
seja através do nome da cidade ou por coordenadas geográficas diretas.
"""

# Importa as bibliotecas e configurações necessárias do módulo de configuração
from .config import u, EarthLocation, Nominatim, GeocoderTimedOut, GeocoderUnavailable, GEOPY_USABLE

def get_location_from_city(city_name_input, altitude_meters=None):
    """
    Transforma o nome de uma cidade em coordenadas geográficas (latitude, longitude, altitude).

    Parâmetros:
        city_name_input (str): O nome da cidade (ex: "Uberaba, Brasil").
        altitude_meters (float, opcional): A altitude em metros. Se não for fornecida, será usada 0.

    Retorna:
        EarthLocation: Objeto da Astropy com as coordenadas da cidade, ou None se não for encontrada.
    """
    if not GEOPY_USABLE:
        print("AVISO: geopy não está disponível. Não é possível buscar a cidade pelo nome.")
        return None

    print(f"Buscando coordenadas para: '{city_name_input}'...")
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
            print(f"  Não foi possível encontrar coordenadas para '{city_name_input}'.")
            return None

    except (GeocoderTimedOut, GeocoderUnavailable) as e:
        print(f"  Serviço de geocodificação indisponível: {e}")
        return None
    except Exception as e:
        print(f"  Ocorreu um erro inesperado ao buscar a cidade: {e}")
        return None

def set_location_for_uberaba():
    """
    Função de conveniência para configurar a localização para Uberaba, MG, para os testes.
    """
    print("Configurando localização de teste para Uberaba, MG, Brasil.")
    # Coordenadas aproximadas de Uberaba e altitude
    uberaba_lat = -19.7485
    uberaba_lon = -47.9318
    uberaba_alt = 823 # metros

    return EarthLocation(lat=uberaba_lat*u.deg, lon=uberaba_lon*u.deg, height=uberaba_alt*u.m)

def set_timezone_for_sao_paulo():
    """
    Função de conveniência para configurar o fuso horário para 'America/Sao_Paulo'.
    """
    try:
        from .config import pytz
        print("Configurando fuso horário de teste para 'America/Sao_Paulo'.")
        return pytz.timezone('America/Sao_Paulo')
    except Exception as e:
        print(f"ERRO ao configurar o fuso horário de teste: {e}")
        return None

print("Módulo de Localização (src/location.py) carregado.")
