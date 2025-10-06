"""
Serviço para lidar com a lógica de animações, como fornecer
personagens animados dinamicamente.
"""
import os
from flask import current_app

def get_animated_characters():
    """
    Escaneia os diretórios de imagens estáticas para encontrar personagens animados
    (npcs, pets, animals) e retorna uma lista formatada em JSON.

    A estrutura de diretórios esperada é:
    - static/images/npcs/...
    - static/images/pets/...
    - static/images/animals/...

    Retorna:
        list: Uma lista de dicionários, onde cada dicionário representa um personagem
              com as chaves "type" (e.g., "npcs") e "name" (caminho relativo do arquivo).
    """
    characters = []
    base_path = os.path.join(current_app.static_folder, 'images')
    character_folders = ['npcs', 'pets', 'animals']

    for folder in character_folders:
        folder_path = os.path.join(base_path, folder)
        if os.path.isdir(folder_path):
            for root, _, files in os.walk(folder_path):
                for file in files:
                    # Garante que estamos lidando apenas com arquivos de imagem
                    if file.lower().endswith(('.png', '.webp', '.gif', '.jpg', '.jpeg')):
                        # Cria o caminho relativo a partir da pasta base do tipo (e.g., 'pets/')
                        relative_path = os.path.relpath(os.path.join(root, file), folder_path).replace('\\', '/')
                        characters.append({
                            "type": folder,
                            "name": relative_path
                        })
    
    return characters

