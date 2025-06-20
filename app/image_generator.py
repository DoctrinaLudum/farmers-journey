# app/image_generator.py
from PIL import Image
import os
import io
from . import config
from . import map_generator # Importa o nosso novo "Arquiteto"

def generate_expansion_image(island_type: str, level: int):
    """
    Gera a imagem da ilha, pedindo o mapa ao map_generator e montando os tiles.
    """
    try:
        # 1. Pede ao "Arquiteto" para desenhar o mapa do nível atual
        layout_map = map_generator.generate_layout_map(island_type, level)
        if not layout_map:
            # Se não houver mapa para este nível, não há o que construir.
            return None

        # 2. Pega as dimensões de cada "azulejo" na configuração
        tile_width, tile_height = config.TILE_SIZE

        # 3. Calcula o tamanho da imagem final com base no tamanho do mapa
        map_height_in_tiles = len(layout_map)
        map_width_in_tiles = len(layout_map[0])
        final_image_width = map_width_in_tiles * tile_width
        final_image_height = map_height_in_tiles * tile_height

        # 4. Cria uma "tela" em branco para a nossa imagem final
        final_image = Image.new('RGBA', (final_image_width, final_image_height))

        # 5. Itera sobre cada célula do mapa para "colar" os azulejos
        for row_index, row_list in enumerate(layout_map):
            for col_index, tile_name in enumerate(row_list):
                
                # Constrói o caminho para o ficheiro do tile
                # Ex: app/static/images/expansions/tiles/0_0_0_1_.png
                tile_path = os.path.join('app', 'static', 'images', 'expansions', 'tiles', f"{tile_name}.png")
                
                if os.path.exists(tile_path):
                    tile_image = Image.open(tile_path).convert("RGBA")
                    
                    # Calcula onde colar o tile na tela final
                    paste_x = col_index * tile_width
                    paste_y = row_index * tile_height
                    
                    # Cola o tile na posição correta
                    final_image.paste(tile_image, (paste_x, paste_y), tile_image)

        # 6. Salva a imagem montada num buffer de memória
        byte_arr = io.BytesIO()
        final_image.save(byte_arr, format='PNG')
        byte_arr.seek(0) # Retorna o cursor para o início do buffer para que possa ser lido

        return byte_arr

    except Exception as e:
        print(f"Erro ao gerar a imagem da expansão por tiles: {e}")
        return None