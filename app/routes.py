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
        "farm_id": farm_id, "username": f"Fazenda #{farm_id}", "error": None, "expansion_progress": None
    }

    farm_data, error = sunflower_api.get_farm_data(farm_id)
    if error:
        context['error'] = error
        return render_template('dashboard.html', title=f"Erro na Fazenda #{farm_id}", **context)
    if not farm_data:
        context['error'] = "Não foi possível obter os dados da fazenda."
        return render_template('dashboard.html', title=f"Erro na Fazenda #{farm_id}", **context)

    try:
        # Extrai os dicionários principais para simplificar o acesso e melhorar a legibilidade
        land_info = farm_data.get('expansion_data', {}).get('land', {})
        bumpkin_info = farm_data.get('bumpkin', {})
        
        current_land_type = land_info.get('type')
        current_land_level = land_info.get('level')

        expansion_progress_data = analysis.analyze_expansion_progress(farm_data)

        context.update({
            'username': farm_data.get('username', 'N/A'),
            'sfl': Decimal(farm_data.get('balance', '0')),
            'coins': int(farm_data.get('coins', 0)),
            'bumpkin_level': bumpkin_info.get('level', 0),
            'current_land_level': current_land_level,
            'expansion_progress': expansion_progress_data
        })

        if expansion_progress_data and 'resources' in expansion_progress_data:
            for resource in expansion_progress_data['resources']:
                have = Decimal(str(resource.get('have', 0)))
                required = Decimal(str(resource.get('required', 0)))
                resource['shortfall'] = float(max(required - have, Decimal('0')))
                resource['surplus'] = float(max(have - required, Decimal('0')))
                icon_filename = f"{resource['name']}.png"
                resource['icon'] = url_for('static', filename=f'images/{icon_filename}')

        expansion_goals = {}
        if current_land_type and current_land_level:
            island_order = ["basic", "petal", "desert", "volcano"]
            if current_land_type in island_order:
                current_island_index = island_order.index(current_land_type)
                for island_name, levels in config.LAND_EXPANSION_REQUIREMENTS.items():
                    if island_name in island_order:
                        island_index = island_order.index(island_name)
                        if island_index < current_island_index: continue
                        valid_levels = [lvl for lvl in sorted(levels.keys()) if lvl > current_land_level] if island_index == current_island_index else sorted(levels.keys())
                        if valid_levels: expansion_goals[island_name] = valid_levels
        context['expansion_goals'] = expansion_goals

    except Exception as e:
        log.error(f"Erro ao processar dados do painel: {e}")
        context['error'] = "Ocorreu um erro ao preparar os dados do painel."

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

        farm_data, error = sunflower_api.get_farm_data(farm_id)
        if error:
            return jsonify({"error": f"Não foi possível buscar dados da fazenda: {error}"}), 500
        
        goal_data = analysis.calculate_total_requirements(
            current_land_type=current_land_type,
            current_level=current_level,
            goal_land_type=goal_land_type,
            goal_level=goal_level,
            all_reqs=config.LAND_EXPANSION_REQUIREMENTS
        )

        if not goal_data or "requirements" not in goal_data:
             return jsonify({
                 "requirements": None,
                 "goal_level_display": goal_level
             })

        inventory = farm_data.get('inventory', {})
        sfl_balance = Decimal(farm_data.get('balance', '0'))
        coins_balance = int(farm_data.get('coins', 0))
        
        processed_reqs = []
        for item, needed_total in goal_data["requirements"].items():
            have = sfl_balance if item == "SFL" else (coins_balance if item == "Coins" else Decimal(inventory.get(item, '0')))
            shortfall = max(Decimal(str(needed_total)) - have, Decimal('0'))
            processed_reqs.append({
                "name": item,
                "shortfall": int(shortfall) if shortfall % 1 == 0 else float(shortfall),
                "needed": needed_total,
                "icon": url_for('static', filename=f'images/{item}.png')
            })

        response_data = {
            "goal_level_display": goal_level,
            "max_bumpkin_level": goal_data["max_bumpkin_level"],
            "total_time_str": goal_data["total_time_str"],
            "requirements": processed_reqs
        }
        return jsonify(response_data)

    except (IndexError, ValueError):
        return jsonify({"error": "Formato de 'goal_level' inválido."}), 400
    except Exception as e:
        log.error(f"Erro inesperado no endpoint da API de metas: {e}")
        return jsonify({"error": "Um erro inesperado ocorreu."}), 500