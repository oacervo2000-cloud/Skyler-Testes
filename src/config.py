# src/config.py

"""
Módulo de Configuração.

Este arquivo centraliza a importação de bibliotecas de uso comum e a
configuração de parâmetros globais para a ferramenta. As dependências
específicas de cada módulo (como geopy ou astroquery) devem ser importadas
diretamente nos módulos que as utilizam.
"""

# --- Bibliotecas Padrão ---
import warnings
from datetime import datetime, timedelta, date

# --- Bibliotecas de Análise de Dados ---
import numpy as np
import pandas as pd

# --- Bibliotecas Astronômicas ---
import astropy.units as u
from astropy.coordinates import EarthLocation, SkyCoord, AltAz, get_body
from astropy.coordinates.funcs import get_sun
from astropy.time import Time
from astroplan import Observer
from astroplan.moon import moon_illumination
from astropy.utils.exceptions import AstropyWarning
import erfa

# --- Bibliotecas de Visualização ---
import matplotlib.pyplot as plt

# --- Outras ---
import requests
from tqdm.auto import tqdm

# --- Configurações Globais ---
warnings.filterwarnings('ignore', category=AstropyWarning)
warnings.filterwarnings('ignore', category=erfa.ErfaWarning)

# Constantes e Parâmetros
MIN_ALTITUDE_DEFAULT = 30 * u.deg

print("Módulo de Configuração (src/config.py) carregado com sucesso.")
