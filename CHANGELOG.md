# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [1.0.0] - 2025-11-24

### Adicionado
- Interface web interativa com Streamlit
- Jupyter Notebook para análises customizadas
- Análise de visibilidade noturna para múltiplos alvos
- Calendário anual de visibilidade com heatmap
- Suporte para alvos de céu profundo via SIMBAD
- Cálculo de posições de planetas e corpos do sistema solar
- Análise de impacto da Lua (iluminação e separação angular)
- Integração com API Open-Meteo para previsão meteorológica
- Geolocalização automática via nome de cidade
- Suite completa de testes com pytest
- Documentação abrangente (README, CONTRIBUTING, CODE_OF_CONDUCT)
- Configuração de CI/CD com GitHub Actions
- Licença MIT para uso educacional livre

### Módulos Implementados
- `src/config.py` - Configurações centralizadas
- `src/location.py` - Funções de geolocalização
- `src/targets.py` - Gerenciamento de alvos astronômicos
- `src/analysis.py` - Cálculos de visibilidade e eventos noturnos
- `src/plotting.py` - Visualizações (gráficos e heatmaps)

### Testes
- `tests/test_analysis.py` - Testes para módulo de análise
- `tests/test_location.py` - Testes para geolocalização
- `tests/test_targets.py` - Testes para gerenciamento de alvos

---

## [Unreleased]

### Planejado
- Tradução para inglês e espanhol
- Suporte para catálogos customizados
- Exportação de resultados em PDF
- Modo offline para uso sem internet
- App mobile (versão futura)
- Integração com telescópios automatizados

---

[1.0.0]: https://github.com/seu-usuario/Skyler-Testes/releases/tag/v1.0.0
