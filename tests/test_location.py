# tests/test_location.py

import pytest
from astropy.coordinates import EarthLocation
from astropy import units as u
import pytz

from src.location import get_location_from_city, set_timezone_for_sao_paulo

def test_get_location_from_city_success():
    """
    Testa se a função retorna um objeto EarthLocation válido para uma cidade conhecida.
    """
    city = "São Paulo, Brazil"
    location = get_location_from_city(city)

    assert isinstance(location, EarthLocation)
    assert u.isclose(location.lat, -23.55 * u.deg, atol=1 * u.deg)
    assert u.isclose(location.lon, -46.63 * u.deg, atol=1 * u.deg)

def test_get_location_from_city_not_found():
    """
    Testa se a função retorna None para uma cidade inexistente.
    """
    # CORREÇÃO: A função retorna None, não levanta uma exceção.
    location = get_location_from_city("CidadeInexistente12345")
    assert location is None

def test_set_timezone_for_sao_paulo_inside():
    """
    Testa se o fuso horário correto é retornado para uma localização dentro da área.
    """
    location_sp = EarthLocation(lat=-23.55 * u.deg, lon=-46.63 * u.deg)
    tz = set_timezone_for_sao_paulo(location_sp)

    assert tz is not None
    assert tz == pytz.timezone('America/Sao_Paulo')

def test_set_timezone_for_sao_paulo_outside():
    """
    Testa se None é retornado para uma localização fora da área.
    """
    location_lisbon = EarthLocation(lat=38.72 * u.deg, lon=-9.13 * u.deg)
    tz = set_timezone_for_sao_paulo(location_lisbon)

    assert tz is None
