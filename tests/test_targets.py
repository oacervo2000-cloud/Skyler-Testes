# tests/test_targets.py

import pytest
from astropy.coordinates import SkyCoord
from astropy import units as u

from src.targets import get_target_skycoords, registrar_alvos_sistema_solar

def test_get_target_skycoords_single_target():
    """
    Testa se a função retorna as coordenadas corretas para um único alvo conhecido.
    """
    targets = get_target_skycoords(['Sirius'])
    assert 'Sirius' in targets
    assert isinstance(targets['Sirius'], SkyCoord)
    # Coordenadas de Sirius (aproximadas)
    assert u.isclose(targets['Sirius'].ra, 101.28 * u.deg, atol=1 * u.deg)
    assert u.isclose(targets['Sirius'].dec, -16.71 * u.deg, atol=1 * u.deg)

def test_get_target_skycoords_multiple_targets():
    """
    Testa o processamento de uma lista de alvos.
    """
    target_names = ['Sirius', 'Betelgeuse']
    targets = get_target_skycoords(target_names)
    assert len(targets) == 2
    assert 'Sirius' in targets
    assert 'Betelgeuse' in targets

def test_get_target_skycoords_invalid_target():
    """
    Testa se alvos inválidos são ignorados e um aviso é gerado (o aviso não é testado aqui,
    apenas que o alvo inválido não está no resultado).
    """
    target_names = ['Sirius', 'AlvoInexistente123']
    targets = get_target_skycoords(target_names)
    assert len(targets) == 1
    assert 'Sirius' in targets
    assert 'AlvoInexistente123' not in targets

def test_registrar_alvos_sistema_solar():
    """
    Testa se a função do sistema solar retorna um dicionário de SkyCoord.
    """
    from astropy.time import Time

    # Precisa de um tempo para obter as coordenadas dos corpos do sistema solar
    observation_time = Time('2023-01-01T00:00:00')

    ss_targets = registrar_alvos_sistema_solar(observation_time)

    assert isinstance(ss_targets, dict)
    assert 'Mars' in ss_targets  # Verificar se um planeta conhecido está presente
    assert 'Moon' in ss_targets
    assert isinstance(ss_targets['Mars'], SkyCoord)
