# app/services/expansion_service.py
import logging
from collections import defaultdict
from datetime import timedelta
from decimal import Decimal, InvalidOperation

from app.analysis import get_item_image_path
from app.domain import buildings, expansions

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

def analyze_expansion_progress(secondary_data: dict, main_data: dict):
    """
    Analisa o progresso do jogador para a próxima expansão de terra.
    """
    if not secondary_data or not main_data:
        return None

    try:
        land_info = secondary_data.get("land", {})
        land_type = land_info.get("type")
        current_level_str = land_info.get("level")

        if not land_type or current_level_str is None:
            log.warning("Dados de tipo ou nível da ilha ausentes nos dados secundários.")
            return None

        try:
            current_level = int(current_level_str)
        except (ValueError, TypeError):
            log.error(f"Nível da ilha inválido: {current_level_str}")
            return None

        next_level = current_level + 1
        
        expansion_details = expansions.EXPANSION_DATA.get(land_type, {}).get(next_level)
        
        if not expansion_details:
            log.info(f"Nenhum requisito de expansão encontrado para {land_type} nível {next_level}.")
            return {"requirements_met": True}

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
    """Calcula o total de recursos, tempo e nível de Bumpkin para uma meta."""
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

    if goal_island_index < current_island_index or \
       (goal_island_index == current_island_index and goal_level <= current_level):
        return {}

    for i in range(current_island_index, goal_island_index + 1):
        island_name = island_order[i]
        island_data = {int(k): v for k, v in all_expansions.get(island_name, {}).items() if str(k).isdigit()}
        if not island_data: continue

        start_range = current_level + 1 if i == current_island_index else min(island_data.keys())
        end_range = goal_level if i == goal_island_index else max(island_data.keys())

        for level in range(start_range, end_range + 1):
            level_details = island_data.get(level)
            if not level_details: continue
            
            level_reqs = level_details.get("requirements", {})
            if not level_reqs: continue

            max_bumpkin_level = max(max_bumpkin_level, level_reqs.get("Bumpkin Level", 0))
            total_seconds += parse_time_to_seconds(level_reqs.get("Time", "00:00:00"))

            for item, amount in level_reqs.items():
                if item not in ["Bumpkin Level", "Time"]:
                    try:
                        total_needed[item] += Decimal(str(amount))
                    except InvalidOperation:
                        log.warning(f"Valor inválido para o item {item}: {amount}")

    final_requirements = {item: int(val) if val % 1 == 0 else float(val) for item, val in total_needed.items()}
    
    return {
        "requirements": dict(sorted(final_requirements.items())),
        "max_bumpkin_level": max_bumpkin_level,
        "total_time_str": format_seconds_to_str(total_seconds)
    }
# ---> FIM FUNÇÃO PARA CÁLCULO DE META TOTAL ---


def calculate_total_gains(start_land_type: str, start_level: int, goal_land_type: str, goal_level: int):
    """Calcula os ganhos de nodes e edifícios na simulação."""
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
        log.error(f"Tipo de ilha inválido: start={start_land_type}, goal={goal_land_type}")
        return {}

    for i in range(start_island_index, goal_island_index + 1):
        island_name = island_order[i]
        island_data = {int(k): v for k, v in expansion_data.get(island_name, {}).items() if str(k).isdigit()}
        if not island_data: continue
        
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

    summarized_gains = defaultdict(lambda: {"total": 0, "details": defaultdict(int)})

    for level, gains in gains_by_level.items():
        for building in gains.get("buildings", []):
            summarized_gains[building]["total"] += 1
            summarized_gains[building]["details"][level] += 1
            summarized_gains[building]["type"] = "building"

        for node, count in gains.get("nodes", {}).items():
            summarized_gains[node]["total"] += count
            summarized_gains[node]["details"][level] += count
            summarized_gains[node]["type"] = "node"

    summary_list = []
    for name, data in summarized_gains.items():
        summary_list.append({
            "name": name,
            "total": data["total"],
            "details": dict(sorted(data["details"].items())),
            "type": data["type"],
            "icon": get_item_image_path(name)
        })
    
    return {"summary": sorted(summary_list, key=lambda x: x['name'])}