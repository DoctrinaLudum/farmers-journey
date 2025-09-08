# app/analysis.py
import logging
from collections import defaultdict
from datetime import timedelta
from decimal import Decimal, InvalidOperation

import requests

from .domain import bumpkin as bumpkin_domain
from .domain import fishing as fishing_data_domain
from .domain import flowers as flower_domain
from .domain import foods as foods_domain
from .domain import item_map
from .domain import npcs as npc_domain
from .domain import seeds as seeds_domain
from .domain import treasure_dig as treasure_domain

log = logging.getLogger(__name__)

def parse_time_to_seconds(time_str: str) -> int:
    """Converte uma string de tempo HH:MM:SS para segundos."""
    if not isinstance(time_str, str):
        return 0
    parts = list(map(int, time_str.split(':')))
    return parts[0] * 3600 + parts[1] * 60 + parts[2]

def format_seconds_to_str(seconds: int) -> str:
    """Formata um total de segundos para uma string legível (ex: 2d 5h 10m)."""
    if seconds == 0:
        return "N/A"
    td = timedelta(seconds=seconds)
    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    
    return " ".join(parts) if parts else "0m"

# ---> FUNÇÃO PARA ANÁLISE DE PESCA ---
def analyze_fishing_data(main_data: dict, secondary_data: dict):
    """
    Analisa os dados de pesca, com lógica de conquistas e caminhos de imagem corretos.
    - main_data: Contém 'milestones', inventário e atividades.
    - secondary_data: Usado para obter o 'level' do bumpkin (se necessário).
    """
    # --- 1. Inicialização e Extração de Dados ---
    if not main_data:
        log.warning("Dados principais (main_data) não fornecidos para a análise de pesca.")
        return None

    inventory = main_data.get('inventory', {})
    player_milestones = main_data.get('milestones', {})
    activity_from_root = main_data.get('farmActivity', {})
    activity_from_bumpkin = main_data.get('bumpkin', {}).get('activity', {})
    farm_activity = {**activity_from_root, **activity_from_bumpkin}

    all_fish_static = fishing_data_domain.FISHING_DATA
    all_fish_list = []
    all_seasons = ["spring", "summer", "autumn", "winter"]
    
    # Extrai todos os tipos de peixe para os filtros dinâmicos
    all_fish_types_set = set(details.get('type') for details in all_fish_static.values() if details.get('type'))
    all_fish_types_set.add("treasure")
    all_fish_types = sorted(list(all_fish_types_set))
    
    # --- 2. Processamento de Peixes e Tesouros ---
    for fish_name, details in all_fish_static.items():
        fish_type = details.get('type', 'basic')
        seasons_for_item = all_seasons if fish_type == 'chapter' else details.get('seasons', [])

        all_fish_list.append({
            "name": fish_name,
            "type": fish_type,
            "seasons": seasons_for_item,
            # Simplificado: Passa apenas a lista de nomes. O template resolverá o caminho da imagem.
            "baits": details.get('baits', []),
            "likes": details.get('likes', []),
            "player_count": farm_activity.get(f"{fish_name} Caught", 0),
            "inventory_count": int(inventory.get(fish_name, 0)),
            # A chave 'image_path' foi removida.
        })

    treasure_list = list(treasure_domain.TREASURES.keys())
    for treasure_name in treasure_list:
        player_count = farm_activity.get(f"{treasure_name} Caught", 0) + farm_activity.get(f"{treasure_name} Dug", 0)
        if player_count > 0:
            all_fish_list.append({
                "name": treasure_name,
                "type": "treasure",
                "seasons": all_seasons,
                "baits": [], 
                "likes": [], 
                "player_count": player_count,
                "inventory_count": int(inventory.get(treasure_name, 0)),
            })

    all_fish_list.sort(key=lambda x: x['name'])
    
    # --- 3. Processamento de Iscas e Insumos ---
    consumable_items = ["Rod", "Earthworm", "Grub", "Red Wiggler", "Fishing Lure"]
    bait_inventory = []
    for item_name in consumable_items:
        display_name = "Varas de Pesca" if item_name == "Rod" else item_name
        bait_inventory.append({
            "name": display_name,
            # Adicionado para que o template possa usar o nome original para encontrar a imagem.
            "original_name": item_name,
            "player_quantity": int(inventory.get(item_name, 0)),
        })

    # --- 4. Lógica de Análise das Conquistas ---
    total_fish_caught = sum(f['player_count'] for f in all_fish_list if f.get('type') != 'treasure')
    fish_by_type = defaultdict(list)
    for fish in all_fish_list:
        if fish.get('type') != 'treasure':
            fish_by_type[fish['type']].append(fish)

    encyclopedia_fish = fish_by_type.get('basic', []) + fish_by_type.get('advanced', []) + fish_by_type.get('expert', [])
    milestone_info = fishing_data_domain.FISHING_MILESTONES
    player_achievements = []
    marine_marvels_for_milestone = [f for f in fish_by_type.get('marine marvel', []) if f['type'] != 'chapter']
    
    long_tasks = { "Novice Angler": "Capture pelo menos 1 de cada peixe da categoria Basic.", "Advanced Angler": "Capture pelo menos 1 de cada peixe da categoria Advanced.", "Expert Angler": f"Capture um total de {300} peixes de qualquer tipo.", "Fish Encyclopedia": "Descubra 30 espécies de peixes das categorias Basic, Advanced e Expert.", "Master Angler": f"Capture um total de {1500} peixes de qualquer tipo.", "Marine Marvel Master": "Capture pelo menos 1 de cada Maravilha Marinha (excluindo peixes de capítulo).", "Deep Sea Diver": "Capture 5 de cada peixe das categorias Basic, Advanced e Expert.", "Marine Biologist": "Descubra todas as 38 espécies de peixes das categorias Basic, Advanced e Expert." }
    tier_map = { "Novice Angler": "basic", "Advanced Angler": "basic", "Expert Angler": "advanced", "Fish Encyclopedia": "advanced", "Master Angler": "expert", "Marine Marvel Master": "expert", "Deep Sea Diver": "expert", "Marine Biologist": "expert" }

    for ach_name, ach_details in milestone_info.items():
        is_completed = ach_name in player_milestones
        progress = {"current": 0, "total": 1, "percent": 100 if is_completed else 0}
        if not is_completed:
            if ach_name == "Novice Angler": progress = {"current": sum(1 for f in fish_by_type['basic'] if f['player_count'] > 0), "total": len(fish_by_type['basic'])}
            elif ach_name == "Advanced Angler": progress = {"current": sum(1 for f in fish_by_type['advanced'] if f['player_count'] > 0), "total": len(fish_by_type['advanced'])}
            elif ach_name == "Expert Angler": progress = {"current": total_fish_caught, "total": 300}
            elif ach_name == "Fish Encyclopedia": progress = {"current": sum(1 for f in encyclopedia_fish if f['player_count'] > 0), "total": 30}
            elif ach_name == "Master Angler": progress = {"current": total_fish_caught, "total": 1500}
            elif ach_name == "Marine Marvel Master": progress = {"current": sum(1 for f in marine_marvels_for_milestone if f['player_count'] > 0), "total": len(marine_marvels_for_milestone)}
            elif ach_name == "Deep Sea Diver": progress = {"current": sum(1 for f in encyclopedia_fish if f['player_count'] >= 5), "total": len(encyclopedia_fish)}
            elif ach_name == "Marine Biologist": progress = {"current": sum(1 for f in encyclopedia_fish if f['player_count'] > 0), "total": len(encyclopedia_fish)}
            if progress.get('total', 0) > 0: progress["percent"] = min((progress.get('current', 0) / progress['total'] * 100), 100)
            else: progress["percent"] = 100 if progress.get('current', 0) > 0 else 0
        if is_completed: progress['current'] = progress.get('total', 1)
        player_achievements.append({ "name": ach_name, "player_has": is_completed, "task": ach_details["task"], "long_task": long_tasks.get(ach_name, ach_details["task"]), "tier": tier_map.get(ach_name, "basic"), "progress_percent": progress.get('percent', 100), "progress_text": f"{int(progress.get('current', 0))}/{int(progress.get('total', 1))}" })

    # --- 5. Montagem Final dos Dados ---
    codex_total = len(all_fish_static)
    codex_completed = sum(1 for f in all_fish_list if f['player_count'] > 0 and f.get('type') != 'treasure')
    codex_by_tier_display = {
        "Basic Fish": sorted(fish_by_type.get('basic', []), key=lambda x: x['name']),
        "Advanced Fish": sorted(fish_by_type.get('advanced', []), key=lambda x: x['name']),
        "Expert Fish": sorted(fish_by_type.get('expert', []), key=lambda x: x['name']),
        "Marine Marvel": sorted(fish_by_type.get('marine marvel', []), key=lambda x: x['name']),
        "Chapter Fish": sorted(fish_by_type.get('chapter', []), key=lambda x: x['name']),
    }
    
    fish_only_list = [f for f in all_fish_list if f.get('type') != 'treasure']
    most_caught_fish_data = max(fish_only_list, key=lambda x: x['player_count'], default=None) if fish_only_list else None
    
    most_caught_fish_details = {
        "name": "N/A",
        "count": 0,
        "icon": None
    }
    if most_caught_fish_data:
        most_caught_fish_details["name"] = most_caught_fish_data.get("name", "N/A")
        most_caught_fish_details["count"] = most_caught_fish_data.get("player_count", 0)
        if most_caught_fish_details["name"] != "N/A":
            most_caught_fish_details["icon"] = get_item_image_path(most_caught_fish_details["name"])
    
    fishing_stats = {
        "total_casts": farm_activity.get("Rod Casted", 0),
        "total_fish_caught": total_fish_caught,
        "most_caught_fish": most_caught_fish_details,
        "total_rods_crafted": farm_activity.get("Rod Crafted", 0)
    }
    
    return {
        "fishing_stats": fishing_stats,
        "all_fish_sorted": all_fish_list,
        "codex_by_tier": codex_by_tier_display,
        "codex_completed": codex_completed,
        "codex_total": codex_total,
        "codex_progress_percent": (codex_completed / codex_total * 100) if codex_total > 0 else 0,
        "player_achievements": player_achievements,
        "bait_inventory": bait_inventory,
        "all_fish_types": all_fish_types,
    }
# ---> FIM FUNÇÃO PARA ANÁLISE DE PESCA ---

# --->  FUNÇÃO MONTAGEM IMG BUMPKIN ---
def build_bumpkin_image_url(equipped_items: dict) -> str:
    """
    Constrói a URL da imagem do Bumpkin com base no dicionário de itens equipados
    fornecido diretamente pela API principal.
    """
    try:
        log.info(f"Itens equipados recebidos para construir imagem: {equipped_items}")

        ids_numericos = [0] * len(bumpkin_domain.PART_ORDER)

        for part_name_api, item_name in equipped_items.items():
            item_id = bumpkin_domain.ITEM_IDS.get(item_name)
            
            try:
                slot_index = bumpkin_domain.PART_ORDER.index(part_name_api)
                if item_id is not None:
                    ids_numericos[slot_index] = item_id
            except ValueError:
                log.warning(f"A parte do corpo '{part_name_api}' não foi encontrada na PART_ORDER e será ignorada.")

        while ids_numericos and ids_numericos[-1] == 0:
            ids_numericos.pop()

        string_de_ids = "_".join(map(str, ids_numericos))
        
        url_imagem_final = f"https://animations.sunflower-land.com/bumpkin_image/0_v1_{string_de_ids}/100"

        log.info(f"URL da imagem final construída: {url_imagem_final}")
        
        return url_imagem_final

    except Exception as e:
        log.error(f"Falha ao construir URL da imagem do Bumpkin a partir dos itens equipados: {e}")
        return None
# ---> FIM FUNÇÃO MONTAGEM IMG BUMPKIN ---

# ---> FUNÇÃO PARA ANÁLISE DE FLORES ---
def process_flower_info(main_farm_data):
    """
    Analisa os dados de flores da fazenda, comparando-os com os dados
    estáticos para criar um diário de cultivos.
    """
    # 1. Obter dados do jogador
    flowers_data = main_farm_data.get("flowers", {})
    if not flowers_data:
        flowers_data = main_farm_data.get("bumpkin", {}).get("flowers", {})

    discovered_flowers_data = flowers_data.get("discovered", {})
    discovered_flower_names = set(discovered_flowers_data.keys())
    activity_from_root = main_farm_data.get("farmActivity", {})
    activity_from_bumpkin = main_farm_data.get("bumpkin", {}).get("activity", {})
    farm_activity = {**activity_from_root, **activity_from_bumpkin}
    inventory = main_farm_data.get("inventory", {})
    current_season = main_farm_data.get("season", {}).get("season", "spring")
    all_flower_types = sorted(list(set(data.get('type') for data in flower_domain.FLOWER_DATA.values() if data.get('type'))))

    processed_flowers = []
    
    # --- Novas Estatísticas ---
    most_harvested_flower = {"name": "N/A", "count": 0}
    for key, value in farm_activity.items():
        if " Harvested" in key and key.replace(" Harvested", "") in flower_domain.FLOWER_DATA:
            if value > most_harvested_flower["count"]:
                most_harvested_flower["name"] = key.replace(" Harvested", "")
                most_harvested_flower["count"] = value

    if most_harvested_flower["name"] != "N/A":
        most_harvested_flower["icon"] = get_item_image_path(most_harvested_flower["name"])
    else:
        most_harvested_flower["icon"] = None

    total_harvested = 0

    # 2. Iterar sobre a nossa base de dados de flores
    for flower_name, data in flower_domain.FLOWER_DATA.items():
        
        flower_info = data.copy()
        flower_info['type'] = data.get('type', 'Unknown').lower()
        
        # 3. Contagem de Colheitas
        harvest_key = f"{flower_name} Harvested"
        harvest_count = farm_activity.get(harvest_key, 0)
        flower_info['harvest_count'] = harvest_count
        total_harvested += harvest_count

        # 3.5. Contagem do Inventário
        inventory_count = int(Decimal(inventory.get(flower_name, '0')))
        flower_info['inventory_count'] = inventory_count

        # 3.6. Lógica de Sazonalidade ---
        seed_name = flower_info.get("seed")
        if seed_name:
            seed_data = seeds_domain.SEEDS_DATA.get(seed_name, {})
            flower_info['seasons'] = seed_data.get("seasons", [])
        else:
            flower_info['seasons'] = []

        # 4. Status de Descoberta
        is_discovered = (
            flower_name in discovered_flower_names or
            harvest_count > 0 or
            inventory_count > 0
        )
        
        if is_discovered:
            discovered_flower_names.add(flower_name)

        if is_discovered:
            flower_info['status'] = "Discovered"
        else:
            if 'cross_breed' in data:
                parent1, parent2 = data['cross_breed']
                if parent1 in discovered_flower_names and parent2 in discovered_flower_names:
                    flower_info['status'] = "Available"
                else:
                    flower_info['status'] = "Locked"
            else:
                flower_info['status'] = "Available"
        
        icon_name = flower_name.lower().replace(" ", "_")
        flower_info['icon'] = f'images/flowers/{icon_name}.webp'
        
        processed_flowers.append(flower_info)

    # 5. Agrupar flores por semente para exibição no template
    flower_seeds_data = {name: data for name, data in seeds_domain.SEEDS_DATA.items() if data.get("planting_spot") == "Flower Bed"}

    flowers_by_seed = {}
    for seed_name in flower_seeds_data:
        flowers_by_seed[seed_name] = [
            flower for flower in processed_flowers if flower.get("seed") == seed_name
        ]

    seed_order = list(flower_seeds_data.keys())
    
    all_flowers_sorted = sorted(
        processed_flowers,
        key=lambda x: (seed_order.index(x['seed']) if x.get('seed') in seed_order else len(seed_order), x['name'])
    )

    # 6. Preparar o dicionário final para o template
    return {
        "flower_info": {
            "total_discovered": len(discovered_flower_names),
            "total_flowers": len(flower_domain.FLOWER_DATA),
            "total_harvested": total_harvested,
            "flowers_by_seed": flowers_by_seed,
            "most_harvested_flower": most_harvested_flower,
            "all_flowers_sorted": all_flowers_sorted,
            "current_season": current_season,
            "all_flower_types": all_flower_types,
        }
    }
# ---> FUNÇÃO PARA ANÁLISE DE FLORES ---

# ---> FUNÇÃO PARA ANÁLISE DE PRESENTES DE NPCS ---
def process_npc_gifts(main_farm_data: dict):
    """
    Prepara os dados de presentes dos NPCs para exibição, incluindo o progresso
    de amizade do jogador com base nos dados da API.
    """
    npc_list = []
    player_npcs_data = main_farm_data.get("npcs", {})

    # Itera sobre os dados brutos dos NPCs
    for npc_id, npc_data in npc_domain.NPC_DATA.items():
        image_filename = npc_id.replace("'", "").replace(" ", "_") + '.webp'
        
        gives_key = False
        all_rewards_data = npc_data.get("rewards", {})
        
        planned_rewards = all_rewards_data.get("planned", [])
        for reward_info in planned_rewards:
            reward_items = reward_info.get("reward", {}).get("items", {})
            if any("Key" in item_name for item_name in reward_items.keys()):
                gives_key = True
                break
        
        if not gives_key and "repeats" in all_rewards_data:
            repeat_reward_items = all_rewards_data["repeats"].get("reward", {}).get("items", {})
            if any("Key" in item_name for item_name in repeat_reward_items.keys()):
                gives_key = True

        flowers_text = ", ".join(npc_data.get("flowers", {}).keys())

        player_friendship = player_npcs_data.get(npc_id, {}).get("friendship", {})
        current_points = player_friendship.get("points", 0)
        last_claimed_points = player_friendship.get("giftClaimedAtPoints", 0)

        all_planned_rewards = sorted(npc_data.get("rewards", {}).get("planned", []), key=lambda r: r['points_required'])
        next_reward_points = 0
        next_reward_info = None
        is_repeat_reward = False

        for reward in all_planned_rewards:
            if reward['points_required'] > last_claimed_points:
                next_reward_points = reward['points_required']
                next_reward_info = reward.get('reward')
                break
        
        if not next_reward_points and npc_data.get("rewards", {}).get("repeats"):
            repeats_data = npc_data["rewards"]["repeats"]
            repeat_points_needed = repeats_data.get('points_required', 0)
            if repeat_points_needed > 0:
                next_reward_points = last_claimed_points + repeat_points_needed
                next_reward_info = repeats_data.get('reward')
                is_repeat_reward = True

        gives_repeating_key = False
        if is_repeat_reward:
            repeats_data = npc_data.get("rewards", {}).get("repeats", {})
            if repeats_data:
                repeat_reward_items = repeats_data.get("reward", {}).get("items", {})
                if any("Key" in item_name for item_name in repeat_reward_items.keys()):
                    gives_repeating_key = True

        progress_percent = 0
        points_in_level = 0
        total_for_level = 0
        if next_reward_points > 0:
            total_for_level = next_reward_points - last_claimed_points
            if total_for_level > 0:
                accumulated_points = current_points - last_claimed_points
                points_in_level = max(0, min(accumulated_points, total_for_level))
                progress_percent = (points_in_level / total_for_level) * 100
            elif current_points >= next_reward_points:
                progress_percent = 100
                points_in_level = total_for_level

        total_possible_points = all_planned_rewards[-1]['points_required'] if all_planned_rewards else 0
        total_progress_percent = 0
        if total_possible_points > 0:
            total_progress_percent = min((current_points / total_possible_points) * 100, 100)

        npc_list.append({
            "name": npc_data["name"],
            "image_filename": image_filename,
            "flowers_text": flowers_text,
            "flowers": npc_data.get("flowers", {}),
            "rewards": npc_data.get("rewards", {}),
            "friendship_current": current_points,
            "friendship_last_claimed": last_claimed_points,
            "friendship_next_reward": next_reward_points,
            "friendship_progress_percent": progress_percent,
            "friendship_points_in_level": points_in_level,
            "friendship_total_for_level": total_for_level,
            "friendship_total_possible_points": total_possible_points,
            "friendship_total_progress_percent": total_progress_percent,
            "friendship_next_reward_info": next_reward_info,
            "friendship_is_repeat_reward": is_repeat_reward,
            "gives_repeating_key": gives_repeating_key,
            "gives_key": gives_key,
        })
    
    return sorted(npc_list, key=lambda x: x['name'])
# ---> FIM DA FUNÇÃO PARA ANÁLISE DE PRESENTES DE NPCS ---

# ---> FUNÇÃO PARA CRIAÇÃO DE CAMINHOS DINAMICOS DE IMAGENS ---
def get_item_image_path(item_name: str) -> str:
    """
    Determina o caminho da imagem para um item consultando o mapa mestre de itens.
    Esta abordagem é performática e robusta, pois o mapa é construído uma única vez.
    """
    if not item_name:
        return "images/resources/unknown.webp"

    # 1. Casos especiais que não se encaixam no mapeamento padrão
    if item_name == "SFL":
        return "images/resources/flower.webp"
    if item_name == "Coins":
        return "images/resources/coins.webp"
    if item_name == "Gem":
        return "images/resources/gem.webp"
    if item_name == "Yield Fertiliser":
        return "images/misc/increase_arrow.webp"
    if item_name == "Time Fertiliser":
        return "images/misc/stopwatch.webp"
    if item_name == "Bee Swarm":
        return "images/misc/bee.webp"
    
    if item_name == "Parsnip":
        return "images/crops/parsnip.webp"

    path_name = item_name.lower().replace(" ", "_")

    item_id = bumpkin_domain.ITEM_IDS.get(item_name)
    if item_id is not None:
        return f"images/wearables/{item_id}.webp"

    # 2. Mapeamento centralizado de categoria para a pasta de imagens correspondente
    CATEGORY_TO_FOLDER = {
        "Resource": "resources", "Crop": "crops", "Nodes": "nodes",
        "Fish": "fish", "Flower": "flowers", "Seed": "seeds", "Fruit": "fruits",
        "Tool": "tools", "Treasure": "treasure", "Building": "buildings",
        "Food": "food", "Cake": "food/cakes", "Animal Product": "animal",
        "Mushroom": "resources", "CompostWorm": "composters",
        "AnimalFood": "animal_food", "AnimalMedicine": "animal_food",
        "Fertiliser": "fertilisers", "GreenhouseCrop": "crops", "ExoticCrop": "crops",
        "Misc": "misc",
        "Collectibles": "collectables",
    }

    # 3. Consulta ao mapa mestre para encontrar a categoria do item
    category = item_map.MASTER_ITEM_MAP.get(item_name)

    if category:
        if category == "Food" and ("Cake" in item_name or foods_domain.CONSUMABLES_DATA.get(item_name, {}).get("building") == "Bakery"):
            folder = CATEGORY_TO_FOLDER["Cake"]
        else:
            folder = CATEGORY_TO_FOLDER.get(category, "resources")
        
        return f"images/{folder}/{path_name}.webp"

    # 4. Fallbacks para itens não encontrados no mapa
    if "Key" in item_name: return f"images/{CATEGORY_TO_FOLDER['Misc']}/{path_name}.webp"
    if "Seed" in item_name: return f"images/{CATEGORY_TO_FOLDER['Seed']}/{path_name}.webp"

    # 5. Default final para itens completamente desconhecidos
    log.warning(f"Não foi possível determinar o caminho da imagem para o item '{item_name}'. Usando fallback para 'resources'.")
    return f"images/resources/{path_name}.webp"
# ---> FIM FUNÇÃO PARA CRIAÇÃO DE CAMINHOS DINAMICOS DE IMAGENS ---