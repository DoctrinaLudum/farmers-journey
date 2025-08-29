# app/services/resource_dashboard_service.py
import logging
from decimal import Decimal
from . import pricing_service
from ..domain import tools as tools_domain

log = logging.getLogger(__name__)

def _get_tool_cost(resource_name):
    """Gets the cost of the tool required to harvest a resource."""
    for tool, data in tools_domain.TOOLS.items():
        if resource_name in data.get("collects", []):
            return pricing_service.get_item_prices(tool)
    return {}

def analyze_resources_for_dashboard(unified_analyses: list, farm_data: dict) -> dict:
    """
    Analyzes and processes resource data for the dashboard, calculating profit and other metrics.

    Args:
        unified_analyses (list): A list of resource analysis data from other services.
        farm_data (dict): The complete farm data from the API.

    Returns:
        dict: A dictionary containing the processed data for the dashboard.
    """

    processed_analyses = []

    for analysis_group in unified_analyses:
        processed_group = {
            'title': analysis_group['title'],
            'resources': {}
        }
        for resource_name, data in analysis_group['resources'].items():
            summary = data.get('summary', {})

            # 1. Get Prices
            prices = pricing_service.get_item_prices(resource_name)
            sfl_price = prices.get('sfl', Decimal('0'))

            # 2. Get Tool Costs
            tool_cost_prices = _get_tool_cost(resource_name)
            tool_cost_sfl = tool_cost_prices.get('sfl', Decimal('0'))

            # 3. Yield
            min_yield = summary.get('yield', {}).get('min', 0)
            max_yield = summary.get('yield', {}).get('max', 0)
            avg_yield = (Decimal(str(min_yield)) + Decimal(str(max_yield))) / 2

            # 4. Recovery Time
            recovery_time_seconds = summary.get('recovery', {}).get('time_seconds', 0)

            # 5. Profit Calculation
            profit_per_cycle_min = (Decimal(str(min_yield)) * sfl_price) - tool_cost_sfl
            profit_per_cycle_max = (Decimal(str(max_yield)) * sfl_price) - tool_cost_sfl

            sfl_per_hour = Decimal('0')
            if recovery_time_seconds > 0:
                avg_profit_per_cycle = (profit_per_cycle_min + profit_per_cycle_max) / 2
                cycles_per_hour = Decimal('3600') / Decimal(str(recovery_time_seconds))
                sfl_per_hour = avg_profit_per_cycle * cycles_per_hour

            processed_group['resources'][resource_name] = {
                'summary': summary,
                'yield_range': f"{min_yield:.2f} - {max_yield:.2f}",
                'yield_avg': f"{avg_yield:.2f}",
                'recovery_time': recovery_time_seconds,
                'sfl_price': sfl_price,
                'tool_cost_sfl': tool_cost_sfl,
                'profit_per_cycle_min': profit_per_cycle_min,
                'profit_per_cycle_max': profit_per_cycle_max,
                'sfl_per_hour': sfl_per_hour,
                'bonuses': summary.get('bonuses', [])
            }
        processed_analyses.append(processed_group)

    return {'analyses': processed_analyses}
