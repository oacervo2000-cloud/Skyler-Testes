# 🔭 Analisador de Visibilidade Astronômica

Este repositório contém uma ferramenta avançada para planejamento de observações astronômicas. Utilizando uma arquitetura modular em Python, a ferramenta permite que astrônomos amadores e profissionais analisem a visibilidade de corpos celestes a partir de qualquer localização na Terra.

A ferramenta oferece duas interfaces principais para atender a diferentes necessidades:
1.  **Aplicação Web com Streamlit**: Uma interface gráfica interativa, ideal para uso rápido e visual.
2.  **Jupyter Notebook**: Para usuários que desejam explorar a análise de forma mais profunda, personalizar o código ou integrá-lo em seus próprios scripts.

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

## Instalação
Antes de usar qualquer uma das interfaces, clone o repositório e instale as dependências:
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git  # Substitua pela URL correta
cd seu-repositorio
pip install -r requirements.txt
```

---

## Opções de Uso

Você pode escolher a interface que melhor se adapta ao seu fluxo de trabalho.

### Opção 1: Aplicação Web (Streamlit)
Ideal para uma experiência visual e interativa sem necessidade de código.
1.  **Inicie o Servidor**: No terminal, execute o comando:
    ```bash
    streamlit run app.py
    ```
2.  **Use a Interface**: A aplicação abrirá no seu navegador. Siga as instruções no tutorial abaixo.

### Opção 2: Jupyter Notebook
Ideal para personalização, análise de dados e integração com outros scripts Python.
1.  **Inicie o Servidor Jupyter**: No terminal, execute:
    ```bash
    jupyter notebook
    ```
2.  **Abra o Notebook**: No seu navegador, abra o arquivo `analise_astronomica.ipynb`.
3.  **Siga o Guia**: O próprio notebook contém instruções detalhadas em células de Markdown.

---

## Tutorial da Aplicação Web (Streamlit)

### Passo 1: Configurar a Análise
Na barra lateral esquerda, configure os parâmetros da sua sessão:
1.  **Defina sua Localização**: Digite o nome da sua cidade (ex: `São Francisco do Sul, Brazil`) e clique em **Definir Localização**.
2.  **Ajuste a Data e Elevação**: Selecione a data desejada e a elevação mínima para a observação.

### Passo 2: Executar Análise Noturna ou Anual
-   Use a aba **🌙 Análise Noturna** para ver a visibilidade de múltiplos alvos em uma noite.
-   Use a aba **📅 Calendário Anual** para ver o melhor período do ano para observar um único alvo.

#### **Interpretando os Resultados**
-   **Gráfico de Visibilidade (Análise Noturna)**: Mostra a altitude de um alvo ao longo da noite. A área verde indica a janela de observação ideal.
-   **Calendário Anual (Mapa de Calor)**: Mostra a duração da visibilidade (em horas) para cada noite do ano. Cores claras (amarelo) significam mais horas de observação.

---

## Tutorial do Jupyter Notebook

O notebook é projetado para ser autoexplicativo. O fluxo de trabalho é simples:

### Passo 1: Abra e Leia
-   Após iniciar o Jupyter e abrir `analise_astronomica.ipynb`, leia as instruções nas células de Markdown.

### Passo 2: Configure a Análise
-   Encontre a célula de código marcada como **"⚙️ 2. Configurações da Análise"**.
-   Edite as variáveis Python diretamente nesta célula para definir sua cidade, a data da análise, os alvos desejados e a elevação mínima.
    ```python
    # Exemplo de configuração
    NOME_DA_CIDADE = "Vitória da Conquista, Brazil"
    DATA_ANALISE = date(2024, 7, 15)
    alvos_manuais = ["NGC 5128", "M83"]
    ALVO_ANUAL = "M42"
    ```

### Passo 3: Execute as Células
-   Execute as células de código em ordem.
-   A célula **"🌙 3. Execução da Análise Noturna"** gerará os gráficos de visibilidade para os alvos noturnos.
-   A célula **"📅 4. Execução da Análise Anual"** gerará o calendário de visibilidade para o alvo anual.
-   Os resultados (gráficos e saídas de texto) aparecerão diretamente no notebook.

---

Desenvolvido para entusiastas da astronomia. Boas observações!
