# app/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, json
from decimal import Decimal, InvalidOperation
import logging
from datetime import datetime
from .domain import expansions
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
    """
    Exibe o painel de bordo completo para uma fazenda específica, usando a
    estrutura de dados de expansão unificada.
    """
    log.info(f"Iniciando a montagem do painel para a fazenda #{farm_id}")

    # 1. Contexto base com valores padrão seguros.
    context = {
        "farm_id": farm_id, "username": f"Fazenda #{farm_id}", "error": None,
        "sfl": 0, "coins": 0, "bumpkin_level": 0, "current_land_level": 0,
        "current_land_type": "basic", "expansion_progress": None,
        "expansion_goals": {}, "fishing_info": None,
        "expansion_construction_info": None, "current_level_nodes": None
    }

    # 2. Busca dos dados das APIs.
    try:
        main_farm_data, secondary_farm_data, api_error = sunflower_api.get_farm_data(farm_id)
        prices_data, prices_error = sunflower_api.get_prices_data()

        if api_error or prices_error:
            context['error'] = api_error or prices_error
            return render_template('dashboard.html', title=f"Erro na Fazenda #{farm_id}", **context)
    except Exception as e:
        context['error'] = f"Falha crítica ao comunicar com as APIs: {e}"
        return render_template('dashboard.html', title=f"Erro na Fazenda #{farm_id}", **context)

    # 3. Processamento de Dados Gerais e de Construção.
    try:
        current_land_level = secondary_farm_data.get('land', {}).get('level', 0)
        current_land_type = secondary_farm_data.get('land', {}).get('type', 'basic')
        context.update({
            'username': main_farm_data.get('username', f"Fazenda #{farm_id}"),
            'sfl': Decimal(main_farm_data.get('balance', '0')),
            'coins': int(main_farm_data.get('coins', 0)),
            'bumpkin_level': secondary_farm_data.get('bumpkin', {}).get('level', 0),
            'current_land_level': current_land_level,
            'current_land_type': current_land_type
        })
        
        expansion_construction = main_farm_data.get("expansionConstruction")
        if expansion_construction and "readyAt" in expansion_construction:
            ready_at_timestamp = expansion_construction["readyAt"]
            # Compara a data de término com a data atual
            is_complete = datetime.now().timestamp() * 1000 > ready_at_timestamp

            context["expansion_construction_info"] = {
                "readyAt": ready_at_timestamp,
                "target_level": current_land_level + 1,
                "is_complete": is_complete # NOVO: Passa o estado de conclusão
            }
    except Exception as e:
        log.error(f"Erro ao processar dados gerais: {e}")

    # 4. Processamento dos NODES (recursos por nível) da Expansão Atual.
    try:
        expansion_details = expansions.EXPANSION_DATA.get(context['current_land_type'], {}).get(context['current_land_level'], {})
        nodes_data = expansion_details.get("nodes", {})
        if nodes_data:
            processed_nodes = []
            for node_name, count in nodes_data.items():
                if count > 0:
                    processed_nodes.append({
                        "name": node_name, "count": count,
                        "icon": url_for('static', filename=f'images/nodes/{node_name.lower().replace(" ", "_")}.png')
                    })
            context['current_level_nodes'] = sorted(processed_nodes, key=lambda x: x['name'])
    except Exception as e:
        log.error(f"Erro ao processar nodes da expansão atual: {e}")

    # 5. Processamento do ASSESSOR DE EXPANSÃO.
    try:
        expansion_progress_data = analysis.analyze_expansion_progress(secondary_farm_data, main_farm_data)
        
        # Este loop adiciona as chaves 'shortfall' e 'surplus' que o template precisa.
        if expansion_progress_data and 'resources' in expansion_progress_data:
            for resource in expansion_progress_data['resources']:
                have = Decimal(str(resource.get('have', 0)))
                required = Decimal(str(resource.get('required', 0)))
                resource['shortfall'] = float(max(required - have, Decimal('0')))
                resource['surplus'] = float(max(have - required, Decimal('0')))
        # --- FIM DO BLOCO RESTAURADO ---
        
        context['expansion_progress'] = expansion_progress_data
    except Exception as e:
        log.error(f"Falha ao analisar progresso de expansão: {e}", exc_info=True)

    # 6. Processamento das METAS DE EXPANSÃO.
    try:
        expansion_goals = {}
        effective_current_level = context['current_land_level']
        if context["expansion_construction_info"]:
            effective_current_level += 1

        island_order = ["basic", "petal", "desert", "volcano"]
        current_land_type = context['current_land_type']
        if current_land_type in island_order:
            current_island_index = island_order.index(current_land_type)
            for island_name, levels_data in expansions.EXPANSION_DATA.items():
                if island_name in island_order:
                    island_index = island_order.index(island_name)
                    if island_index < current_island_index:
                        continue
                    
                    levels = levels_data.keys()
                    valid_levels = [lvl for lvl in sorted(levels) if lvl > effective_current_level] if island_index == current_island_index else sorted(levels)
                    
                    if valid_levels:
                        expansion_goals[island_name] = valid_levels
        context['expansion_goals'] = expansion_goals
    except Exception as e:
        log.error(f"Falha ao calcular metas de expansão: {e}", exc_info=True)

    # 7. Processamento da PESCA.
    try:
        context['fishing_info'] = analysis.analyze_fishing_data(main_farm_data, secondary_farm_data)
    except Exception as e:
        log.error(f"Falha ao analisar dados de pesca: {e}", exc_info=True)

    # 8. Processamento do Mini-Mapa de Expansão
    try:
        map_plots = []
        # Define os lotes que pertencem a cada tipo de ilha
        island_map = {
            "basic": range(1, 10), "petal": range(10, 16),
            "desert": range(16, 26), "volcano": range(26, 31)
        }

        # Pega a informação completa da construção, se existir
        construction_info = context.get("expansion_construction_info")

        # Variáveis para controlar a legenda dinâmica
        context['in_progress_plot_island'] = None
        context['complete_plot_island'] = None

        for plot_number, coords in expansions.EXPANSION_COORDINATES.items():
            if plot_number == 0: continue

            plot_state = "locked"
            if plot_number <= context['current_land_level']:
                plot_state = "owned"
            elif construction_info and plot_number == construction_info["target_level"]:
                plot_island_type = next((island for island, r in island_map.items() if plot_number in r), "basic")
                if construction_info["is_complete"]:
                    plot_state = "construction_complete"
                    context['complete_plot_island'] = plot_island_type # Guarda a cor da ilha
                else:
                    plot_state = "in_progress"
                    context['in_progress_plot_island'] = plot_island_type # Guarda a cor da ilha
            elif plot_number == context['current_land_level'] + 1:
                plot_state = "next_available"
            
            plot_island = next((island for island, r in island_map.items() if plot_number in r), "basic")
            
            map_plots.append({
                "number": plot_number, "x": coords['x'], "y": coords['y'],
                "state": plot_state, "island": plot_island,
                "requirements_data": json.dumps(expansions.EXPANSION_DATA.get(plot_island, {}).get(plot_number, {}).get("requirements", {})),
                "nodes_data": json.dumps({k: v for k, v in expansions.EXPANSION_DATA.get(plot_island, {}).get(plot_number, {}).get("nodes", {}).items() if v > 0})
            })
        
        context['map_plots'] = map_plots
    except Exception as e:
        log.error(f"Erro ao processar o mapa de expansão: {e}")

    return render_template('dashboard.html', title=f"Painel de {context['username']}", **context)


@bp.route('/api/goal_requirements/<int:farm_id>/<string:current_land_type>/<int:current_level>')
def api_goal_requirements(farm_id, current_land_type, current_level):
    """
    Endpoint da API para calcular os requisitos de uma meta de expansão.
    """
    try:
        goal_str = request.args.get('goal_level')
        if not goal_str:
            return jsonify({"error": "Parâmetro 'goal_level' ausente."}), 400

        goal_parts = goal_str.split('-')
        goal_land_type = goal_parts[0]
        goal_level = int(goal_parts[1])

        # Busca os dados mais recentes da fazenda para a verificação
        main_farm_data, _, farm_error = sunflower_api.get_farm_data(farm_id)
        prices_data, prices_error = sunflower_api.get_prices_data()

        if farm_error or prices_error:
            return jsonify({"error": f"Não foi possível buscar dados: {farm_error or prices_error}"}), 500

        # Determina o nível inicial efetivo para o cálculo
        effective_start_level = current_level
        if main_farm_data.get("expansionConstruction"):
            effective_start_level += 1

        goal_data = analysis.calculate_total_requirements(
            current_land_type=current_land_type,
            current_level=effective_start_level, # Usa o nível efetivo
            goal_land_type=goal_land_type,
            goal_level=goal_level
        )

        if not goal_data or "requirements" not in goal_data:
             return jsonify({"requirements": None, "goal_level_display": goal_level})

        # O resto da função permanece igual, pois já está a funcionar corretamente.
        inventory = main_farm_data.get('inventory', {})
        sfl_balance = Decimal(main_farm_data.get('balance', '0'))
        coins_balance = Decimal(main_farm_data.get('coins', '0'))
        item_prices = prices_data.get("data", {}).get("p2p", {})
        
        processed_reqs = []
        total_sfl_cost = Decimal('0')

        for item, needed_total_dec in goal_data["requirements"].items():
            needed_total = Decimal(str(needed_total_dec))
            have = sfl_balance if item == "SFL" else (coins_balance if item == "Coins" else Decimal(inventory.get(item, '0')))
            shortfall = max(needed_total - have, Decimal('0'))
            
            price = Decimal(str(item_prices.get(item, '0')))
            value_of_needed = needed_total * price
            total_sfl_cost += value_of_needed
            icon_name = "Flower" if item == "SFL" else item

            processed_reqs.append({
                "name": item, "shortfall": f"{shortfall:.2f}",
                "needed": f"{needed_total:.2f}", "value_of_needed": f"{value_of_needed:.2f}",
                "icon": url_for('static', filename=f'images/{icon_name}.png')
            })

        response_data = {
            "goal_level_display": goal_level, "goal_land_type": goal_land_type,
            "max_bumpkin_level": goal_data["max_bumpkin_level"],
            "total_time_str": goal_data["total_time_str"],
            "total_sfl_cost": f"{total_sfl_cost:.2f}",
            "requirements": processed_reqs
        }
        return jsonify(response_data)

    except (IndexError, ValueError):
        return jsonify({"error": "Formato de 'goal_level' inválido."}), 400
    except Exception as e:
        log.error("Erro inesperado no endpoint da API de metas para a fazenda %s: %s", farm_id, e, exc_info=True)
        return jsonify({"error": "Um erro inesperado ocorreu."}), 500
