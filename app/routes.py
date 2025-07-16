# app/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from decimal import Decimal, InvalidOperation
import logging
from datetime import datetime

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
    Exibe o painel de bordo completo para uma fazenda específica.
    Esta versão é refatorada para usar a arquitetura de dados separados,
    garantindo que não haja perda de dados e mantendo a modularidade.
    """
    log.info(f"Iniciando a montagem do painel para a fazenda #{farm_id}")

    # 1. Começamos com um contexto base, com valores padrão seguros.
    context = {
        "farm_id": farm_id,
        "username": f"Fazenda #{farm_id}",
        "error": None,
        "sfl": 0, "coins": 0, "bumpkin_level": 0, "current_land_level": 0,
        "expansion_progress": None, "expansion_goals": {},
        "categorized_inventory": {}, "total_inventory_value": 0,
        "fishing_info": None,
        "expansion_construction_info": None
    }

    # 2. Bloco Try/Except CRÍTICO: Buscar os dados de ambas as APIs.
    # A nova função get_farm_data retorna os dados de forma separada.
    try:
        # Recebemos os dados separadamente, como planeado.
        main_farm_data, secondary_farm_data, api_error = sunflower_api.get_farm_data(farm_id)
        prices_data, prices_error = sunflower_api.get_prices_data()

        if api_error or prices_error:
            context['error'] = api_error or prices_error
            log.error(f"Erro crítico ao buscar dados para a fazenda {farm_id}: {context['error']}")
            return render_template('dashboard.html', title=f"Erro na Fazenda #{farm_id}", **context)

    except Exception as e:
        log.exception(f"Exceção crítica não tratada ao buscar dados das APIs para a fazenda {farm_id}.")
        context['error'] = f"Falha ao comunicar com as APIs do jogo: {e}"
        return render_template('dashboard.html', title=f"Erro na Fazenda #{farm_id}", **context)

    # 3. Processamento de DADOS GERAIS (SFL, Moedas, Nível)
    # Cada informação é buscada da sua fonte correta.
    try:
        context['username'] = main_farm_data.get('username', f"Fazenda #{farm_id}")
        context['sfl'] = Decimal(main_farm_data.get('balance', '0'))
        context['coins'] = int(main_farm_data.get('coins', 0))
        # O nível do Bumpkin vem dos dados secundários, que são mais detalhados.
        context['bumpkin_level'] = secondary_farm_data.get('bumpkin', {}).get('level', 0)
        current_land_level = secondary_farm_data.get('land', {}).get('level', 0)
        context['current_land_level'] = current_land_level


    except (TypeError, ValueError, InvalidOperation) as e:
        log.error(f"Erro ao processar dados gerais da fazenda {farm_id}: {e}")

     # NOVO E ATUALIZADO: Extrair dados da construção de expansão
    expansion_construction = main_farm_data.get("expansionConstruction")
    if expansion_construction and "readyAt" in expansion_construction:
        ready_at_timestamp = expansion_construction["readyAt"]
        # Converte o timestamp (em milissegundos) para um objeto datetime
        ready_at_datetime = datetime.fromtimestamp(ready_at_timestamp / 1000)
        
        context["expansion_construction_info"] = {
            "readyAt": ready_at_timestamp,
            "target_level": current_land_level + 1,
            "readyAt_formatted": ready_at_datetime.strftime('%d/%m/%Y %H:%M')
        }

    # 4. Processamento do ASSESSOR DE EXPANSÃO (Componente Isolado)
    try:
        # Passamos os dados separados para a função de análise.
        expansion_progress_data = analysis.analyze_expansion_progress(secondary_farm_data, main_farm_data)
        
        if expansion_progress_data and 'resources' in expansion_progress_data:
            for resource in expansion_progress_data['resources']:
                have = Decimal(str(resource.get('have', 0)))
                required = Decimal(str(resource.get('required', 0)))
                resource['shortfall'] = float(max(required - have, Decimal('0')))
                resource['surplus'] = float(max(have - required, Decimal('0')))
                icon_name = "Flower" if resource['name'] == "SFL" else resource['name']
                
                # AQUI ESTÁ A CORREÇÃO: Removemos o subdiretório '/resources' que não existe.
                # O caminho correto é diretamente dentro de 'images/'.
                resource['icon'] = url_for('static', filename=f'images/{icon_name}.png')
        
        context['expansion_progress'] = expansion_progress_data
        context['current_land_level'] = secondary_farm_data.get('land', {}).get('level', 0)
    except Exception as e:
        log.error(f"Falha ao analisar o progresso de expansão para a fazenda {farm_id}: {e}", exc_info=True)


    # 5. Processamento do INVENTÁRIO (Componente Isolado)
    try:
        inventory_from_api = main_farm_data.get('inventory', {})
        # A sua lógica de inventário, que já funciona, continua aqui.
        # Ela usará 'main_farm_data' e 'prices_data'.
        # ...
    except Exception as e:
        log.error(f"Falha ao analisar o inventário para a fazenda {farm_id}: {e}", exc_info=True)


    # 6. Processamento das METAS DE EXPANSÃO (Dropdown)
    try:
        expansion_goals = {}
        current_land_type = secondary_farm_data.get('land', {}).get('type')
        current_land_level = secondary_farm_data.get('land', {}).get('level')

        # Se uma expansão está em construção, o nosso nível "efetivo" para calcular
        # as próximas metas é o nível atual + 1.
        effective_current_level = current_land_level
        if context["expansion_construction_info"]:
            effective_current_level += 1

        if current_land_type and current_land_level is not None:
            island_order = ["basic", "petal", "desert", "volcano"]
            if current_land_type in island_order:
                current_island_index = island_order.index(current_land_type)
                for island_name, levels in config.LAND_EXPANSION_REQUIREMENTS.items():
                    if island_name in island_order:
                        island_index = island_order.index(island_name)
                        if island_index < current_island_index:
                            continue
                        
                        # A lógica agora usa 'effective_current_level'
                        valid_levels = [lvl for lvl in sorted(levels.keys()) if lvl > effective_current_level] if island_index == current_island_index else sorted(levels.keys())
                        
                        if valid_levels:
                            expansion_goals[island_name] = valid_levels
        context['expansion_goals'] = expansion_goals
    except Exception as e:
        log.error(f"Falha ao calcular metas de expansão: {e}", exc_info=True)

    # 7. Processamento da PESCA (Componente Isolado)
    try:
        # Passa os dados corretos para a função de análise.
        # A função em analysis.py agora já sabe onde encontrar as milestones.
        context['fishing_info'] = analysis.analyze_fishing_data(main_farm_data, secondary_farm_data)
    except Exception as e:
        log.error(f"Falha ao analisar os dados de pesca para a fazenda {farm_id}: {e}", exc_info=True)

    # No final, renderizamos o template com o que foi possível processar.
    return render_template('dashboard.html', title=f"Painel de {context['username']}", **context)


@bp.route('/api/goal_requirements/<int:farm_id>/<string:current_land_type>/<int:current_level>')
def api_goal_requirements(farm_id, current_land_type, current_level):
    """
    Endpoint da API para calcular os requisitos de uma meta de expansão,
    agora compatível com a arquitetura de dados separados.
    """
    try:
        goal_str = request.args.get('goal_level')
        if not goal_str:
            return jsonify({"error": "Parâmetro 'goal_level' ausente."}), 400

        goal_parts = goal_str.split('-')
        goal_land_type = goal_parts[0]
        goal_level = int(goal_parts[1])

        # CORREÇÃO AQUI: Chamada atualizada para a função get_farm_data
        main_farm_data, secondary_farm_data, farm_error = sunflower_api.get_farm_data(farm_id)
        prices_data, prices_error = sunflower_api.get_prices_data()

        if farm_error or prices_error:
            return jsonify({"error": f"Não foi possível buscar dados: {farm_error or prices_error}"}), 500

        # A função de cálculo não precisa de alterações
        goal_data = analysis.calculate_total_requirements(
            current_land_type=current_land_type,
            current_level=current_level,
            goal_land_type=goal_land_type,
            goal_level=goal_level,
            all_reqs=config.LAND_EXPANSION_REQUIREMENTS
        )

        if not goal_data or "requirements" not in goal_data:
             return jsonify({"requirements": None, "goal_level_display": goal_level})

        # Usamos main_farm_data para obter o inventário e balanços
        inventory = main_farm_data.get('inventory', {})
        sfl_balance = Decimal(main_farm_data.get('balance', '0'))
        coins_balance = Decimal(main_farm_data.get('coins', '0'))
        item_prices = prices_data.get("data", {}).get("p2p", {})
        
        processed_reqs = []
        total_sfl_cost = Decimal('0')

        # O resto da lógica da função permanece o mesmo
        for item, needed_total_dec in goal_data["requirements"].items():
            needed_total = Decimal(str(needed_total_dec))
            have = sfl_balance if item == "SFL" else (coins_balance if item == "Coins" else Decimal(inventory.get(item, '0')))
            shortfall = max(needed_total - have, Decimal('0'))
            
            price = Decimal(str(item_prices.get(item, '0')))
            value_of_needed = needed_total * price
            total_sfl_cost += value_of_needed
            icon_name = "Flower" if item == "SFL" else item

            processed_reqs.append({
                "name": item,
                "shortfall": f"{shortfall:.2f}",
                "needed": f"{needed_total:.2f}",
                "value_of_needed": f"{value_of_needed:.2f}",
                "icon": url_for('static', filename=f'images/{icon_name}.png')
            })

        response_data = {
            "goal_level_display": goal_level,
            "goal_land_type": goal_land_type,
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