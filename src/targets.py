# src/targets.py

"""
Módulo de Gerenciamento de Alvos.

Contém funções para carregar, buscar e registrar alvos celestes,
sejam eles fixos (deep sky) ou objetos do Sistema Solar.
"""

import os
import warnings

# Importações do módulo de configuração
from .config import (
    u, SkyCoord, Vizier, VIZIER_USABLE,
    RemoteServiceError, AstroqueryTimeoutError,
    get_body, Time, ASTROPY_USABLE, pd, tqdm, astropy, GET_SUN_MOON_USABLE
)

def get_target_skycoords(target_names_list):
    """
    Busca coordenadas celestes e magnitude para uma lista de nomes de alvos fixos.
    """
    if not VIZIER_USABLE:
        print("AVISO: VizieR não está disponível. Não é possível buscar coordenadas.")
        return {}

    print(f"Buscando dados para {len(target_names_list)} alvos fixos...")
    targets_data_dict = {}
    vizier_tool = Vizier(columns=['_RAJ2000', '_DEJ2000', 'Vmag'], row_limit=1)

    for target_name in tqdm(target_names_list, desc="Buscando Alvos Fixos"):
        try:
            result_table = vizier_tool.query_object(target_name, catalog="SIMBAD")
            if not result_table:
                raise ValueError("Nenhum resultado encontrado no SIMBAD.")

            row = result_table[0][0]
            coord = SkyCoord(ra=row['_RAJ2000']*u.deg, dec=row['_DEJ2000']*u.deg, frame='icrs')
            vmag = row['Vmag'] if 'Vmag' in row.colnames and pd.notna(row['Vmag']) else None

            targets_data_dict[target_name] = {'coord': coord, 'magnitude': vmag, 'type': 'fixed'}
        except (RemoteServiceError, AstroqueryTimeoutError, ValueError, IndexError) as e:
            print(f"  Não foi possível resolver '{target_name}' via VizieR/SIMBAD. Tentando fallback. Erro: {e}")
            try:
                # Fallback para SkyCoord.from_name se o VizieR falhar
                coord = SkyCoord.from_name(target_name)
                targets_data_dict[target_name] = {'coord': coord, 'magnitude': None, 'type': 'fixed'}
                print(f"    Sucesso no fallback para '{target_name}'.")
            except Exception as e_fallback:
                print(f"    Falha total ao resolver '{target_name}': {e_fallback}")
                targets_data_dict[target_name] = {'coord': None, 'magnitude': None, 'type': 'fixed'}

    return targets_data_dict

def registrar_alvos_sistema_solar(ss_names_list):
    """
    Valida e prepara objetos do Sistema Solar para análise.
    """
    if not GET_SUN_MOON_USABLE:
        print("AVISO: get_body não está funcional. Não é possível registrar alvos do sistema solar.")
        return {}

    print(f"Registrando {len(ss_names_list)} alvos do Sistema Solar...")
    ss_targets_data = {}
    for name in tqdm(ss_names_list, desc="Validando Alvos do Sistema Solar"):
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                warnings.simplefilter("ignore", astropy.utils.exceptions.AstropyWarning)
                # Tenta buscar pelo nome em minúsculas, que é o padrão para planetas
                _ = get_body(name.lower(), Time.now())
                iau_name = name.lower()

            ss_targets_data[name] = {
                'name_display': name,
                'type': 'solar_system',
                'iau_name': iau_name,
                'coord': None, # Será calculado sob demanda
                'magnitude': None # Varia e não é facilmente obtido
            }
        except Exception:
            print(f"  AVISO: Não foi possível validar/registrar o objeto do sistema solar '{name}'. Verifique o nome.")

    return ss_targets_data

def load_targets_from_files(fixed_targets_file='fixed_targets.txt', ss_targets_file='ss_targets.txt'):
    """
    Carrega nomes de alvos de arquivos de texto.
    """
    all_targets_data = {}

    # Carregar alvos fixos
    if os.path.exists(fixed_targets_file):
        print(f"Lendo alvos fixos de '{fixed_targets_file}'...")
        with open(fixed_targets_file, 'r') as f:
            fixed_names = [line.strip() for line in f if line.strip()]
        if fixed_names:
            fixed_data = get_target_skycoords(fixed_names)
            all_targets_data.update(fixed_data)
    else:
        print(f"AVISO: Arquivo de alvos fixos '{fixed_targets_file}' não encontrado.")

    # Carregar alvos do sistema solar
    if os.path.exists(ss_targets_file):
        print(f"Lendo alvos do sistema solar de '{ss_targets_file}'...")
        with open(ss_targets_file, 'r') as f:
            ss_names = [line.strip() for line in f if line.strip()]
        if ss_names:
            ss_data = registrar_alvos_sistema_solar(ss_names)
            all_targets_data.update(ss_data)
    else:
        print(f"AVISO: Arquivo de alvos do sistema solar '{ss_targets_file}' não encontrado.")

    return all_targets_data

print("Módulo de Gerenciamento de Alvos (src/targets.py) carregado.")
