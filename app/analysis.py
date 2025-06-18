# app/analysis.py
import logging
from decimal import Decimal, ROUND_HALF_UP
import config
from collections import defaultdict


log = logging.getLogger(__name__)

def compare_snapshots(new_snapshot_data: dict, old_snapshot_data: dict):
    """
    Compara dois snapshots da fazenda e retorna um resumo das diferenças.
    """
    if not new_snapshot_data or not old_snapshot_data:
        return None, "Dados de snapshot inválidos para comparação."

    summary = {
        'sfl_change': 0.0,
        'items_added': {},
        'items_removed': {}
    }

    # 1. Comparar SFL (balance)
    try:
        new_balance = Decimal(new_snapshot_data.get('balance', '0'))
        old_balance = Decimal(old_snapshot_data.get('balance', '0'))
        sfl_diff = new_balance - old_balance
        # Arredonda para 4 casas decimais para exibição
        summary['sfl_change'] = float(sfl_diff.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP))
    except Exception as e:
        log.error(f"Erro ao calcular diferença de SFL: {e}")

    # 2. Comparar Inventário
    new_inventory = new_snapshot_data.get('inventory', {})
    old_inventory = old_snapshot_data.get('inventory', {})
    
    # Combina todas as chaves de ambos os inventários para não perder nenhum item
    all_item_keys = set(new_inventory.keys()) | set(old_inventory.keys())

    for item in all_item_keys:
        try:
            new_amount = Decimal(new_inventory.get(item, '0'))
            old_amount = Decimal(old_inventory.get(item, '0'))
            diff = new_amount - old_amount

            if diff > 0:
                summary['items_added'][item] = float(diff)
            elif diff < 0:
                summary['items_removed'][item] = float(abs(diff))
        except Exception as e:
            log.warning(f"Não foi possível calcular a diferença para o item '{item}': {e}")
            continue

    log.info("Comparação de snapshots concluída.")
    return summary, None

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
    Calcula o total de recursos necessários para ir do nível atual até um nível objetivo.
    """
    total_needed = defaultdict(lambda: {'needed': 0})
    
    # Validação simples
    if not current_land_type or not goal_land_type or goal_level <= current_level:
        return {}

    # Por enquanto, vamos assumir que a progressão é na mesma ilha
    if current_land_type != goal_land_type:
        # Lógica para múltiplas ilhas pode ser adicionada aqui no futuro
        return {}
        
    island_reqs = all_reqs.get(current_land_type, {})
    
    for level in range(current_level + 1, goal_level + 1):
        level_reqs = island_reqs.get(level)
        if not level_reqs:
            continue

        for item, amount in level_reqs.items():
            if item not in ["Bumpkin Level", "Time"]:
                total_needed[item]['needed'] += amount

    return dict(sorted(total_needed.items()))
# ---> FIM DA FUNÇÃO DE CÁLCULO DE META TOTAL <---