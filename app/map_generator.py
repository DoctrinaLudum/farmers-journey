# app/map_generator.py
from . import config

# O padrão de expansão anti-horário.
EXPANSION_PATTERN = ["bottom-left", "top-left", "top-right", "bottom-right"]

def get_grid_size_for_level(island_type: str, level: int):
    """
    Calcula o tamanho da grelha (largura, altura) para um nível.
    """
    start_config = config.ISLAND_START_CONFIG.get(island_type)
    if not start_config or level < start_config["start_level"]:
        return None

    width, height = start_config["start_size"]
    start_level = start_config["start_level"]

    for current_level in range(start_level, level):
        expansion_step = current_level - start_level
        if expansion_step % 2 == 0:
            width += 1
        else:
            height += 1
            
    return width, height

def generate_layout_map(island_type: str, level: int):
    """
    Gera programaticamente o mapa de tiles (grelha 2D) para um dado nível de ilha.
    """
    size_info = get_grid_size_for_level(island_type, level)
    if not size_info:
        return None
    
    width, height = size_info

    # 1. Cria uma grelha vazia (preenchida com o tile de fundo '0_0_0_0_')
    grid = [['0_0_0_0_' for _ in range(width)] for _ in range(height)]

    # 2. Preenche o "miolo" da ilha com o tile de terra '1_1_1_1_'
    for r in range(1, height - 1):
        for c in range(1, width - 1):
            grid[r][c] = '1_1_1_1_'
    
    # --- INÍCIO DA CORREÇÃO ---
    # 3. Preenche as bordas retas de forma mais inteligente
    for c in range(1, width - 1):
        grid[0][c] = '0_1_1_1_'        # Borda de cima
        grid[height - 1][c] = '1_1_0_1_' # Borda de baixo
    for r in range(1, height - 1):
        grid[r][0] = '1_0_1_1_'        # Borda da esquerda
        grid[r][width - 1] = '1_1_1_0_' # Borda da direita

    # 4. Preenche os 4 cantos corretamente
    grid[0][0] = '0_0_1_1_'                # Canto superior esquerdo
    grid[0][width - 1] = '0_1_1_0_'        # Canto superior direito
    grid[height - 1][0] = '1_0_1_0_'       # Canto inferior esquerdo
    grid[height - 1][width - 1] = '1_1_0_0_' # Canto inferior direito
    # --- FIM DA CORREÇÃO ---

    # 5. Posiciona o tile de expansão para o próximo nível
    start_level = config.ISLAND_START_CONFIG[island_type]["start_level"]
    if level >= start_level:
        expansion_step = level - start_level
        pattern_index = expansion_step % len(EXPANSION_PATTERN)
        position_key = EXPANSION_PATTERN[pattern_index]

        pos_coords = {
            "top-left": (0, 0), "top-right": (0, width - 1),
            "bottom-left": (height - 1, 0), "bottom-right": (height - 1, width - 1)
        }
        
        if position_key in pos_coords:
            r, c = pos_coords[position_key]
            grid[r][c] = config.EXPANSION_TILE_NAME

    return grid