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
observer_location = None
city_name = st.sidebar.text_input("Cidade", "São Paulo, Brazil")
if st.sidebar.button("Definir Localização"):
    with st.spinner(f"Buscando coordenadas para {city_name}..."):
        observer_location = get_location_from_city(city_name)

if observer_location:
    st.session_state['observer_location'] = observer_location
    st.sidebar.success(f"Localização: {observer_location.lat.deg:.2f}, {observer_location.lon.deg:.2f}")
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

# --- Lógica da Aba de Análise Noturna ---
with tab1:
    # CORREÇÃO: Adicionar conteúdo indentado a este bloco.
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
            observer_location = st.session_state['observer_location']
            with st.spinner("Calculando..."):
                observer_timezone = set_timezone_for_sao_paulo(observer_location) or pytz.UTC
                night_events = calculate_nightly_events(analysis_date, observer_location, observer_timezone)
                if not night_events:
                    st.error("Não foi possível calcular os eventos noturnos.")
                else:
                    start_night, end_night = night_events['inicio_noite'], night_events['fim_noite']
                    st.success(f"Janela de observação: {start_night.to_datetime(observer_timezone).strftime('%H:%M')} a {end_night.to_datetime(observer_timezone).strftime('%H:%M')}")

                    all_targets = {}
                    names_to_fetch = []
                    if use_deep_sky: names_to_fetch.extend(DEEP_SKY_TARGETS_PRESET)
                    if manual_targets_input: names_to_fetch.extend([n.strip() for n in manual_targets_input.split('\\n') if n.strip()])
                    if names_to_fetch: all_targets.update(get_target_skycoords(names_to_fetch))
                    if use_solar_system: all_targets.update(registrar_alvos_sistema_solar(start_night))

                    if not all_targets:
                        st.warning("Nenhum alvo selecionado.")
                    else:
                        st.subheader("Gráficos de Visibilidade")
                        for name, coord in all_targets.items():
                            if coord:
                                with st.container(border=True):
                                    df_visibility = analyze_target_visibility_for_night(start_night, end_night, observer_location, coord, min_altitude)
                                    fig = plot_target_visibility(df_visibility, name, analysis_date, min_altitude_deg)
                                    st.pyplot(fig)
                            else:
                                st.warning(f"Coordenadas não encontradas para {name}.")

# --- Lógica da Aba de Análise Anual ---
with tab2:
    st.header("Calendário de Visibilidade Anual")
    yearly_target_name = st.text_input("Nome do Alvo", "M31", key="yearly_target")
    year = st.number_input("Ano", value=date.today().year, min_value=1900, max_value=2100, key="yearly_year")

    if st.button("Gerar Calendário Anual", type="primary", key="yearly_button"):
        if 'observer_location' not in st.session_state:
            st.error("A localização do observador deve ser definida antes de executar a análise.")
        else:
            observer_location = st.session_state['observer_location']
            with st.spinner(f"Analisando '{yearly_target_name}' para {year}..."):
                target_coords_dict = get_target_skycoords([yearly_target_name])
                if not target_coords_dict or yearly_target_name not in target_coords_dict:
                    st.error(f"Não foi possível encontrar '{yearly_target_name}'.")
                else:
                    target_coord = target_coords_dict[yearly_target_name]
                    observer_timezone = set_timezone_for_sao_paulo(observer_location) or pytz.UTC
                    df_year = analyze_year_visibility(year, observer_location, observer_timezone, target_coord, min_altitude)
                    if df_year.empty:
                        st.warning(f"Nenhum período de visibilidade encontrado para '{yearly_target_name}'.")
                    else:
                        st.success("Análise anual concluída!")
                        fig = plot_yearly_visibility(df_year, yearly_target_name, year)
                        st.pyplot(fig)
