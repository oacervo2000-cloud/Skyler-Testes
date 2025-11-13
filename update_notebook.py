# update_notebook.py
import nbformat

def update_notebook_with_file_loading():
    """
    Lê o notebook, adiciona a funcionalidade de carregamento de arquivos
    e salva as alterações, garantindo um formato JSON válido.
    """
    try:
        # --- Ler o Notebook Existente ---
        with open('analise_astronomica.ipynb', 'r') as f:
            nb = nbformat.read(f, as_version=4)

        # --- Célula de Configuração (índice 3) ---
        config_cell = nb.cells[3]
        if 'ARQUIVO_DE_ALVOS' not in config_cell.source:
            config_cell.source += '\\n\\n# --- Carregar Alvos de um Arquivo (Opcional) ---\\n'
            config_cell.source += '# Deixe em branco ("") para não usar. Suporta .txt ou .csv\\n'
            config_cell.source += 'ARQUIVO_DE_ALVOS = "targets.csv"'

        # --- Célula de Análise Noturna (índice 5) ---
        analysis_cell = nb.cells[5]

        # Lógica de leitura de arquivo
        file_loading_logic = """
    # Carregar alvos do arquivo, se especificado
    if ARQUIVO_DE_ALVOS:
        print(f"Carregando alvos de '{ARQUIVO_DE_ALVOS}'...")
        try:
            if ARQUIVO_DE_ALVOS.endswith('.txt'):
                with open(ARQUIVO_DE_ALVOS, 'r') as f:
                    alvos_do_arquivo = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                nomes_alvos.extend(alvos_do_arquivo)
            elif ARQUIVO_DE_ALVOS.endswith('.csv'):
                with open(ARQUIVO_DE_ALVOS, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    # Assume que a coluna se chama 'alvo'
                    alvos_do_arquivo = [row['alvo'] for row in reader if 'alvo' in row and row['alvo'].strip()]
                nomes_alvos.extend(alvos_do_arquivo)
            print(f"{len(alvos_do_arquivo)} alvos carregados do arquivo.")
        except FileNotFoundError:
            print(f"AVISO: O arquivo '{ARQUIVO_DE_ALVOS}' não foi encontrado.")
        except Exception as e:
            print(f"AVISO: Erro ao ler o arquivo '{ARQUIVO_DE_ALVOS}': {e}")
"""
        # Inserir a lógica no ponto certo, se ainda não existir
        if "if ARQUIVO_DE_ALVOS:" not in analysis_cell.source:
            # A lógica é inserida após a coleta dos alvos manuais
            original_source_lines = analysis_cell.source.split('\\n')
            insertion_point = next(i for i, line in enumerate(original_source_lines) if "if alvos_manuais:" in line)

            # Divide o código em antes e depois do ponto de inserção
            part1 = '\\n'.join(original_source_lines[:insertion_point + 1])
            part2 = '\\n'.join(original_source_lines[insertion_point + 1:])

            # Remonta o código com a nova lógica
            analysis_cell.source = f"{part1}{file_loading_logic}{part2}"

        # --- Escrever as Alterações ---
        with open('analise_astronomica.ipynb', 'w') as f:
            nbformat.write(nb, f)

        print("Notebook atualizado com sucesso.")

    except Exception as e:
        print(f"Ocorreu um erro ao atualizar o notebook: {e}")

if __name__ == "__main__":
    update_notebook_with_file_loading()
