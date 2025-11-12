# create_notebook.py
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

# Construir o notebook célula por célula com listas de strings
nb = new_notebook()
nb.cells = [
    new_markdown_cell([
        "# Ferramenta de Análise Astronômica (Jupyter Notebook)\\n",
        "Bem-vindo à versão Jupyter..."
    ]),
    new_code_cell([
        "import warnings\\n",
        "from datetime import date\\n",
        "import pytz, csv, os\\n",
        "from src.config import *\\n",
        "from src.location import *\\n",
        "from src.targets import *\\n",
        "from src.analysis import *\\n",
        "from src.plotting import *\\n",
        "warnings.filterwarnings('ignore', category=AstropyWarning)\\n",
        "print(\\\"Módulos carregados.\\\")"
    ]),
    new_markdown_cell([
        "---",
        "## ⚙️ 2. Configurações da Análise"
    ]),
    new_code_cell([
        "from datetime import date\\n",
        "NOME_DA_CIDADE = \\"Vitória da Conquista, Brazil\\"\\n",
        "DATA_ANALISE = date(2024, 7, 15)\\n",
        "ELEVACAO_MINIMA_GRAUS = 30\\n",
        "usar_alvos_predefinidos = True\\n",
        "usar_alvos_sistema_solar = True\\n",
        "alvos_manuais = [\\"NGC 5128\\", \\"M83\\"]\\n",
        "ARQUIVO_DE_ALVOS = \\"targets.csv\\"\\n",
        "ALVO_ANUAL = \\"M42\\"\\n",
        "ANO_ANALISE = 2024"
    ]),
    new_markdown_cell([
        "---",
        "## 🌙 3. Execução da Análise Noturna"
    ]),
    new_code_cell([
        "observer_location = get_location_from_city(NOME_DA_CIDADE)\\n",
        "observer_timezone = set_timezone_for_sao_paulo(observer_location) or pytz.UTC\\n",
        "if observer_location is not None:\\n",
        "    night_events = calculate_nightly_events(DATA_ANALISE, observer_location, observer_timezone)\\n",
        "    start_night, end_night = night_events['inicio_noite'], night_events['fim_noite']\\n",
        "    nomes_alvos = []\\n",
        "    if usar_alvos_predefinidos: nomes_alvos.extend(DEEP_SKY_TARGETS_PRESET)\\n",
        "    if alvos_manuais: nomes_alvos.extend(alvos_manuais)\\n",
        "    if ARQUIVO_DE_ALVOS:\\n",
        "        if ARQUIVO_DE_ALVOS.endswith('.txt'):\\n",
        "            with open(ARQUIVO_DE_ALVOS, 'r') as f:\\n",
        "                nomes_alvos.extend([l.strip() for l in f if l.strip() and not l.startswith('#')])\\n",
        "        elif ARQUIVO_DE_ALVOS.endswith('.csv'):\\n",
        "            with open(ARQUIVO_DE_ALVOS, 'r') as f:\\n",
        "                reader = csv.DictReader(f)\\n",
        "                nomes_alvos.extend([row['alvo'] for row in reader if 'alvo' in row])\\n",
        "    all_targets = {}\\n",
        "    if nomes_alvos: all_targets.update(get_target_skycoords(nomes_alvos))\\n",
        "    if usar_alvos_sistema_solar: all_targets.update(registrar_alvos_sistema_solar(start_night))\\n",
        "    for name, coord in all_targets.items():\\n",
        "        if coord is not None:\\n",
        "            df = analyze_target_visibility_for_night(start_night, end_night, observer_location, coord, ELEVACAO_MINIMA_GRAUS * u.deg)\\n",
        "            fig = plot_target_visibility(df, name, DATA_ANALISE, ELEVACAO_MINIMA_GRAUS)\\n",
        "            plt.show()"
    ]),
    new_markdown_cell([
        "---",
        "## 📅 4. Execução da Análise Anual"
    ]),
    new_code_cell([
        "if observer_location is not None and ALVO_ANUAL:\\n",
        "    target_coords = get_target_skycoords([ALVO_ANUAL])\\n",
        "    if ALVO_ANUAL in target_coords:\\n",
        "        df_year = analyze_year_visibility(ANO_ANALISE, observer_location, observer_timezone, target_coords[ALVO_ANUAL], ELEVACAO_MINIMA_GRAUS * u.deg)\\n",
        "        fig = plot_yearly_visibility(df_year, ALVO_ANUAL, ANO_ANALISE)\\n",
        "        plt.show()"
    ])
]

nb['metadata'] = {
    'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
    'language_info': {'name': 'python', 'version': '3.12.12'}
}

with open('analise_astronomica.ipynb', 'w') as f:
    nbformat.write(nb, f)

print("Notebook recriado com sucesso usando a abordagem de listas de strings.")
