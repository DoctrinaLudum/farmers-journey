# app/analysis.py
import logging
from decimal import Decimal, InvalidOperation
import config
from collections import defaultdict
from datetime import timedelta
from .domain import fishing as fishing_data_domain



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
    - secondary_data: Contém os dados da ilha (tipo, nível) da API sfl.world.
    - main_data: Contém o inventário e o balanço de SFL/moedas da API principal.
    """
    if not secondary_data or not main_data:
        return None

    try:
        # Pega o tipo e o nível da ilha dos dados secundários
        land_info = secondary_data.get("land", {})
        land_type = land_info.get("type")
        current_level = land_info.get("level")

        if not land_type or current_level is None:
            log.warning("Dados de tipo ou nível da ilha ausentes nos dados secundários.")
            return None

        next_level = current_level + 1
        
        # Busca os requisitos no config
        requirements = config.LAND_EXPANSION_REQUIREMENTS.get(land_type, {}).get(next_level)

        if not requirements:
            log.info(f"Nenhum requisito de expansão encontrado para {land_type} nível {next_level}.")
            return {"requirements_met": True} # Sinaliza que pode ser o nível máximo

        # ---> Lógica de Comparação <---
        progress = {
            "land_type": land_type,
            "next_level": next_level,
            "bumpkin_level_req": requirements.get("Bumpkin Level", 0),
            "time_req": requirements.get("Time", "N/A"),
            "resources": []
        }
        
        # Pega os recursos do jogador dos dados principais
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
                "name": item,
                "have": have_amount,
                "required": required_amount,
                "percentage": percentage
            })
        
        return progress

    except Exception as e:
        log.exception(f"Erro ao analisar o progresso da expansão: {e}")
        return None
# ---> FIM FUNÇÃO PARA ANÁLISE DE EXPANSÃO ---

# ---> NOVA FUNÇÃO PARA CÁLCULO DE META TOTAL <---
def calculate_total_requirements(current_land_type, current_level, goal_land_type, goal_level, all_reqs):
    """
    Calcula o total de recursos, o tempo acumulado e o nível máximo de Bumpkin
    necessários para ir do nível atual até um nível objetivo.
    """
    total_needed = defaultdict(Decimal)
    total_seconds = 0
    max_bumpkin_level = 0
    
    island_order = ["basic", "petal", "desert", "volcano"]

    try:
        current_island_index = island_order.index(current_land_type)
        goal_island_index = island_order.index(goal_land_type)
    except ValueError:
        return {}

    is_invalid_goal = goal_island_index < current_island_index or \
                      (goal_island_index == current_island_index and goal_level <= current_level)
    
    if is_invalid_goal:
        return {}

    # Itera sobre as ilhas desde a atual até a do objetivo
    for i in range(current_island_index, goal_island_index + 1):
        island_name = island_order[i]
        island_reqs = all_reqs.get(island_name, {})
        
        start_range = current_level + 1 if i == current_island_index else min(island_reqs.keys())
        end_range = goal_level if i == goal_island_index else max(island_reqs.keys())

        # Soma os requisitos para cada nível no intervalo definido
        for level in range(start_range, end_range + 1):
            level_reqs = island_reqs.get(level)
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
    Analisa os dados de pesca, com lógica de conquistas 100% alinhada
    com o ficheiro milestones.ts do jogo.
    - main_data: Contém 'milestones', inventário e atividades.
    - secondary_data: Usado para obter o 'level' do bumpkin (se necessário).
    """
    if not main_data:
        log.warning("Dados principais (main_data) não fornecidos para a análise de pesca.")
        return None

    # O 'bumpkin_data' é usado para obter a 'activity' como alternativa.
    bumpkin_data = main_data.get('bumpkin', {}) or {}
    
    inventory = main_data.get('inventory', {})
    # Prioriza 'farmActivity' dos dados principais, mas usa 'activity' como alternativa.
    farm_activity = main_data.get('farmActivity', {}) or bumpkin_data.get('activity', {})
    
    # PONTO-CHAVE CORRIGIDO: Acessa os milestones diretamente de 'main_data',
    # que representa o objeto 'farm'. O caminho é farm > milestones.
    player_milestones = main_data.get('milestones', {})
    log.debug(f"Analisando pesca com milestones encontrados em farm > milestones: {player_milestones}")

    all_fish_static = fishing_data_domain.FISHING_DATA
    
    all_fish_list = []
    fish_by_type = defaultdict(list)
    
    # O resto da função permanece exatamente igual.
    for fish_name, details in all_fish_static.items():
        fish_type = details.get('type', 'basic')
        fish_info = {
            "name": fish_name,
            "type": fish_type,
            "seasons": details.get('seasons', []),
            "baits": details.get('baits', []),
            "likes": details.get('likes', []),
            "player_count": farm_activity.get(f"{fish_name} Caught", 0),
            "image_filename": f"{fish_name.lower().replace(' ', '_')}.png"
        }
        all_fish_list.append(fish_info)
        fish_by_type[fish_type].append(fish_info)

    all_fish_list.sort(key=lambda x: x['name'])
    total_fish_caught = sum(f['player_count'] for f in all_fish_list)
    
    encyclopedia_fish = fish_by_type.get('basic', []) + fish_by_type.get('advanced', []) + fish_by_type.get('expert', [])
    
    # --- Lógica de Análise das Conquistas ---
    milestone_info = fishing_data_domain.FISHING_MILESTONES
    player_achievements = []
    
    marine_marvels_for_milestone = [f for f in fish_by_type.get('marine marvel', []) if f['type'] != 'chapter']

    long_tasks = {
        "Novice Angler": "Capture pelo menos 1 de cada peixe da categoria Basic.",
        "Advanced Angler": "Capture pelo menos 1 de cada peixe da categoria Advanced.",
        "Expert Angler": f"Capture um total de {300} peixes de qualquer tipo.",
        "Fish Encyclopedia": "Descubra 30 espécies de peixes das categorias Basic, Advanced e Expert.",
        "Master Angler": f"Capture um total de {1500} peixes de qualquer tipo.",
        "Marine Marvel Master": "Capture pelo menos 1 de cada Maravilha Marinha (excluindo peixes de capítulo).",
        "Deep Sea Diver": "Capture 5 de cada peixe das categorias Basic, Advanced e Expert.",
        "Marine Biologist": "Descubra todas as 38 espécies de peixes das categorias Basic, Advanced e Expert."
    }
    
    tier_map = {
        "Novice Angler": "basic", "Advanced Angler": "basic",
        "Expert Angler": "advanced", "Fish Encyclopedia": "advanced",
        "Master Angler": "expert", "Marine Marvel Master": "expert",
        "Deep Sea Diver": "expert", "Marine Biologist": "expert"
    }

    for ach_name, ach_details in milestone_info.items():
        is_completed = ach_name in player_milestones
        progress = {"current": 0, "total": 1, "percent": 100 if is_completed else 0}

        if not is_completed:
            if ach_name == "Novice Angler":
                progress = {"current": sum(1 for f in fish_by_type['basic'] if f['player_count'] > 0), "total": len(fish_by_type['basic'])}
            elif ach_name == "Advanced Angler":
                progress = {"current": sum(1 for f in fish_by_type['advanced'] if f['player_count'] > 0), "total": len(fish_by_type['advanced'])}
            elif ach_name == "Expert Angler":
                progress = {"current": total_fish_caught, "total": 300}
            elif ach_name == "Fish Encyclopedia":
                progress = {"current": sum(1 for f in encyclopedia_fish if f['player_count'] > 0), "total": 30}
            elif ach_name == "Master Angler":
                progress = {"current": total_fish_caught, "total": 1500}
            elif ach_name == "Marine Marvel Master":
                progress = {"current": sum(1 for f in marine_marvels_for_milestone if f['player_count'] > 0), "total": len(marine_marvels_for_milestone)}
            elif ach_name == "Deep Sea Diver":
                progress = {"current": sum(1 for f in encyclopedia_fish if f['player_count'] >= 5), "total": len(encyclopedia_fish)}
            elif ach_name == "Marine Biologist":
                progress = {"current": sum(1 for f in encyclopedia_fish if f['player_count'] > 0), "total": len(encyclopedia_fish)}

            if progress.get('total', 0) > 0:
                progress["percent"] = min((progress.get('current', 0) / progress['total'] * 100), 100)
            else:
                progress["percent"] = 100 if progress.get('current', 0) > 0 else 0
        
        if is_completed:
            progress['current'] = progress.get('total', 1)

        player_achievements.append({
            "name": ach_name, "player_has": is_completed,
            "task": ach_details["task"], "long_task": long_tasks.get(ach_name, ach_details["task"]),
            "tier": tier_map.get(ach_name, "basic"),
            "progress_percent": progress.get('percent', 100),
            "progress_text": f"{int(progress.get('current', 0))}/{int(progress.get('total', 1))}"
        })

    # --- Análise de Itens (iscas, tesouros) ---
    treasure_list = [item for item, details in config.INVENTORY_ITEMS.items() if details.get('type') == 'Treasure']
    fished_treasures = []
    for treasure_name in treasure_list:
        player_count = farm_activity.get(f"{treasure_name} Caught", 0) + farm_activity.get(f"{treasure_name} Dug", 0)
        if player_count > 0:
            fished_treasures.append({"name": treasure_name, "player_count": player_count})
    
    fishing_items = ["Earthworm", "Grub", "Red Wiggler", "Fishing Lure"]
    bait_inventory = []
    for item_name in fishing_items:
        bait_inventory.append({"name": item_name, "player_quantity": int(inventory.get(item_name, 0))})

    # --- Montagem Final ---
    codex_total = len(all_fish_static)
    codex_completed = sum(1 for f in all_fish_list if f['player_count'] > 0)
    codex_by_tier_display = {
        "Basic Fish": sorted(fish_by_type.get('basic', []), key=lambda x: x['name']),
        "Advanced Fish": sorted(fish_by_type.get('advanced', []), key=lambda x: x['name']),
        "Expert Fish": sorted(fish_by_type.get('expert', []), key=lambda x: x['name']),
        "Marine Marvel": sorted(fish_by_type.get('marine marvel', []), key=lambda x: x['name']),
        "Chapter Fish": sorted(fish_by_type.get('chapter', []), key=lambda x: x['name']),
    }
    
    return {
        "total_casts": farm_activity.get("Rod Casted", 0),
        "total_fish_caught": total_fish_caught,
        "all_fish_sorted": all_fish_list,
        "codex_by_tier": codex_by_tier_display,
        "codex_completed": codex_completed,
        "codex_total": codex_total,
        "codex_progress_percent": (codex_completed / codex_total * 100) if codex_total > 0 else 0,
        "player_achievements": player_achievements,
        "bait_inventory": bait_inventory, 
        "fished_treasures": fished_treasures
    }
# ---> FIM FUNÇÃO PARA ANÁLISE DE PESCA ---