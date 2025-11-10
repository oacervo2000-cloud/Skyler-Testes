# 🔭 Analisador de Visibilidade Astronômica

Este repositório contém uma ferramenta avançada para planejamento de observações astronômicas, construída com uma arquitetura modular em Python. A ferramenta permite que astrônomos amadores e profissionais analisem a visibilidade de corpos celestes (alvos de céu profundo e do sistema solar) a partir de qualquer localização na Terra.

O projeto oferece duas interfaces principais para interagir com a análise:
1.  Uma **aplicação web interativa** construída com Streamlit para uma experiência de usuário amigável.
2.  Um **Jupyter Notebook** detalhado para análises mais aprofundadas e personalizadas.

## Funcionalidades Principais
-   **Análise Noturna Detalhada**: Gere gráficos de altitude vs. tempo para múltiplos alvos em uma noite específica.
-   **Calendário de Visibilidade Anual**: Crie um mapa de calor visual para identificar as melhores noites para observar um alvo ao longo de um ano.
-   **Localização Flexível**: Defina sua localização pelo nome da cidade ou por coordenadas.
-   **Seleção de Alvos Abrangente**: Use listas pré-selecionadas, adicione alvos do sistema solar ou insira manualmente qualquer objeto.
-   **Considerações Atmosféricas**: Configure a elevação mínima do alvo acima do horizonte.

## Estrutura do Projeto
-   `app.py`: Ponto de entrada para a aplicação web Streamlit.
-   `analise_astronomica.ipynb`: Jupyter Notebook para análises interativas.
-   `requirements.txt`: Lista de todas as dependências.
-   `src/`: Código backend modularizado (config, location, targets, analysis, plotting).
-   `tests/`: Suíte de testes (pytest) para garantir a robustez do código.

## Como Usar

### 1. Pré-requisitos
-   Python 3.8 ou superior.
-   `pip` (gerenciador de pacotes do Python).

### 2. Instalação
Clone o repositório e instale as dependências:
```bash
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_REPOSITORIO>
pip install -r requirements.txt
```

### 3. Executando a Aplicação Web (Recomendado)
A maneira mais fácil de usar a ferramenta é através da aplicação Streamlit. No terminal, execute:
```bash
streamlit run app.py
```
Isso iniciará um servidor local e abrirá a aplicação no seu navegador.

---

## Tutorial Passo a Passo da Aplicação Web

Ao abrir a aplicação, você verá a interface principal. O uso é dividido em duas partes: a barra lateral de configuração e as abas de análise.

### Passo 1: Configurar a Localização e Data

1.  **Defina sua Localização**: Na barra lateral esquerda, em **📍 Localização do Observador**, digite o nome da sua cidade (ex: "Lisboa, Portugal") e clique no botão **Definir Localização**. A aplicação buscará as coordenadas e confirmará com uma mensagem de sucesso.
2.  **Ajuste a Data (para Análise Noturna)**: Em **Data da Análise Noturna**, selecione a data para a qual deseja planejar suas observações.
3.  **Defina a Elevação Mínima**: Use o slider **Elevação Mínima (°) ** para definir a altitude mínima que um objeto deve ter no céu para ser considerado "observável". O padrão é 30°, um bom valor para evitar a turbulência atmosférica próxima ao horizonte.

### Passo 2: Executar uma Análise Noturna

Esta análise é ideal para ver o que estará visível em uma noite específica.

1.  **Selecione a Aba**: Certifique-se de que a aba **🌙 Análise Noturna** está selecionada.
2.  **Escolha os Grupos de Alvos**:
    -   Marque **Incluir Alvos de Céu Profundo** para analisar uma lista curada de galáxias, nebulosas e aglomerados populares.
    -   Marque **Incluir Alvos do Sistema Solar** para analisar a visibilidade dos planetas, Sol e Lua.
    -   Use a caixa de texto **Adicionar alvos manualmente** para inserir nomes de objetos específicos (um por linha).
3.  **Gere a Análise**: Clique no botão **Gerar Análise da Noite**.
4.  **Interprete os Resultados**:
    -   A aplicação primeiro mostrará a **janela de observação** (o período entre o início e o fim do crepúsculo astronômico).
    -   Abaixo, serão exibidos gráficos para cada alvo. Cada gráfico mostra a altitude do objeto no céu ao longo da noite. A área sombreada em verde indica o período em que o alvo está acima da elevação mínima que você definiu, representando a janela de observação ideal para aquele objeto.

### Passo 3: Gerar um Calendário Anual

Esta análise é perfeita para planejamento de longo prazo, mostrando as melhores épocas do ano para observar um alvo específico.

1.  **Selecione a Aba**: Clique na aba **📅 Calendário Anual**.
2.  **Defina o Alvo e o Ano**:
    -   Em **Nome do Alvo**, digite o nome do objeto que deseja analisar (ex: "Orion Nebula" ou "M42").
    -   Em **Ano**, defina o ano para o qual deseja gerar o calendário.
3.  **Gere o Calendário**: Clique no botão **Gerar Calendário Anual**. Esta análise é mais intensiva e pode levar alguns minutos.
4.  **Interprete o Resultado**:
    -   Será exibido um **mapa de calor**. O eixo vertical representa os meses do ano e o eixo horizontal, os dias do mês.
    -   As cores indicam a **duração da visibilidade** em horas para cada noite. Cores mais claras (amarelo) representam noites com longos períodos de visibilidade, enquanto cores escuras (roxo/preto) indicam pouca ou nenhuma visibilidade.
    -   Use este gráfico para identificar rapidamente os meses ideais para suas sessões de astrofotografia ou observação.

---

Desenvolvido como uma ferramenta de planejamento para entusiastas da astronomia. Boas observações!
