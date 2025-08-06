# app/services/farm_layout_service.py

import logging

log = logging.getLogger(__name__)

# Define ícones para cada tipo de nó para uma representação visual clara.
NODE_ICONS = {
    "Tree": "🌳", "Crop": "🌾", "Stone": "🪨", "Iron": "⚙️",
    "Gold": "🪙", "Crimstone": "💎", "Sunstone": "☀️",
    "Fruit Patch": "🍎", "Flower Bed": "🌸", "Beehive": "🐝",
    "Oil Reserve": "🛢️", "Building": "🏠", "Collectible": "🏆",
    "Manor": "🏰", "Water Well": "💧", "Hen House": "🐔",
    "Compost Bin": "🗑️", "Market": "🏪", "Fire Pit": "🔥",
    "Workbench": "🛠️", "Bakery": "🥖", "Kitchen": "🍳",
    "Deli": "🥪", "Smoothie Shack": "🥤", "Toolshed": "🧰",
    "Greenhouse": "🌿", "Barn": "🐄",
    "DEFAULT": "❓"
}

def generate_layout_map(farm_data: dict):
    """
    Analisa os dados da fazenda e gera uma representação em grade do layout.

    Args:
        farm_data: O dicionário de dados da API principal da fazenda.

    Returns:
        Um dicionário contendo a grade, dimensões e legenda, ou None se não houver dados.
    """
    grid = {}
    all_coords = []

    # Lista de chaves na API que contêm nós posicionáveis.
    node_sources = [
        "trees", "crops", "stones", "iron", "gold", "crimstones", "sunstones",
        "fruitPatches", "flowerBeds", "beehives", "oilReserves", "buildings",
        "collectibles"
    ]
    
    # Inclui os colecionáveis da casa, se existirem.
    home_collectibles = farm_data.get("home", {}).get("collectibles", {})
    if home_collectibles:
        farm_data["home_collectibles"] = home_collectibles
        node_sources.append("home_collectibles")

    for source_key in node_sources:
        items = farm_data.get(source_key, {})
        for item_name, item_data in items.items():
            # A estrutura de dados pode ser uma lista (ex: collectibles) ou um dicionário (ex: trees).
            item_list = item_data if isinstance(item_data, list) else [item_data]

            for single_item_data in item_list:
                # Extrai as coordenadas de forma segura.
                coords = single_item_data.get("coordinates")
                if not coords:
                    coords = {"x": single_item_data.get("x"), "y": single_item_data.get("y")}

                if coords and coords.get("x") is not None and coords.get("y") is not None:
                    x, y = coords["x"], coords["y"]
                    width = single_item_data.get("width", 1)
                    height = single_item_data.get("height", 1)

                    # Determina o tipo do nó para o ícone e a legenda.
                    if source_key in ["buildings", "collectibles", "home_collectibles"]:
                        node_type = item_name
                    else:
                        node_type = source_key.rstrip('s').capitalize()
                    
                    # Prepara detalhes para o tooltip.
                    details = {"id": item_name}
                    if source_key == "fruitPatches" and single_item_data.get("fruit"):
                        details["fruit"] = single_item_data["fruit"]["name"]
                    
                    # Preenche a grade, considerando a largura e altura do nó.
                    for i in range(width):
                        for j in range(height):
                            grid_x, grid_y = x + i, y + j
                            if grid.get((grid_x, grid_y)):
                                log.warning(f"Sobreposição de nós detectada em ({grid_x}, {grid_y})")
                                continue

                            is_primary_cell = (i == 0 and j == 0)
                            grid[(grid_x, grid_y)] = {
                                "type": node_type,
                                "icon": NODE_ICONS.get(node_type, NODE_ICONS["DEFAULT"]),
                                "details": str(details),
                                "is_primary": is_primary_cell,
                                "width": width,
                                "height": height
                            }
                            all_coords.append((grid_x, grid_y))

    if not all_coords:
        return None

    # Calcula as dimensões do mapa.
    min_x = min(c[0] for c in all_coords)
    max_x = max(c[0] for c in all_coords)
    min_y = min(c[1] for c in all_coords)
    max_y = max(c[1] for c in all_coords)

    return {
        "grid": grid,
        "min_x": min_x, "max_x": max_x,
        "min_y": min_y, "max_y": max_y,
        "legend": NODE_ICONS
    }