# src/targets.py

"""
Módulo de Gerenciamento de Alvos.
... (comentários como antes) ...
"""
import warnings

from astroquery.simbad import Simbad
# CORREÇÃO: O nome correto da exceção é TimeoutError, não AstroqueryTimeoutError.
from astroquery.exceptions import RemoteServiceError, TimeoutError

from astropy.coordinates import SkyCoord, get_body
from astropy.time import Time
from astropy import units as u
import pandas as pd
from tqdm.auto import tqdm

DEEP_SKY_TARGETS_PRESET = [
    'M31', 'M42', 'M45', 'M13', 'M51', 'M8', 'M20',
    'Eta Carinae Nebula', '47 Tucanae', 'Omega Centauri',
    'Sirius', 'Canopus', 'Betelgeuse', 'Rigel', 'Vega'
]
SOLAR_SYSTEM_TARGETS_PRESET = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]

def get_target_skycoords(target_names_list):
    """
    Busca as coordenadas celestes (RA/Dec) para uma lista de nomes de alvos.
    """
    print(f"Buscando coordenadas para {len(target_names_list)} alvos...")
    targets_coords = {}

    simbad = Simbad()
    simbad.add_votable_fields('ra', 'dec')

    for name in tqdm(target_names_list, desc="Buscando Alvos"):
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                result_table = simbad.query_object(name)

            if result_table:
                ra = result_table['RA'][0]
                dec = result_table['DEC'][0]
                targets_coords[name] = SkyCoord(ra=ra*u.deg, dec=dec*u.deg, frame='icrs')
            else:
                targets_coords[name] = SkyCoord.from_name(name)
        except (RemoteServiceError, TimeoutError, Exception) as e:
            print(f"  AVISO: Não foi possível resolver o alvo '{name}'. Tentando fallback. Erro: {e}")
            try:
                # Se o Simbad falhar, tenta o resolver de nomes padrão do SkyCoord
                targets_coords[name] = SkyCoord.from_name(name)
            except Exception as fallback_e:
                print(f"  AVISO: Fallback também falhou para '{name}'. Erro: {fallback_e}")
                continue

    return targets_coords

def registrar_alvos_sistema_solar(observation_time):
    """
    Obtém as coordenadas dos principais corpos do sistema solar para um dado momento.
    """
    print("Obtendo posições dos alvos do Sistema Solar...")
    ss_targets = {}
    for name in tqdm(SOLAR_SYSTEM_TARGETS_PRESET, desc="Calculando Posições"):
        try:
            ss_targets[name] = get_body(name.lower(), observation_time)
        except Exception as e:
            print(f"  AVISO: Não foi possível obter coordenadas para '{name}'. Erro: {e}")
    return ss_targets

print("Módulo de Gerenciamento de Alvos (src/targets.py) carregado.")
