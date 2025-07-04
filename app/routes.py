# app/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from decimal import Decimal, InvalidOperation
import logging

from . import sunflower_api
from . import analysis
import config

log = logging.getLogger(__name__)
bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET'])
def index():
    """Exibe a página inicial de boas-vindas com o formulário."""
    return render_template('index.html', title="Bem-vindo!")

@bp.route('/farm', methods=['POST'])
def handle_farm_request():
    """Recebe o Farm ID do formulário e redireciona para a página do painel."""
    farm_id = request.form.get('farm_id')
    if farm_id and farm_id.isdigit():
        return redirect(url_for('main.farm_dashboard', farm_id=farm_id))
    return redirect(url_for('main.index'))

@bp.route('/farm/<int:farm_id>')
def farm_dashboard(farm_id):
    """Exibe o painel de bordo completo para uma fazenda específica."""
    log.info(f"Iniciando a montagem do painel para a fazenda #{farm_id}")

    context = {
        "farm_id": farm_id,
        "username": f"Fazenda #{farm_id}",
        "error": None,
        "sfl": 0,
        "coins": 0,
        "bumpkin_level": 0,
        "current_land_level": 0,
        "expansion_progress": None,
        "expansion_goals": {},
        "inventory_list": [],
        "total_inventory_value": 0,
        "chores_list": []
    }

    farm_data, farm_error = sunflower_api.get_farm_data(farm_id)
    prices_data, prices_error = sunflower_api.get_prices_data()

    if farm_error or prices_error:
        context['error'] = farm_error or prices_error
        return render_template('dashboard.html', title=f"Erro na Fazenda #{farm_id}", **context)

    try:
        context['username'] = farm_data.get('username', 'N/A')
        context['sfl'] = Decimal(farm_data.get('balance', '0'))
        context['coins'] = int(farm_data.get('coins', 0))
        
        land_info = farm_data.get('expansion_data', {}).get('land', {})
        bumpkin_info = farm_data.get('bumpkin', {})
        context['bumpkin_level'] = bumpkin_info.get('level', 0)
        
        current_land_type = land_info.get('type')
        current_land_level = land_info.get('level')
        context['current_land_level'] = current_land_level

        expansion_progress_data = analysis.analyze_expansion_progress(farm_data)
        if expansion_progress_data and 'resources' in expansion_progress_data:
            for resource in expansion_progress_data['resources']:
                have = Decimal(str(resource.get('have', 0)))
                required = Decimal(str(resource.get('required', 0)))
                resource['shortfall'] = float(max(required - have, Decimal('0')))
                resource['surplus'] = float(max(have - required, Decimal('0')))
                icon_name = "Flower" if resource['name'] == "SFL" else resource['name']
                resource['icon'] = url_for('static', filename=f'images/{icon_name}.png')
        context['expansion_progress'] = expansion_progress_data
        
        # ---> INÍCIO DA NOVA LÓGICA: CATEGORIZAR O INVENTÁRIO <---
        categorized_inventory = {}
        total_inventory_value = Decimal('0')
        inventory_from_api = farm_data.get('inventory', {})
        item_prices = prices_data.get("data", {}).get("p2p", {})

        for category, item_list in config.INVENTORY_CATEGORIES.items():
            owned_items_in_category = []
            for item_name in item_list:
                # Verifica se o jogador possui o item
                if item_name in inventory_from_api:
                    try:
                        quantity = Decimal(inventory_from_api[item_name])
                        if quantity > 0:
                            # Tenta encontrar o preço do item
                            price_info = item_prices.get(item_name)
                            price = Decimal(str(price_info)) if price_info else Decimal('0')
                            
                            value = quantity * price
                            total_inventory_value += value
                            
                            # Adiciona o item à lista, independentemente de ter valor ou não
                            owned_items_in_category.append({
                                "name": item_name,
                                "amount": float(quantity),
                                "value": float(value), # Será 0.00 se não houver preço
                                "icon": url_for('static', filename=f'images/{item_name}.png')
                            })
                    except (InvalidOperation, TypeError):
                        log.warning(f"Ignorando item '{item_name}' com quantidade inválida.")
            
            if owned_items_in_category:
                owned_items_in_category.sort(key=lambda x: x['name']) # Ordena por nome
                categorized_inventory[category] = owned_items_in_category
        
        context['categorized_inventory'] = categorized_inventory
        context['total_inventory_value'] = float(total_inventory_value)
        # ---> FIM DA NOVA LÓGICA ---

        item_prices = prices_data.get("data", {}).get("p2p", {})
        raw_inventory = farm_data.get("inventory", {})
        inventory_list = []
        total_inventory_value = Decimal('0')

        for item_name, quantity_str in raw_inventory.items():
            if item_name in item_prices:
                try:
                    quantity = Decimal(quantity_str)
                    price = Decimal(str(item_prices[item_name]))
                    value = quantity * price
                    total_inventory_value += value
                    inventory_list.append({
                        "name": item_name, "quantity": quantity, "value": value,
                        "icon": url_for('static', filename=f'images/{item_name}.png')
                    })
                except (InvalidOperation, TypeError):
                    log.warning("Ignorando item '%s' do inventário com quantidade inválida.", item_name)
        
        inventory_list.sort(key=lambda x: x['name'])
        context['inventory_list'] = inventory_list
        context['total_inventory_value'] = total_inventory_value

        # Esta lógica calcula quais as metas de expansão válidas para mostrar no dropdown.
        expansion_goals = {}
        if current_land_type and current_land_level:
            island_order = ["basic", "petal", "desert", "volcano"]
            if current_land_type in island_order:
                current_island_index = island_order.index(current_land_type)
                for island_name, levels in config.LAND_EXPANSION_REQUIREMENTS.items():
                    if island_name in island_order:
                        island_index = island_order.index(island_name)
                        if island_index < current_island_index:
                            continue
                        
                        # Se for a ilha atual, pega apenas os níveis futuros. Se for uma ilha futura, pega todos os níveis.
                        valid_levels = [lvl for lvl in sorted(levels.keys()) if lvl > current_land_level] if island_index == current_island_index else sorted(levels.keys())
                        
                        if valid_levels:
                            expansion_goals[island_name] = valid_levels
        context['expansion_goals'] = expansion_goals

    except Exception:
        log.error("Erro CRÍTICO ao processar dados do painel para a fazenda %s", farm_id, exc_info=True)
        context['error'] = "Ocorreu um erro inesperado ao processar os dados da fazenda."

    return render_template('dashboard.html', title=f"Painel de {context['username']}", **context)


@bp.route('/api/goal_requirements/<int:farm_id>/<string:current_land_type>/<int:current_level>')
def api_goal_requirements(farm_id, current_land_type, current_level):
    """
    Endpoint da API para calcular os requisitos de uma meta de expansão,
    incluindo o custo total em SFL.
    """
    try:
        goal_str = request.args.get('goal_level')
        if not goal_str:
            return jsonify({"error": "Parâmetro 'goal_level' ausente."}), 400

        goal_parts = goal_str.split('-')
        goal_land_type = goal_parts[0]
        goal_level = int(goal_parts[1])

        # Busca os dados da fazenda e os preços dos itens
        farm_data, farm_error = sunflower_api.get_farm_data(farm_id)
        prices_data, prices_error = sunflower_api.get_prices_data()

        if farm_error or prices_error:
            return jsonify({"error": f"Não foi possível buscar dados: {farm_error or prices_error}"}), 500

        goal_data = analysis.calculate_total_requirements(
            current_land_type=current_land_type,
            current_level=current_level,
            goal_land_type=goal_land_type,
            goal_level=goal_level,
            all_reqs=config.LAND_EXPANSION_REQUIREMENTS
        )

        if not goal_data or "requirements" not in goal_data:
             return jsonify({"requirements": None, "goal_level_display": goal_level})

        inventory = farm_data.get('inventory', {})
        sfl_balance = Decimal(farm_data.get('balance', '0'))
        coins_balance = Decimal(farm_data.get('coins', 0))
        item_prices = prices_data.get("data", {}).get("p2p", {})
        
        processed_reqs = []
        total_sfl_cost = Decimal('0')

        for item, needed_total_dec in goal_data["requirements"].items():
            needed_total = Decimal(str(needed_total_dec))
            have = sfl_balance if item == "SFL" else (coins_balance if item == "Coins" else Decimal(inventory.get(item, '0')))
            shortfall = max(needed_total - have, Decimal('0'))
            
            # Calcula o custo em SFL para a quantidade total necessária
            price = Decimal(str(item_prices.get(item, '0')))
            value_of_needed = needed_total * price
            total_sfl_cost += value_of_needed
            icon_name = "Flower" if item == "SFL" else item

            processed_reqs.append({
                "name": item,
                # Formata com 2 casas decimais para o frontend
                "shortfall": f"{shortfall:.2f}",
                "needed": f"{needed_total:.2f}",
                "value_of_needed": f"{value_of_needed:.2f}",
                "icon": url_for('static', filename=f'images/{icon_name}.png')

            })

        response_data = {
            "goal_level_display": goal_level,
            "goal_land_type": goal_land_type,  # Nome da ilha
            "max_bumpkin_level": goal_data["max_bumpkin_level"],
            "total_time_str": goal_data["total_time_str"],
            "total_sfl_cost": f"{total_sfl_cost:.2f}", # Custo total
            "requirements": processed_reqs
        }
        return jsonify(response_data)

    except (IndexError, ValueError):
        return jsonify({"error": "Formato de 'goal_level' inválido."}), 400
    except Exception as e:
        log.error("Erro inesperado no endpoint da API de metas para a fazenda %s: %s", farm_id, e, exc_info=True)
        return jsonify({"error": "Um erro inesperado ocorreu."}), 500