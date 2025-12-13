# Como Contribuir

Obrigado por seu interesse em contribuir com o **Analisador de Visibilidade Astronômica**! Este projeto é voltado para a comunidade educacional e suas contribuições são muito bem-vindas.

## 🚀 Começando

1. **Fork o repositório**
2. **Clone seu fork**:
   ```bash
   git clone https://github.com/seu-usuario/Skyler-Testes.git
   cd Skyler-Testes
   ```
3. **Crie um ambiente virtual**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # No Windows: venv\\Scripts\\activate
   ```
4. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

## 🔧 Desenvolvimento

### Estrutura do Projeto

- `src/`: Código-fonte modular
  - `config.py`: Configurações e importações centralizadas
  - `location.py`: Funções de geolocalização
  - `targets.py`: Gerenciamento de alvos astronômicos
  - `analysis.py`: Cálculos de visibilidade
  - `plotting.py`: Visualizações
- `tests/`: Testes unitários com pytest
- `app.py`: Aplicação web Streamlit
- `analise_astronomica.ipynb`: Interface Jupyter Notebook

### Executando os Testes

```bash
pytest tests/
```

Para executar com cobertura:
```bash
pytest --cov=src tests/
```

### Executando a Aplicação

**Streamlit:**
```bash
streamlit run app.py
```

**Jupyter Notebook:**
```bash
jupyter notebook analise_astronomica.ipynb
```

## 📝 Diretrizes de Contribuição

### Tipos de Contribuições

- 🐛 **Correções de bugs**: Reporte ou corrija bugs
- ✨ **Novas funcionalidades**: Adicione recursos úteis
- 📚 **Documentação**: Melhore README, docstrings, exemplos
- 🧪 **Testes**: Aumente a cobertura de testes
- 🌐 **Tradução**: Ajude a internacionalizar o projeto

### Processo de Contribuição

1. **Crie uma issue** descrevendo o que pretende fazer
2. **Crie um branch** para sua feature:
   ```bash
   git checkout -b feature/minha-feature
   ```
3. **Faça suas alterações** seguindo as diretrizes de código
4. **Escreva/atualize testes** para suas mudanças
5. **Execute os testes** para garantir que tudo funciona
6. **Commit suas mudanças** com mensagens descritivas:
   ```bash
   git commit -m "Adiciona funcionalidade X"
   ```
7. **Push para seu fork**:
   ```bash
   git push origin feature/minha-feature
   ```
8. **Abra um Pull Request** descrevendo suas mudanças

### Estilo de Código

- Siga a [PEP 8](https://pep8.org/) para código Python
- Use nomes de variáveis e funções descritivos em português
- Adicione docstrings para todas as funções públicas
- Mantenha linhas com no máximo 100 caracteres
- Use type hints quando apropriado

### Mensagens de Commit

Use mensagens claras e descritivas:
- ✅ "Adiciona cálculo de fase da Lua"
- ✅ "Corrige bug na plotagem de alvos circumpolares"
- ❌ "Update"
- ❌ "Fix"

## 🧪 Escrevendo Testes

Todos os novos recursos devem incluir testes. Use pytest e siga o padrão existente:

```python
def test_minha_funcao():
    """Testa se minha_funcao retorna o valor esperado."""
    resultado = minha_funcao(parametro)
    assert resultado == valor_esperado
```

## 📚 Documentação

- Adicione docstrings para novas funções:
  ```python
  def minha_funcao(parametro):
      """
      Descrição breve da função.
      
      Args:
          parametro: Descrição do parâmetro
          
      Returns:
          Descrição do retorno
      """
  ```
- Atualize o README.md se adicionar funcionalidades importantes
- Inclua exemplos de uso quando relevante

## 🤝 Código de Conduta

Este projeto segue o [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). Ao participar, você concorda em seguir suas diretrizes.

## 💡 Dúvidas?

Se tiver dúvidas sobre como contribuir, abra uma issue ou entre em contato com os mantenedores do projeto.

**Obrigado por contribuir! 🌟**
