# app/services/mushrooms_service.py
import logging
from decimal import Decimal
from datetime import datetime, timezone
from . import pricing_service

log = logging.getLogger(__name__)

# Define os colecionáveis relacionados a cogumelos e seus bônus
MUSHROOM_COLLECTIBLES = {
    "Mushroom House": {"boost": Decimal("0.2"), "resource": "Wild Mushroom"},
    "Fairy Circle": {"boost": Decimal("0.2"), "resource": "Wild Mushroom"},
}

# Define os vestíveis relacionados a cogumelos e seus bônus
MUSHROOM_WEARABLES = {
    "Mushroom Hat": {"boost": Decimal("0.1")},  # Aplica-se a todos os cogumelos
}

def _format_time_remaining(timestamp_ms):
    """Calcula e formata o tempo restante a partir de um timestamp em milissegundos."""
    if not timestamp_ms:
        return "N/A"
    
    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    remaining_seconds = (timestamp_ms - now_ms) / 1000
    
    if remaining_seconds <= 0:
        return "Pronto"
        
    days, remainder = divmod(remaining_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    parts = []
    if days > 0: parts.append(f"{int(days)}d")
    if hours > 0: parts.append(f"{int(hours)}h")
    if minutes > 0: parts.append(f"{int(minutes)}m")
    
    return " ".join(parts) if parts else f"{int(seconds)}s"

def analyze_mushroom_spawns(farm_data, active_bud_buffs):
    """
    Analisa os dados de cogumelos da fazenda, calcula os rendimentos com bônus,
    e prepara os dados para a visualização e uso interno.
    """
    mushrooms_data = farm_data.get("mushrooms")
    if not mushrooms_data or not mushrooms_data.get("mushrooms"):
        return None

    mushroom_status = {}
    
    # Lógica de bônus de colecionáveis
    active_collectible_bonuses = {}
    placed_collectibles = farm_data.get("collectibles", {})
    for collectible_name, bonus_info in MUSHROOM_COLLECTIBLES.items():
        if collectible_name in placed_collectibles and placed_collectibles[collectible_name]:
            active_collectible_bonuses[collectible_name] = bonus_info

    # Lógica de bônus de vestíveis
    active_wearable_bonuses = {}
    equipped_wearables = farm_data.get("bumpkin", {}).get("equipped", {})
    if equipped_wearables:
        for wearable_name, bonus_info in MUSHROOM_WEARABLES.items():
            if wearable_name in equipped_wearables.values():
                active_wearable_bonuses[wearable_name] = bonus_info

    total_sfl_value = Decimal("0")

    for mushroom_id, mushroom in mushrooms_data["mushrooms"].items():
        # O 'amount' da API já é o valor final com bônus aplicados
        api_final_amount = Decimal(str(mushroom.get("amount", 0)))
        mushroom_name = mushroom.get("name")

        calculated_bonus_amount = Decimal("0") # Este é o bônus que *teria sido* aplicado, para exibição
        applied_boosts = []
        
        for collectible, bonus_info in active_collectible_bonuses.items():
            if bonus_info.get("resource") == mushroom_name:
                boost = bonus_info["boost"]
                calculated_bonus_amount += boost
                applied_boosts.append({
                    "source_item": collectible,
                    "value": float(boost),
                    "operation": "add",
                    "source_type": "collectible"
                })

        for wearable, bonus_info in active_wearable_bonuses.items():
            boost = bonus_info["boost"]
            calculated_bonus_amount += boost
            applied_boosts.append({
                "source_item": wearable,
                "value": float(boost),
                "operation": "add",
                "source_type": "wearable"
            })

        bud_yield = Decimal(active_bud_buffs.get(mushroom_name, {}).get('yield', '0'))
        if bud_yield > 0:
            calculated_bonus_amount += bud_yield
            applied_boosts.append({
                "source_item": "Bud Boost",
                "value": float(bud_yield),
                "operation": "add",
                "source_type": "bud"
            })

        sfl_price = Decimal(str(pricing_service.get_item_prices(mushroom_name).get('sfl', 0))) # Preço do item
        sfl_value = api_final_amount * sfl_price # Valor SFL baseado no total já calculado pela API
        total_sfl_value += sfl_value

        mushroom_status[mushroom_id] = {
            "id": mushroom_id, "name": mushroom_name,
            "coordinates": {"x": mushroom.get("x"), "y": mushroom.get("y")}, # Coordenadas
            "base_amount": float(api_final_amount), # O valor base agora é o valor final da API
            "bonus_amount": float(calculated_bonus_amount), # O bônus calculado para exibição
            "total_amount": float(api_final_amount), # O total é o valor final da API
            "sfl_price": float(sfl_price), # Preço SFL do item
            "sfl_value": float(sfl_value), "resource_name": mushroom_name,
            "applied_boosts": applied_boosts,
        }

    next_wild_spawn_ms = mushrooms_data.get("spawnedAt", 0) + 16 * 60 * 60 * 1000
    next_magic_spawn_ms = mushrooms_data.get("magicSpawnedAt", 0) + 48 * 60 * 60 * 1000

    summary_data = {
        "total_ready": len(mushroom_status), "total_sfl_value": float(total_sfl_value),
        "next_wild_spawn_in": _format_time_remaining(next_wild_spawn_ms),
        "next_magic_spawn_in": _format_time_remaining(next_magic_spawn_ms),
        "next_wild_spawn_at": next_wild_spawn_ms,
        "next_magic_spawn_at": next_magic_spawn_ms,
    }

    # Adiciona os dados de resumo a cada cogumelo para o card de informações do mapa
    for mushroom_id in mushroom_status:
        mushroom_status[mushroom_id]["summary"] = summary_data

    view_data = {"mushroom_status": dict(sorted(mushroom_status.items())), "summary": summary_data}

    return {"view": view_data, "internal": mushroom_status}