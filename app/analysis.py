# app/analysis.py
import logging
from collections import defaultdict
from datetime import timedelta
from decimal import Decimal, InvalidOperation

import requests

import config

from .domain import buildings
from .domain import bumpkin as bumpkin_domain
from .domain import expansions
from .domain import fishing as fishing_data_domain
from .domain import flowers as flower_domain

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

# ---> FUNÇÃO PARA ANÁLISE DE EXPANSÃO ---
def analyze_expansion_progress(secondary_data: dict, main_data: dict):
    """
    Analisa o progresso do jogador para a próxima expansão de terra.
    """
    if not secondary_data or not main_data:
        return None

    try:
        land_info = secondary_data.get("land", {})
        land_type = land_info.get("type")
        current_level = land_info.get("level")

        if not land_type or current_level is None:
            log.warning("Dados de tipo ou nível da ilha ausentes nos dados secundários.")
            return None

        next_level = current_level + 1
        
        # ALTERADO: Busca os detalhes da nova estrutura unificada
        expansion_details = expansions.EXPANSION_DATA.get(land_type, {}).get(next_level)
        
        if not expansion_details:
            log.info(f"Nenhum requisito de expansão encontrado para {land_type} nível {next_level}.")
            return {"requirements_met": True}

        # Acessa a sub-chave 'requirements'
        requirements = expansion_details.get("requirements", {})
        if not requirements:
             return {"requirements_met": True}

        progress = {
            "land_type": land_type,
            "next_level": next_level,
            "bumpkin_level_req": requirements.get("Bumpkin Level", 0),
            "time_req": requirements.get("Time", "N/A"),
            "resources": []
        }

        inventory = main_data.get("inventory", {})
        sfl_balance = Decimal(main_data.get("balance", "0"))
        coins_balance = Decimal(main_data.get("coins", "0"))

        for item, required_amount in requirements.items():
            if item in ["Bumpkin Level", "Time"]:
                continue

            have_amount = 0
            if item == "SFL":
                have_amount = sfl_balance
            elif item == "Coins":
                have_amount = coins_balance
            else:
                have_amount = Decimal(inventory.get(item, "0"))

            percentage = 0
            if required_amount > 0:
                percentage = min((have_amount / Decimal(str(required_amount))) * 100, 100)

            progress["resources"].append({
                "name": item, "have": have_amount,
                "required": required_amount, "percentage": percentage
            })
        
        return progress

    except Exception as e:
        log.exception(f"Erro ao analisar o progresso da expansão: {e}")
        return None

# ---> FUNÇÃO PARA CÁLCULO DE META TOTAL ---
def calculate_total_requirements(current_land_type, current_level, goal_land_type, goal_level):
    """calculate_total_requirements
    Calcula o total de recursos, o tempo acumulado e o nível máximo de Bumpkin
    necessários para ir do nível atual até um nível objetivo, usando a fonte de dados unificada.
    """
    total_needed = defaultdict(Decimal)
    total_seconds = 0
    max_bumpkin_level = 0
    
    island_order = expansions.ISLAND_ORDER
    all_expansions = expansions.EXPANSION_DATA 

    try:
        current_level = int(current_level)
        goal_level = int(goal_level)

        current_island_index = island_order.index(current_land_type)
        goal_island_index = island_order.index(goal_land_type)
    except (ValueError, TypeError):
        return {}

    is_invalid_goal = goal_island_index < current_island_index or \
                      (goal_island_index == current_island_index and goal_level <= current_level)
    
    if is_invalid_goal:
        return {}

    for i in range(current_island_index, goal_island_index + 1):
        island_name = island_order[i]
        
         # 2. Converte a chave para string ANTES de chamar .isdigit()
        island_data = {int(k): v for k, v in all_expansions.get(island_name, {}).items() if str(k).isdigit()}
        if not island_data:
            continue

        start_range = current_level + 1 if i == current_island_index else min(island_data.keys())
        end_range = goal_level if i == goal_island_index else max(island_data.keys())

        for level in range(start_range, end_range + 1):
            level_details = island_data.get(level)
            if not level_details:
                continue
            
            level_reqs = level_details.get("requirements", {})
            if not level_reqs:
                continue

            max_bumpkin_level = max(max_bumpkin_level, level_reqs.get("Bumpkin Level", 0))
            total_seconds += parse_time_to_seconds(level_reqs.get("Time", "00:00:00"))

            for item, amount in level_reqs.items():
                if item not in ["Bumpkin Level", "Time"]:
                    try:
                        total_needed[item] += Decimal(str(amount))
                    except InvalidOperation:
                        log.warning(f"Valor inválido para o item {item}: {amount}")

    final_requirements = {
        item: int(val) if val % 1 == 0 else float(val)
        for item, val in total_needed.items()
    }
    
    result = {
        "requirements": dict(sorted(final_requirements.items())),
        "max_bumpkin_level": max_bumpkin_level,
        "total_time_str": format_seconds_to_str(total_seconds)
    }

    return result
# ---> FIM DA FUNÇÃO DE CÁLCULO DE META TOTAL <---

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

        # Lógica para processar Iscas e Gostos com ícones
        baits_with_icons = []
        for bait_name in details.get('baits', []):
            item_details = config.INVENTORY_ITEMS.get(bait_name, {})
            item_type = item_details.get("type", "Resource").lower()
            folder = "composters" if item_type == "compostworm" or bait_name == "Fishing Lure" else "resources"
            baits_with_icons.append({
                "name": bait_name,
                "image_path": f"{folder}/{bait_name.lower().replace(' ', '_')}.png"
            })

        likes_with_icons = []
        for like_name in details.get('likes', []):
            item_details = config.INVENTORY_ITEMS.get(like_name, {})
            item_type_raw = item_details.get("type", "")
            
            folder = "resources"
            if item_type_raw == "Crop": folder = "crops"
            elif item_type_raw == "Fruit": folder = "fruits"
            elif item_type_raw == "Animal Product": folder = "animal"
            elif item_type_raw == "Treasure": folder = "treasure"
            elif item_type_raw in ["basic", "advanced", "expert", "marine marvel", "chapter"] or fishing_data_domain.FISHING_DATA.get(like_name):
                folder = "fish"
            if "Chicken" in like_name:
                folder = "animals/chickens"
            
            likes_with_icons.append({
                "name": like_name,
                "image_path": f"{folder}/{like_name.lower().replace(' ', '_')}.png"
            })

        all_fish_list.append({
            "name": fish_name,
            "type": fish_type,
            "seasons": seasons_for_item,
            "baits": baits_with_icons,      
            "likes": likes_with_icons,    
            "player_count": farm_activity.get(f"{fish_name} Caught", 0),
            "inventory_count": int(inventory.get(fish_name, 0)),
            "image_path": f"fish/{fish_name.lower().replace(' ', '_')}.png"
        })

    treasure_list = [item for item, details in config.INVENTORY_ITEMS.items() if details.get('type') == 'Treasure']
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
                "image_path": f"treasure/{treasure_name.lower().replace(' ', '_')}.png"
            })

    all_fish_list.sort(key=lambda x: x['name'])
    
    # --- 3. Processamento de Iscas e Insumos ---
    consumable_items = ["Rod", "Earthworm", "Grub", "Red Wiggler", "Fishing Lure"]
    bait_inventory = []
    for item_name in consumable_items:
        item_details = config.INVENTORY_ITEMS.get(item_name, {})
        item_type = item_details.get("type", "Resource").lower()
        folder = "resources"
        if item_type == "tool":
            folder = "tools"
        elif item_type == "compostworm":
            folder = "composters"
        if item_name == "Fishing Lure":
            folder = "composters"
        display_name = "Varas de Pesca" if item_name == "Rod" else item_name
        bait_inventory.append({
            "name": display_name,
            "player_quantity": int(inventory.get(item_name, 0)),
            "image_path": f"{folder}/{item_name.lower().replace(' ', '_')}.png"
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
    most_caught_fish = max(fish_only_list, key=lambda x: x['player_count'], default=None) if fish_only_list else None
    
    fishing_stats = {
        "total_casts": farm_activity.get("Rod Casted", 0),
        "total_fish_caught": total_fish_caught,
        "most_caught_name": most_caught_fish.get("name", "N/A") if most_caught_fish else "N/A",
        "most_caught_count": most_caught_fish.get("player_count", 0) if most_caught_fish else 0,
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

# --->  FUNÇÃO GANHO DA EXPANSÂO ---
def calculate_total_gains(start_land_type: str, start_level: int, goal_land_type: str, goal_level: int):
    """
    Calcula os ganhos de nodes e edifícios dentro do intervalo da simulação
    e retorna um resumo agregado.
    """
    gains_by_level = defaultdict(lambda: {"nodes": defaultdict(int), "buildings": []})
    
    island_order = expansions.ISLAND_ORDER
    expansion_data = expansions.EXPANSION_DATA
    building_reqs = buildings.BUILDING_REQUIREMENTS

    try:
        start_level = int(start_level)
        goal_level = int(goal_level)
        
        start_island_index = island_order.index(start_land_type)
        goal_island_index = island_order.index(goal_land_type)
    except (ValueError, TypeError):
        log.error(f"Tipo de ilha inválido fornecido: start={start_land_type}, goal={goal_land_type}")
        return {}

    for i in range(start_island_index, goal_island_index + 1):
        island_name = island_order[i]
        
        island_data = {int(k): v for k, v in expansion_data.get(island_name, {}).items() if str(k).isdigit()}
        if not island_data:
            continue
        
        levels_on_this_island = sorted(island_data.keys())
        
        for level in levels_on_this_island:
            if (i == start_island_index and level <= start_level) or \
               (i == goal_island_index and level > goal_level):
                continue
            
            level_details = island_data.get(level)
            if not level_details: continue

            nodes_at_this_level = level_details.get("nodes", {})
            previous_level = level - 1
            nodes_at_previous_level = {}

            if previous_level in island_data:
                nodes_at_previous_level = island_data.get(previous_level, {}).get("nodes", {})
            elif i == start_island_index and previous_level == start_level:
                 start_island_data_int = {int(k): v for k, v in expansion_data.get(start_land_type, {}).items() if str(k).isdigit()}
                 nodes_at_previous_level = start_island_data_int.get(start_level, {}).get("nodes",{})
            elif i > start_island_index:
                prev_island_name = island_order[i - 1]
                prev_island_data = {int(k): v for k, v in expansion_data.get(prev_island_name, {}).items() if str(k).isdigit()}
                if prev_island_data:
                    last_level_of_prev_island = max(prev_island_data.keys())
                    nodes_at_previous_level = prev_island_data.get(last_level_of_prev_island, {}).get("nodes", {})

            for node, current_count in nodes_at_this_level.items():
                previous_count = nodes_at_previous_level.get(node, 0)
                gain = current_count - previous_count
                if gain > 0:
                    gains_by_level[level]["nodes"][node] += gain
            
            for building, reqs in building_reqs.items():
                if reqs.get("unlocksAtLevel") == level and reqs.get("unlocksOnIsland") == island_name and reqs.get("enabled", False):
                    gains_by_level[level]["buildings"].append(building)

    # --- Parte 2: Lógica de resumo ---
    summarized_gains = defaultdict(lambda: {"total": 0, "details": defaultdict(int)})

    for level, gains in gains_by_level.items():
        for building in gains.get("buildings", []):
            summarized_gains[building]["total"] += 1
            summarized_gains[building]["details"][level] += 1
            summarized_gains[building]["type"] = "building"

        for node, count in gains.get("nodes", {}).items():
            # CORREÇÃO 2: Especifica que estamos a somar ao valor "total"
            summarized_gains[node]["total"] += count
            summarized_gains[node]["details"][level] += count
            summarized_gains[node]["type"] = "node"

    summary_list = []
    for name, data in summarized_gains.items():
        summary_list.append({
            "name": name,
            "total": data["total"],
            "details": dict(sorted(data["details"].items())),
            "type": data["type"]
        })
    
    return {"summary": sorted(summary_list, key=lambda x: x['name'])}
# ---> FIM FUNÇÃO GANHO DA EXPANSÂO ---

# --->  FUNÇÃO MONTAGEM IMG BUMPKIN ---
def build_bumpkin_image_url(equipped_items: dict) -> str:
    """
    Constrói a URL da imagem do Bumpkin com base no dicionário de itens equipados
    fornecido diretamente pela API principal.
    """
    try:
        log.info(f"Itens equipados recebidos para construir imagem: {equipped_items}")

        # Inicializa a lista de IDs com todos os slots possíveis
        ids_numericos = [0] * len(bumpkin_domain.PART_ORDER)

        for part_name_api, item_name in equipped_items.items():
            item_id = bumpkin_domain.ITEM_IDS.get(item_name)
            
            try:
                slot_index = bumpkin_domain.PART_ORDER.index(part_name_api)
                if item_id is not None:
                    ids_numericos[slot_index] = item_id
            except ValueError:
                log.warning(f"A parte do corpo '{part_name_api}' não foi encontrada na PART_ORDER e será ignorada.")

        # Remove os zeros do final da lista
        while ids_numericos and ids_numericos[-1] == 0:
            ids_numericos.pop()

        string_de_ids = "_".join(map(str, ids_numericos))
        
        # Monta a URL final com a base correta
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
    # CORREÇÃO: Os dados de flores podem estar na raiz do save ou dentro do objeto 'bumpkin'.
    # Esta lógica verifica ambos os locais para garantir que os dados sejam encontrados.
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
    total_harvested = 0

    # 2. Iterar sobre a nossa base de dados de flores
    for flower_name, data in flower_domain.FLOWER_DATA.items():
        
        # Faz uma cópia para não alterar o dicionário original
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
            seed_data = flower_domain.FLOWER_SEEDS_DATA.get(seed_name, {})
            flower_info['seasons'] = seed_data.get("seasons", [])
        else:
            flower_info['seasons'] = []

        # 4. Status de Descoberta
        # CORREÇÃO: Considera uma flor descoberta se ela foi colhida ou está no inventário,
        # além de verificar a lista de descobertas da API. Isso torna a lógica mais robusta
        # contra inconsistências nos dados do save.
        is_discovered = (
            flower_name in discovered_flower_names or
            harvest_count > 0 or
            inventory_count > 0
        )
        
        # Adiciona o nome à lista de descobertas se a nova lógica for verdadeira,
        # garantindo que o contador total de descobertas e a lógica de cross-breed funcionem.
        if is_discovered:
            discovered_flower_names.add(flower_name)

        if is_discovered:
            flower_info['status'] = "Discovered"
        else:
            # Verifica se o jogador pode descobrir esta flor
            if 'cross_breed' in data:
                parent1, parent2 = data['cross_breed']
                if parent1 in discovered_flower_names and parent2 in discovered_flower_names:
                    flower_info['status'] = "Available" # Pode ser descoberta
                else:
                    flower_info['status'] = "Locked" # Ainda não pode ser descoberta
            else:
                # Flores básicas que vêm de sementes são sempre "Available" para tentar
                flower_info['status'] = "Available"
        
        # Adiciona o caminho do ícone para o template
        icon_name = flower_name.lower().replace(" ", "_")
        flower_info['icon'] = f'images/flowers/{icon_name}.webp'
        
        processed_flowers.append(flower_info)

    # 5. Agrupar flores por semente para exibição no template
    flowers_by_seed = {}
    for seed_name in flower_domain.FLOWER_SEEDS_DATA:
        flowers_by_seed[seed_name] = [
            flower for flower in processed_flowers if flower.get("seed") == seed_name
        ]

    # 6. Preparar o dicionário final para o template
    return {
        "flower_info": {
            "total_discovered": len(discovered_flower_names),
            "total_flowers": len(flower_domain.FLOWER_DATA),
            "total_harvested": total_harvested,
            "flowers_by_seed": flowers_by_seed,
            "all_flowers_sorted": sorted(processed_flowers, key=lambda x: x['name']),
            "current_season": current_season,
            "all_flower_types": all_flower_types,
        }
    }
# ---> FUNÇÃO PARA ANÁLISE DE FLORES ---
