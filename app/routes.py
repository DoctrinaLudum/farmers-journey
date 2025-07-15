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
    """
    Exibe o painel de bordo completo para uma fazenda específica.
    Esta versão é refatorada para ser mais robusta, isolando cada
    componente de análise de dados.
    """
    log.info(f"Iniciando a montagem do painel para a fazenda #{farm_id}")

    # 1. Começamos com um contexto base, com valores padrão seguros.
    context = {
        "farm_id": farm_id,
        "username": f"Fazenda #{farm_id}",
        "error": None, # Erro geral, apenas para falhas críticas.
        "sfl": 0,
        "coins": 0,
        "bumpkin_level": 0,
        "current_land_level": 0,
        "expansion_progress": None, # Será preenchido se a análise for bem-sucedida
        "expansion_goals": {},
        "categorized_inventory": {}, # Começa como um dicionário vazio
        "total_inventory_value": 0,
        "chores_list": []
    }

    # 2. Bloco Try/Except CRÍTICO: Buscar os dados principais.
    # Se esta parte falhar, não há nada a mostrar.
    try:
        farm_data, farm_error = sunflower_api.get_farm_data(farm_id)
        prices_data, prices_error = sunflower_api.get_prices_data()

        if farm_error or prices_error:
            # Este é um erro crítico, então paramos aqui.
            context['error'] = farm_error or prices_error
            log.error(f"Erro crítico ao buscar dados para a fazenda {farm_id}: {context['error']}")
            return render_template('dashboard.html', title=f"Erro na Fazenda #{farm_id}", **context)

    except Exception as e:
        log.exception(f"Exceção crítica não tratada ao buscar dados da API para a fazenda {farm_id}.")
        context['error'] = f"Falha ao comunicar com as APIs do jogo: {e}"
        return render_template('dashboard.html', title=f"Erro na Fazenda #{farm_id}", **context)


    # 3. Processamento de DADOS GERAIS (SFL, Moedas, Nível)
    # Esta parte é geralmente segura, mas podemos envolvê-la também.
    try:
        context['username'] = farm_data.get('username', 'N/A')
        context['sfl'] = Decimal(farm_data.get('balance', '0'))
        context['coins'] = int(farm_data.get('coins', 0))
        context['bumpkin_level'] = farm_data.get('bumpkin', {}).get('level', 0)
    except (TypeError, ValueError, InvalidOperation) as e:
        log.error(f"Erro ao processar dados gerais da fazenda {farm_id}: {e}")
        # Não definimos um erro geral, apenas deixamos os valores padrão.


    # 4. Processamento do ASSESSOR DE EXPANSÃO (Componente Isolado)
    try:
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
        context['current_land_level'] = farm_data.get('expansion_data', {}).get('land', {}).get('level')
    except Exception as e:
        log.error(f"Falha ao analisar o progresso de expansão para a fazenda {farm_id}: {e}")
        # O 'expansion_progress' continuará como None, e o template pode lidar com isso.


    # 5. Processamento do INVENTÁRIO (Componente Isolado)
    # Esta é a parte que estava a causar o erro!
    try:
        categorized_inventory = {}
        total_inventory_value = Decimal('0')
        inventory_from_api = farm_data.get('inventory', {})
        # Note: A API de preços já foi verificada acima.
        item_prices = prices_data.get("data", {}).get("p2p", {})

        # Esta lógica de categorização precisa ser adicionada ao seu config.py
        # Se você ainda não o fez, podemos trabalhar nisso a seguir.
        # Por enquanto, vamos supor que config.INVENTORY_CATEGORIES existe.
        if hasattr(config, 'INVENTORY_CATEGORIES'):
            for category, item_list in config.INVENTORY_CATEGORIES.items():
                owned_items_in_category = []
                for item_name in item_list:
                    if item_name in inventory_from_api:
                        quantity = Decimal(inventory_from_api[item_name])
                        if quantity > 0:
                            price = Decimal(str(item_prices.get(item_name, '0')))
                            value = quantity * price
                            total_inventory_value += value
                            owned_items_in_category.append({
                                "name": item_name, "amount": float(quantity), "value": float(value),
                                "icon": url_for('static', filename=f'images/{item_name}.png')
                            })
                if owned_items_in_category:
                    owned_items_in_category.sort(key=lambda x: x['name'])
                    categorized_inventory[category] = owned_items_in_category
        
        context['categorized_inventory'] = categorized_inventory
        context['total_inventory_value'] = float(total_inventory_value)
    except Exception as e:
        log.error(f"Falha ao analisar o inventário para a fazenda {farm_id}: {e}")
        # O 'categorized_inventory' continuará vazio. O erro não vai parar a página.


    # 6. Processamento das METAS DE EXPANSÃO (Dropdown)
    try:
        expansion_goals = {}
        current_land_type = farm_data.get('expansion_data', {}).get('land', {}).get('type')
        current_land_level = farm_data.get('expansion_data', {}).get('land', {}).get('level')
        if current_land_type and current_land_level:
            island_order = ["basic", "petal", "desert", "volcano"]
            if current_land_type in island_order:
                current_island_index = island_order.index(current_land_type)
                for island_name, levels in config.LAND_EXPANSION_REQUIREMENTS.items():
                    if island_name in island_order:
                        island_index = island_order.index(island_name)
                        if island_index < current_island_index: continue
                        valid_levels = [lvl for lvl in sorted(levels.keys()) if lvl > current_land_level] if island_index == current_island_index else sorted(levels.keys())
                        if valid_levels:
                            expansion_goals[island_name] = valid_levels
        context['expansion_goals'] = expansion_goals
    except Exception as e:
        log.error(f"Falha ao calcular as metas de expansão para a fazenda {farm_id}: {e}")

    # 7. Processamento da PESCA (Componente Isolado)
    context['fishing_info'] = None # Definir um valor padrão
    try:
        # A nossa nova função de análise é chamada aqui!
        context['fishing_info'] = analysis.analyze_fishing_data(farm_data)
    except Exception as e:
        log.error(f"Falha ao analisar os dados de pesca para a fazenda {farm_id}: {e}")
        # Em caso de erro, 'fishing_info' permanece None e a página não quebra.


    # No final, renderizamos o template com o que foi possível processar.
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