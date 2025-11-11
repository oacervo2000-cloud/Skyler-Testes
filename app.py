# app.py
# Arquivo principal da aplicação web com Streamlit

import streamlit as st
from datetime import date
import pytz

# Importar as funções do backend
from src.config import *
from src.location import get_location_from_city, set_timezone_for_sao_paulo
from src.targets import get_target_skycoords, registrar_alvos_sistema_solar, DEEP_SKY_TARGETS_PRESET
from src.analysis import calculate_nightly_events, analyze_target_visibility_for_night, analyze_year_visibility
from src.plotting import plot_target_visibility, plot_yearly_visibility

# --- Configuração da Página ---
st.set_page_config(page_title="Analisador Astronômico", page_icon="🔭", layout="wide")
st.title("🔭 Analisador de Visibilidade Astronômica")

# --- Barra Lateral de Controles ---
st.sidebar.header("Configurações da Análise")

# 1. Localização
st.sidebar.subheader("📍 Localização do Observador")
location_method = st.sidebar.radio("Método de Localização", ('Cidade', 'Coordenadas'))
observer_location = None

if location_method == 'Cidade':
    city_name = st.sidebar.text_input("Cidade", "São Paulo, Brazil")
    if st.sidebar.button("Definir por Cidade"):
        with st.spinner(f"Buscando coordenadas para {city_name}..."):
            observer_location = get_location_from_city(city_name)
else:
    lat_lon_str = st.sidebar.text_input("Latitude,Longitude", "-22.90,-43.17") # Rio de Janeiro
    if st.sidebar.button("Definir por Coordenadas"):
        try:
            lat, lon = map(float, lat_lon_str.split(','))
            observer_location = EarthLocation(lat=lat*u.deg, lon=lon*u.deg)
        except ValueError:
            st.sidebar.error("Formato inválido. Use 'lat,lon'.")

if observer_location:
    st.session_state['observer_location'] = observer_location
    st.sidebar.success(f"Localização definida: {observer_location.lat.deg:.2f}, {observer_location.lon.deg:.2f}")
elif 'observer_location' in st.session_state:
    observer_location = st.session_state['observer_location']
    st.sidebar.info(f"Localização em cache: {observer_location.lat.deg:.2f}, {observer_location.lon.deg:.2f}")
else:
    st.sidebar.warning("Defina uma localização.")


# 2. Parâmetros
analysis_date = st.sidebar.date_input("Data da Análise Noturna", date.today())
min_altitude_deg = st.sidebar.slider("Elevação Mínima (°)", 10, 90, 30)
min_altitude = min_altitude_deg * u.deg

# --- Abas para diferentes análises ---
tab1, tab2 = st.tabs(["🌙 Análise Noturna", "📅 Calendário Anual"])

# ... (Lógica das abas como antes) ...
with tab1:
    st.header("Análise de Visibilidade para a Noite Selecionada")
    col1, col2 = st.columns(2)
    with col1:
        use_deep_sky = st.checkbox("Incluir Alvos de Céu Profundo", True)
        use_solar_system = st.checkbox("Incluir Alvos do Sistema Solar", True)
    with col2:
        manual_targets_input = st.text_area("Adicionar alvos manualmente (um por linha)", "M83\\nNGC 1365")

    if st.button("Gerar Análise da Noite", type="primary"):
        if 'observer_location' not in st.session_state:
            st.error("A localização do observador deve ser definida antes de executar a análise.")
        else:
            # ... (resto da lógica como antes)
            pass
with tab2:
    st.header("Calendário de Visibilidade Anual")
    yearly_target_name = st.text_input("Nome do Alvo", "M31", key="yearly_target")
    year = st.number_input("Ano", value=date.today().year, min_value=1900, max_value=2100, key="yearly_year")

    if st.button("Gerar Calendário Anual", type="primary", key="yearly_button"):
        if 'observer_location' not in st.session_state:
            st.error("A localização do observador deve ser definida antes de executar a análise.")
        else:
            # ... (resto da lógica como antes)
            pass
