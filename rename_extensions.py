import os
import sys

def rename_files_to_webp(directory_path):
    """
    Itera sobre um diretório e altera a extensão de todos os arquivos para .webp.
    """
    # Verifica se o caminho fornecido é um diretório válido
    if not os.path.isdir(directory_path):
        print(f"Aviso: O diretório '{directory_path}' não foi encontrado e será ignorado.")
        return

    print(f"Processando diretório: {directory_path}")
    count = 0
    # Lista todos os arquivos e pastas no diretório
    for filename in os.listdir(directory_path):
        # Ignora subdiretórios para evitar processamento indesejado
        if os.path.isdir(os.path.join(directory_path, filename)):
            continue

        # Separa o nome do arquivo da sua extensão atual
        base_name, old_extension = os.path.splitext(filename)

        # Pula o arquivo se a extensão já for .webp
        if old_extension.lower() == '.webp':
            continue

        # Monta o caminho completo do arquivo antigo e do novo
        old_file_path = os.path.join(directory_path, filename)
        new_file_path = os.path.join(directory_path, f"{base_name}.webp")

        try:
            # Renomeia o arquivo
            os.rename(old_file_path, new_file_path)
            print(f"  - Renomeado: '{filename}' -> '{os.path.basename(new_file_path)}'")
            count += 1
        except OSError as e:
            print(f"  - Erro ao renomear '{filename}': {e}")

    print(f"Concluído. {count} arquivos foram renomeados em '{os.path.basename(directory_path)}'.\n")

def main():
    """
    Função principal que define os diretórios e inicia o processo.
    """
    # O script assume que está na raiz do projeto 'farmers-journey'
    base_path = os.path.join('app', 'static', 'images')
    
    # Lista de diretórios a serem processados
    directories_to_process = [os.path.join(base_path, 'wearables'), os.path.join(base_path, 'animals\chickens')]

    for directory in directories_to_process:
        rename_files_to_webp(directory)

if __name__ == "__main__":
    main()
    print("Processo de renomeação finalizado.")