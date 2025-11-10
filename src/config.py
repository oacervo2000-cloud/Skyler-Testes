# src/config.py

"""
Módulo de Configuração Central.

Este arquivo contém todas as importações de bibliotecas externas e as configurações
globais que são utilizadas em múltiplos módulos do projeto.
"""

# --- Importações de Bibliotecas Essenciais ---

import warnings
import numpy as np
import pandas as pd
import pytz
import requests
from datetime import datetime, timedelta, date
from tqdm.auto import tqdm

# --- Importações do Matplotlib ---
import matplotlib.pyplot as plt

# --- Importações do AstroPy e correlatas ---
try:
    import astropy
    from astropy.coordinates import EarthLocation, SkyCoord, AltAz, get_body
    from astropy.time import Time
    import astropy.units as u
    from astropy.utils.iers import conf as iers_conf

    import astroplan
    from astroplan import Observer, FixedTarget
    from astroplan.plots import plot_sky, plot_airmass
    from astroplan import moon_illumination

    from astroquery.vizier import Vizier
    from astroquery.exceptions import RemoteServiceError, TimeoutError as AstroqueryTimeoutError

    # Desativa o download automático de dados IERS para evitar problemas de conexão
    iers_conf.auto_download = False
    # Suprime avisos comuns da Astropy que podem poluir a saída
    warnings.filterwarnings('ignore', category=astropy.utils.exceptions.AstropyWarning)

    ASTROPY_USABLE = True
    ASTROPLAN_USABLE = True
    VIZIER_USABLE = True

except ImportError:
    print("AVISO CRÍTICO: Uma ou mais bibliotecas astronômicas (astropy, astroplan, astroquery) não foram encontradas.")
    ASTROPY_USABLE = False
    ASTROPLAN_USABLE = False
    VIZIER_USABLE = False

# --- Importações do Geopy ---
try:
    from geopy.geocoders import Nominatim
    from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
    GEOPY_USABLE = True
except ImportError:
    print("AVISO: Biblioteca 'geopy' não encontrada. A busca de localização por nome de cidade será desabilitada.")
    GEOPY_USABLE = False

# --- Configurações de Funções Globais ---

# Define as funções para obter as posições do Sol e da Lua
if ASTROPY_USABLE:
    try:
        # A função get_body é a forma moderna e preferencial
        get_sun = lambda time_obj: get_body("sun", time_obj)
        get_moon = lambda time_obj: get_body("moon", time_obj)
        # Testa rapidamente para garantir que funciona
        _ = get_sun(Time.now())
        GET_SUN_MOON_USABLE = True
    except Exception as e:
        print(f"ERRO CRÍTICO ao configurar as funções para Sol/Lua: {e}")
        get_sun = None
        get_moon = None
        GET_SUN_MOON_USABLE = False
else:
    get_sun = None
    get_moon = None
    GET_SUN_MOON_USABLE = False

# --- Configurações de Plotagem ---
plt.style.use('seaborn-v0_8-whitegrid')

print("Módulo de Configuração (src/config.py) carregado.")
