# create_notebook.py
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

# Construir o notebook célula por célula
nb = new_notebook()
nb.cells = [
    new_markdown_cell("""# Ferramenta de Análise Astronômica (Jupyter Notebook)

Bem-vindo à versão Jupyter Notebook da **Ferramenta de Análise Astronômica**!

Este notebook permite que você planeje observações astronômicas de forma interativa, personalizável e integrada com seus próprios scripts Python.

---

## 🚀 Como Usar Este Notebook

1. **Configure suas preferências** na seção 2
2. **Execute as células sequencialmente** (Shift+Enter)
3. **Analise os resultados visuais** gerados automaticamente

---

## 📚 1. Importação de Módulos
"""),
    new_code_cell("""import warnings
from datetime import date
import pytz, csv, os
from src.config import *
from src.location import *
from src.targets import *
from src.analysis import *
from src.plotting import *
warnings.filterwarnings('ignore', category=AstropyWarning)
print("Módulos carregados com sucesso!")"""),
    
    new_markdown_cell("""---

## ⚙️ 2. Configurações da Análise

Edite as variáveis abaixo conforme suas necessidades:
"""),
    
    new_code_cell("""from datetime import date

# Localização do observador
NOME_DA_CIDADE = "Vitória da Conquista, Brazil"

# Data para análise noturna
DATA_ANALISE = date(2024, 7, 15)

# Elevação mínima do alvo acima do horizonte (em graus)
ELEVACAO_MINIMA_GRAUS = 30

# Seleção de alvos
usar_alvos_predefinidos = True
usar_alvos_sistema_solar = True
alvos_manuais = ["NGC 5128", "M83"]

# Arquivo de alvos (opcional)
ARQUIVO_DE_ALVOS = None  # Ou "targets.csv" se tiver um arquivo

# Configurações para análise anual
ALVO_ANUAL = "M42"
ANO_ANALISE = 2024

print("✅ Configurações definidas!")"""),
    
    new_markdown_cell("""---

## 🌙 3. Execução da Análise Noturna

Esta seção analisa a visibilidade de múltiplos alvos durante a noite selecionada.
"""),
    
    new_code_cell("""# Obter localização do observador
observer_location = get_location_from_city(NOME_DA_CIDADE)
observer_timezone = set_timezone_for_sao_paulo(observer_location) or pytz.UTC

if observer_location is not None:
    # Calcular eventos noturnos
    night_events = calculate_nightly_events(DATA_ANALISE, observer_location, observer_timezone)
    start_night, end_night = night_events['inicio_noite'], night_events['fim_noite']
    
    print(f"📅 Análise para: {DATA_ANALISE}")
    print(f"🌅 Pôr do Sol: {night_events['por_do_sol'].to_datetime():%H:%M UTC}")
    print(f"🌌 Início da Noite: {start_night.to_datetime():%H:%M UTC}")
    print(f"🌄 Fim da Noite: {end_night.to_datetime():%H:%M UTC}")
    print()
    
    # Coletar nomes de alvos
    nomes_alvos = []
    if usar_alvos_predefinidos:
        nomes_alvos.extend(DEEP_SKY_TARGETS_PRESET)
    if alvos_manuais:
        nomes_alvos.extend(alvos_manuais)
    if ARQUIVO_DE_ALVOS and os.path.exists(ARQUIVO_DE_ALVOS):
        if ARQUIVO_DE_ALVOS.endswith('.txt'):
            with open(ARQUIVO_DE_ALVOS, 'r') as f:
                nomes_alvos.extend([l.strip() for l in f if l.strip() and not l.startswith('#')])
        elif ARQUIVO_DE_ALVOS.endswith('.csv'):
            with open(ARQUIVO_DE_ALVOS, 'r') as f:
                reader = csv.DictReader(f)
                nomes_alvos.extend([row['alvo'] for row in reader if 'alvo' in row])
    
    # Buscar coordenadas
    all_targets = {}
    if nomes_alvos:
        all_targets.update(get_target_skycoords(nomes_alvos))
    if usar_alvos_sistema_solar:
        all_targets.update(registrar_alvos_sistema_solar(start_night))
    
    # Analisar e plotar cada alvo
    print(f"\\n🔭 Analisando {len(all_targets)} alvos...\\n")
    for name, coord in all_targets.items():
        if coord is not None:
            df = analyze_target_visibility_for_night(
                start_night, end_night, observer_location, coord, ELEVACAO_MINIMA_GRAUS * u.deg
            )
            
            if not df.empty:
                print(f"✅ {name}: Visível!")
                fig = plot_target_visibility(df, name, DATA_ANALISE, ELEVACAO_MINIMA_GRAUS)
                plt.show()
            else:
                print(f"❌ {name}: Não visível acima de {ELEVACAO_MINIMA_GRAUS}°")
else:
    print("❌ Não foi possível obter a localização. Verifique o nome da cidade.")"""),
    
    new_markdown_cell("""---

## 📅 4. Execução da Análise Anual

Esta seção gera um calendário de visibilidade para um alvo específico ao longo de um ano inteiro.

**Atenção:** Esta análise pode levar alguns minutos para ser concluída.
"""),
    
    new_code_cell("""if observer_location is not None and ALVO_ANUAL:
    # Buscar coordenadas do alvo
    target_coords = get_target_skycoords([ALVO_ANUAL])
    
    if ALVO_ANUAL in target_coords and target_coords[ALVO_ANUAL] is not None:
        print(f"🔭 Analisando visibilidade anual de {ALVO_ANUAL} para {ANO_ANALISE}...")
        
        # Análise anual
        df_year = analyze_year_visibility(
            ANO_ANALISE, observer_location, observer_timezone, 
            target_coords[ALVO_ANUAL], ELEVACAO_MINIMA_GRAUS * u.deg
        )
        
        if not df_year.empty:
            print(f"\\n✅ {ALVO_ANUAL} foi visível em {len(df_year)} noites durante {ANO_ANALISE}!")
            
            # Gerar heatmap
            fig = plot_yearly_visibility(df_year, ALVO_ANUAL, ANO_ANALISE)
            if fig:
                plt.show()
            
            # Estatísticas
            print(f"\\n📊 Estatísticas:")
            print(f"  - Noites visíveis: {len(df_year)}")
            print(f"  - Duração média: {df_year['duration_hours'].mean():.2f} horas")
            print(f"  - Duração máxima: {df_year['duration_hours'].max():.2f} horas")
        else:
            print(f"❌ {ALVO_ANUAL} não foi visível em nenhuma noite de {ANO_ANALISE}")
    else:
        print(f"❌ Não foi possível encontrar o alvo '{ALVO_ANUAL}'")
else:
    print("❌ Localização ou alvo anual não definidos")"""),
    
    new_markdown_cell("""---

## 🎓 Próximos Passos

- Experimente diferentes datas e localizações
- Adicione seus próprios alvos na lista `alvos_manuais`
- Ajuste a elevação mínima conforme suas condições de observação
- Explore o código-fonte em `src/` para entender os cálculos

**Boas observações! 🔭✨**
""")
]

# Adicionar metadados do kernel
nb['metadata'] = {
    'kernelspec': {
        'display_name': 'Python 3',
        'language': 'python',
        'name': 'python3'
    },
    'language_info': {
        'name': 'python',
        'version': '3.8'
    }
}

# Escrever o notebook
with open('analise_astronomica.ipynb', 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)

print("✅ Notebook 'analise_astronomica.ipynb' criado com sucesso!")
