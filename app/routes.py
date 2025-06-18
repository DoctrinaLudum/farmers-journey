# app/routes.py
from flask import Blueprint, render_template, request, redirect, url_for
from decimal import Decimal, InvalidOperation
import logging

# Use a importação relativa para buscar módulos de dentro do pacote 'app'
from . import sunflower_api
from . import database
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
    
    # --- PONTO DE PARTIDA CORRETO ---
    # Inicializa o contexto com TODAS as chaves que o template espera, com valores padrão.
    context = {
        "farm_id": farm_id,
        "username": f"Fazenda #{farm_id}",
        "error": None,
        "sfl": 0,
        "coins": 0,
        "inventory": {},
        "deliveries": [],
        "chores": {},
        "expansion_progress": None, # Garante que a chave 'expansion_progress' sempre exista
        "current_land_level": None # Garante que a chave 'current_land_level' sempre exista
    }

    # Busca os dados da fazenda
    farm_data, error = sunflower_api.get_farm_data(farm_id)

    # Se a API retornar um erro, ele será salvo no contexto e a página será renderizada
    if error:
        context['error'] = error
        # Renderiza a página mesmo com erro, mas com o contexto padrão seguro
        return render_template('dashboard.html', title=f"Erro na Fazenda #{farm_id}", **context)

    # Pega o nível objetivo da URL (ex: /farm/123?goal_level=desert-22)
    goal_str = request.args.get('goal_level')
    selected_goal = None
    goal_requirements = None

    if goal_str:
        try:
            goal_parts = goal_str.split('-')
            selected_goal = (goal_parts[0], int(goal_parts[1]))
        except (IndexError, ValueError):
            selected_goal = None # Ignora se o formato for inválido

    # Se a busca for bem-sucedida, preenche o contexto com os dados reais
    if farm_data:
        try:
            # Chama a função de análise para obter os dados de progresso
            expansion_progress_data = analysis.analyze_expansion_progress(farm_data)
            
            # Atualiza o contexto com todos os dados
            context.update({
                'username': farm_data.get('username', 'N/A'),
                'sfl': Decimal(farm_data.get('balance', '0')),
                'coins': int(farm_data.get('coins', 0)),
                'inventory': farm_data.get('inventory', {}),
                'chores': farm_data.get('choreBoard', {}).get('chores', {}),
                'bumpkin_level': farm_data.get('bumpkin', {}).get('level', 0),
                'expansion_progress': expansion_progress_data, # Adiciona o resultado da análise
                'current_land_level': farm_data.get('expansion_data', {}).get('land', {}).get('level')
            })

            # Pré-processa a lista de entregas
            deliveries_raw = farm_data.get('delivery', {}).get('orders', [])
            deliveries_processed = []
            for delivery in deliveries_raw:
                if delivery.get("id") and delivery.get("items"):
                    delivery['items_list'] = list(delivery['items'].items())
                    deliveries_processed.append(delivery)
            context['deliveries'] = deliveries_processed

            # Lógica da meta de Expansão
            current_land_type = farm_data.get('expansion_data', {}).get('land', {}).get('type')
            current_land_level = farm_data.get('expansion_data', {}).get('land', {}).get('level')

            if selected_goal and current_land_type:
                goal_requirements = analysis.calculate_total_requirements(
                    current_land_type=current_land_type,
                    current_level=current_land_level,
                    goal_land_type=selected_goal[0],
                    goal_level=selected_goal[1],
                    all_reqs=config.LAND_EXPANSION_REQUIREMENTS
                )

            # Prepara a lista de metas para o dropdown
            expansion_goals = {}
            for island, levels in config.LAND_EXPANSION_REQUIREMENTS.items():
                expansion_goals[island] = sorted(levels.keys())
            
            context['expansion_goals'] = expansion_goals
            context['selected_goal'] = selected_goal
            context['goal_requirements'] = goal_requirements

        except (InvalidOperation, ValueError, TypeError) as e:
            log.error(f"Erro ao processar os dados da fazenda para o painel: {e}")
            context['error'] = "Os dados recebidos da API continham formatos inesperados."

    return render_template('dashboard.html', title=f"Painel de {context['username']}", **context)