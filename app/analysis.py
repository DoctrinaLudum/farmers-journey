# app/analysis.py
import logging
from decimal import Decimal, InvalidOperation
import config
from collections import defaultdict
from datetime import timedelta



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
def analyze_expansion_progress(farm_data: dict):
    """
    Analisa o progresso do jogador para a próxima expansão de terra.
    """
    if not farm_data:
        return None

    try:
        # Pega o tipo e o nível da ilha
        land_info = farm_data.get("expansion_data", {}).get("land", {})
        land_type = land_info.get("type")
        current_level = land_info.get("level")

        if not land_type or current_level is None:
            log.warning("Dados de tipo ou nível da ilha ausentes.")
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

        inventory = farm_data.get("inventory", {})
        sfl_balance = Decimal(farm_data.get("balance", "0"))
        coins_balance = Decimal(farm_data.get("coins", "0"))

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
                percentage = min((have_amount / Decimal(required_amount)) * 100, 100)

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