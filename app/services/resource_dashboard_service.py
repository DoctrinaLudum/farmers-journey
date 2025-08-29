# app/services/resource_dashboard_service.py
import logging
from decimal import Decimal
from . import pricing_service, resource_analysis_service as resource_analysis
from ..domain import tools as tools_domain, resources as resources_domain, crops as crops_domain, fruits as fruits_domain, flowers as flowers_domain

log = logging.getLogger(__name__)

def _get_tool_cost(resource_name):
    """Gets the cost of the tool required to harvest a resource."""
    tool_name = None
    if resource_name in tools_domain.TOOLS_DATA:
        tool_name = "Axe"
    elif resource_name in tools_domain.TOOLS_DATA:
        tool_name = "Pickaxe"
    # Add other tools as necessary

    if tool_name:
        return pricing_service.get_item_prices(tool_name)
    return {}

def analyze_all_resources_for_dashboard(farm_data: dict) -> dict:
    """
    Analyzes and processes all possible resource data for the dashboard, calculating potential stats based on player's bonuses.

    Args:
        farm_data (dict): The complete farm data from the API.

    Returns:
        dict: A dictionary containing the processed data for the dashboard.
    """
    player_items = resource_analysis._get_player_items(farm_data)

    # Define all resources from domain
    all_resources = {
        "Recursos Básicos": list(resources_domain.RESOURCES_DATA.keys()),
        "Culturas": list(crops_domain.CROPS.keys()),
        "Frutas": list(fruits_domain.FRUIT_DATA.keys()),
        "Flores": list(flowers_domain.FLOWER_DATA.keys()),
    }

    processed_analyses = []

    for category, resource_list in all_resources.items():
        processed_group = {
            'title': category,
            'resources': {}
        }
        for resource_name in resource_list:

            # Get base data from domain
            if category == "Recursos Básicos":
                base_data = resources_domain.RESOURCES_DATA.get(resource_name, {})
                base_yield = base_data.get('yield', 1)
                base_recovery_time = base_data.get('recovery_time', 0)
            elif category == "Culturas":
                base_data = crops_domain.CROPS.get(resource_name, {})
                base_yield = 1 # Crops yield is always 1, bonuses are additive
                base_recovery_time = base_data.get('harvestSeconds', 0)
            elif category == "Frutas":
                base_data = fruits_domain.FRUIT_DATA.get(resource_name, {})
                base_yield = base_data.get('yield', 1)
                base_recovery_time = base_data.get('harvestSeconds', 0)
            elif category == "Flores":
                # For flowers, we are interested in the seed
                seed_name = f"{resource_name} Seed"
                base_data = flowers_domain.FLOWER_DATA.get(seed_name, {})
                base_yield = 1 # Flowers yield is 1
                base_recovery_time = base_data.get('plantSeconds', 0)
            else:
                continue

            # This is a simplified bonus calculation for the dashboard
            # A more detailed implementation would call the specific services (chop, mining, etc)
            # For now, we'll just show the base stats + a placeholder for bonuses

            # 1. Get Prices
            prices = pricing_service.get_item_prices(resource_name)
            sfl_price = prices.get('sfl', Decimal('0'))

            # 2. Get Tool Costs
            tool_cost_prices = _get_tool_cost(resource_name)
            tool_cost_sfl = tool_cost_prices.get('sfl', Decimal('0'))

            # 3. Yield (for now, just base)
            min_yield = base_yield
            max_yield = base_yield # Placeholder, real max yield depends on bonuses
            avg_yield = (Decimal(str(min_yield)) + Decimal(str(max_yield))) / 2

            # 4. Recovery Time
            recovery_time_seconds = base_recovery_time

            # 5. Profit Calculation
            profit_per_cycle_min = (Decimal(str(min_yield)) * sfl_price) - tool_cost_sfl
            profit_per_cycle_max = (Decimal(str(max_yield)) * sfl_price) - tool_cost_sfl

            sfl_per_hour = Decimal('0')
            if recovery_time_seconds > 0:
                avg_profit_per_cycle = (profit_per_cycle_min + profit_per_cycle_max) / 2
                cycles_per_hour = Decimal('3600') / Decimal(str(recovery_time_seconds))
                sfl_per_hour = avg_profit_per_cycle * cycles_per_hour

            processed_group['resources'][resource_name] = {
                'yield_range': f"{min_yield:.2f} - {max_yield:.2f}",
                'yield_avg': f"{avg_yield:.2f}",
                'recovery_time': recovery_time_seconds,
                'sfl_price': sfl_price,
                'tool_cost_sfl': tool_cost_sfl,
                'profit_per_cycle_min': profit_per_cycle_min,
                'profit_per_cycle_max': profit_per_cycle_max,
                'sfl_per_hour': sfl_per_hour,
                'bonuses': [] # Placeholder for bonuses
            }
        processed_analyses.append(processed_group)

    return {'analyses': processed_analyses}