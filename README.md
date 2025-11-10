# 🔭 Analisador de Visibilidade Astronômica

Este repositório contém uma ferramenta avançada para planejamento de observações astronômicas. Utilizando uma arquitetura modular em Python, a ferramenta permite que astrônomos amadores e profissionais analisem a visibilidade de corpos celestes a partir de qualquer localização na Terra.

A ferramenta oferece duas interfaces principais:
1.  **Aplicação Web com Streamlit (Recomendado)**: Uma interface gráfica interativa, ideal para uso rápido e visual.
2.  **Jupyter Notebook**: Para usuários que desejam explorar a análise de forma mais profunda ou personalizar o código.

---

## Funcionalidades Principais
-   **Análise Noturna Detalhada**: Gere gráficos de altitude vs. tempo para múltiplos alvos em uma noite específica.
-   **Calendário de Visibilidade Anual**: Crie um mapa de calor para identificar as melhores noites para observar um alvo ao longo de um ano.
-   **Localização Flexível**: Defina sua localização pelo nome da cidade (ex: "Porto, Portugal") ou coordenadas.
-   **Seleção de Alvos Abrangente**: Use listas pré-selecionadas, adicione alvos do sistema solar ou insira manualmente qualquer objeto (ex: "NGC 1300").
-   **Considerações Atmosféricas**: Configure a elevação mínima do alvo acima do horizonte para otimizar a qualidade da observação.

---

## Estrutura do Projeto
-   `app.py`: Ponto de entrada para a aplicação web Streamlit.
-   `analise_astronomica.ipynb`: Jupyter Notebook para análises interativas.
-   `requirements.txt`: Lista de todas as dependências.
-   `src/`: Código backend modularizado (config, location, targets, analysis, plotting).
-   `tests/`: Suíte de testes (pytest) para garantir a robustez do código.

---

## Como Usar

### 1. Pré-requisitos
-   Python 3.8 ou superior.
-   `pip` (gerenciador de pacotes do Python).

### 2. Instalação
Clone o repositório e instale as dependências:
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git  # Substitua pela URL correta
cd seu-repositorio
pip install -r requirements.txt
```

### 3. Executando a Aplicação Web
A maneira mais fácil de usar a ferramenta é através da aplicação Streamlit. No terminal, execute:
```bash
streamlit run app.py
```
Isso iniciará um servidor local e abrirá a aplicação no seu navegador.

---

## Tutorial Passo a Passo da Aplicação Web

### Passo 1: Configurar a Análise
Na barra lateral esquerda, configure os parâmetros da sua sessão de observação:
1.  **Defina sua Localização**: Em **📍 Localização do Observador**, digite o nome da sua cidade (ex: `São Francisco do Sul, Brazil`) e clique em **Definir Localização**.
2.  **Ajuste a Data**: Em **Data da Análise Noturna**, selecione a data desejada.
3.  **Defina a Elevação Mínima**: Use o slider **Elevação Mínima (°) **. Um alvo só é considerado "visível" quando está acima desta altitude.

### Passo 2: Executar uma Análise Noturna
1.  **Selecione a Aba**: Clique na aba **🌙 Análise Noturna**.
2.  **Escolha os Alvos**: Selecione os grupos de alvos ou adicione os seus na caixa de texto. Por exemplo:
    ```
    M87
    Centaurus A
    ```
3.  **Gere a Análise**: Clique em **Gerar Análise da Noite**.

#### **Exemplo de Output: Gráfico de Visibilidade**
Para cada alvo, um gráfico será gerado. Ele mostra a altitude do objeto no céu ao longo da noite.

-   **Eixo Y (Altitude)**: Mostra a altura do alvo em graus, de 0° (horizonte) a 90° (zênite).
-   **Eixo X (Hora)**: Mostra o tempo, desde o início da noite até o amanhecer.
-   **Linha Azul**: Trajetória do alvo no céu.
-   **Linha Tracejada Horizontal**: Sua elevação mínima definida.
-   **Área Verde**: **A Janela de Observação Ideal.** Este é o período em que o alvo está acima da sua elevação mínima, sendo o melhor momento para observá-lo.

```
      Altitude (°)
      90 |
         |      /----\
      60 |     /      \
         |    /        \
      30 |---/----------\--- [Elevação Mínima]
         |  /            \
       0 +------------------
         18:00  21:00  00:00
              Hora
```

### Passo 3: Gerar um Calendário Anual
1.  **Selecione a Aba**: Clique na aba **📅 Calendário Anual**.
2.  **Defina o Alvo e o Ano**: Digite o nome do alvo (ex: `Andromeda Galaxy` ou `M31`) e o ano desejado.
3.  **Gere o Calendário**: Clique em **Gerar Calendário Anual**.

#### **Exemplo de Output: Calendário Anual (Mapa de Calor)**
Um mapa de calor visualiza os melhores meses para observar um alvo.

-   **Eixo Y (Mês)**: De Janeiro a Dezembro.
-   **Eixo X (Dia do Mês)**: De 1 a 31.
-   **Cor da Célula**: Indica a duração (em horas) em que o alvo está acima da elevação mínima naquela noite.
    -   **Amarelo (Claro)**: Muitas horas de visibilidade. Noites excelentes.
    -   **Verde/Azul (Intermediário)**: Algumas horas de visibilidade. Noites boas.
    -   **Roxo/Preto (Escuro)**: Pouca ou nenhuma visibilidade. Noites ruins ou impossíveis.

Este gráfico permite identificar rapidamente, por exemplo, que "a Galáxia de Andrômeda é melhor observada entre Setembro e Dezembro".

---

Desenvolvido para entusiastas da astronomia. Boas observações!
