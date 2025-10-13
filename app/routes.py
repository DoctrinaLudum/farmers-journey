# app/routes.py
import logging
from collections import defaultdict
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation

from flask import (Blueprint, current_app, json, jsonify, redirect,
                   render_template, request, url_for)
from markupsafe import Markup

import config

from . import analysis, game_state, sunflower_api
from .analysis import build_bumpkin_image_url
from .cache import cache  # Importa o objeto 'cache' diretamente
from .domain import crops as crops_domain
from .domain import expansions
from .domain import flowers as flower_domain
from .domain import foods as foods_domain
from .domain import fruits as fruit_domain
from .domain import npcs as npc_domain
from .game_state import GAME_STATE
from .services import (animation_service, bud_service, chop_service, chores_service,
                       crop_machine_service, crop_service, delivery_service,
                       exchange_service, expansion_service,
                       farm_layout_service, flower_service, fruit_service,
                       greenhouse_service, mining_service, mushrooms_service,
                       pricing_service, summary_service, treasure_dig_service, calendar_service)

log = logging.getLogger(__name__)
bp = Blueprint('main', __name__)

from datetime import datetime


@bp.app_template_filter()
def datetimeformat(value, format='%Y-%m-%d %H:%M:%S'):
    if value is None:
        return ''
    return datetime.fromtimestamp(value / 1000).strftime(format)

@bp.app_template_filter()
def time_remaining(timestamp_ms):
    """Calcula e formata o tempo restante a partir de um timestamp em milissegundos."""
    if not timestamp_ms:
        return "N/A"
    
    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    remaining_seconds = (timestamp_ms - now_ms) / 1000
    
    if remaining_seconds <= 0:
        return "Pronta"
        
    days, remainder = divmod(remaining_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    parts = []
    if days > 0: parts.append(f"{int(days)}d")
    if hours > 0: parts.append(f"{int(hours)}h")
    if minutes > 0: parts.append(f"{int(minutes)}m")
    
    return " ".join(parts) if parts else f"{int(seconds)}s"

@bp.app_template_filter()
def format_seconds_to_hms(total_seconds):
    """Formata uma duração em segundos para o formato hh:mm:ss."""
    if not isinstance(total_seconds, (int, float, Decimal)) or total_seconds < 0:
        return "00:00:00"
    
    total_seconds = int(total_seconds)
    
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

@bp.app_template_filter()
def get_item_prices(item_name):
    """
    Filtro do Jinja para buscar os preços de um item usando o pricing_service.
    Retorna um dicionário de preços (ex: {'coins': 10, 'sfl': 1}).
    """
    if not item_name: return {}
    return pricing_service.get_item_prices(item_name)

@bp.app_template_filter()
def generate_currency_html(sfl_value, prefix=""):
    """
    Filtro do Jinja para gerar a estrutura HTML com todos os valores de moeda pré-calculados.
    Isso espelha a funcionalidade de `generateCurrencyHTML` no TypeScript.
    """
    if sfl_value is None:
        return ""
        
    try:
        sfl_value = Decimal(sfl_value)
    except (InvalidOperation, TypeError):
        return ""

    rates = exchange_service.get_exchange_rates().get('sfl', {})
    
    usd_rate = Decimal(str(rates.get('usd', 0)))
    brl_rate = Decimal(str(rates.get('brl', 0)))

    usd_value = sfl_value * usd_rate
    brl_value = sfl_value * brl_rate

# Replica a lógica de formatação do TypeScript, incluindo as bandeiras
    sfl_flag = '<img src="/static/images/resources/flower.webp" alt="SFL" class="icon icon-1x me-1">'
    usd_flag = '<span class="fi fi-us me-2"></span>'
    brl_flag = '<span class="fi fi-br me-2"></span>'
    sfl_formatted = f"{sfl_flag}{prefix}{sfl_value:,.2f} Flower"
    usd_formatted = f"{usd_flag}{prefix}US$ {usd_value:,.2f}"
    brl_formatted = f"{brl_flag}{prefix}R$ {brl_value:,.2f}"
    html = f"""<span class="currency-container">
        <span class="currency-value-display currency-flower">{sfl_formatted}</span>
        <span class="currency-value-display currency-usd">{usd_formatted}</span>
        <span class="currency-value-display currency-brl">{brl_formatted}</span>
    </span>"""    
    return Markup(html)


@bp.route('/api/animated-characters')
def api_animated_characters():
    """
    Endpoint da API que busca os personagens animados do serviço e os retorna em JSON.
    """
    try:
        characters = animation_service.get_animated_characters()
        return jsonify(characters)
    except Exception as e:
        log.error(f"Erro ao buscar personagens animados para a API: {e}", exc_info=True)
        return jsonify({"error": "Não foi possível buscar a lista de personagens"}), 500


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

@bp.route('/api/exchange-rates')
@cache.cached(timeout=600)  # Cache de 10 minutos para este endpoint
def api_exchange_rates():
    """
    Endpoint da API para fornecer as taxas de câmbio em formato JSON.
    O frontend chamará este endpoint para inicializar o conversor de moeda.
    """
    try:
        rates = exchange_service.get_exchange_rates()
        return jsonify(rates)
    except Exception as e:
        log.error(f"Erro ao buscar taxas de câmbio para a API: {e}", exc_info=True)
        return jsonify({"error": "Não foi possível buscar as taxas de câmbio"}), 500

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
        "expansion_construction_info": None, "current_level_nodes": None, "bumpkin_image_url": None,
        "chore_analysis": None, "crop_machine_analysis": None, "greenhouse_analysis": None,

        # Domínios de dados para uso nos templates
        "flower_domain": flower_domain, "fruit_domain": fruit_domain, "foods_domain": foods_domain,
        # Funções helper para os templates
        "crops_domain": crops_domain,
        "get_item_image_path": analysis.get_item_image_path,
        "enumerate": enumerate
    }

    unified_analyses = [] # Inicialização movida para o início da função

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

    

    # CORREÇÃO: Adiciona os dados de preços ao contexto para serem usados no `base.html`.
    context['prices_data'] = prices_data

    # 3. Processamento de Dados Gerais e de Construção.
    try:
        current_land_level = int(secondary_farm_data.get('land', {}).get('level', 0))
        current_land_type = secondary_farm_data.get('land', {}).get('type', 'basic')
        
        # CORREÇÃO: Determina se o usuário é VIP verificando a data de expiração
        # na chave 'vip' dos dados da API. Esta é a forma correta e robusta.
        vip_data = main_farm_data.get("vip")
        is_vip = False
        if vip_data and "expiresAt" in vip_data:
            now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
            is_vip = vip_data["expiresAt"] > now_ms

        context.update({
            'username': main_farm_data.get('username', f"Fazenda #{farm_id}"),
            'sfl': Decimal(main_farm_data.get('balance', '0')),
            'coins': int(main_farm_data.get('coins', 0)),
            'bumpkin_level': secondary_farm_data.get('bumpkin', {}).get('level', 0),
            'current_land_level': current_land_level,
            'current_land_type': current_land_type,
            'is_vip': is_vip
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

    # 3.5. Processamento da Imagem do Bumpkin
    try:
        bumpkin_data = main_farm_data.get("bumpkin", {})
        equipped_items = bumpkin_data.get("equipped")

        # NOVO: Corrige o nome do item "Parsnip" vindo da API para "Parsnip Sword"
        if equipped_items and equipped_items.get("Tool") == "Parsnip":
            log.info("API retornou 'Parsnip' como ferramenta, corrigindo para 'Parsnip Sword'.")
            equipped_items["Tool"] = "Parsnip Sword"
            
        if equipped_items:
            # Passa o dicionário de itens para a função de construção
            context['bumpkin_image_url'] = analysis.build_bumpkin_image_url(equipped_items)
            log.info(f"URL da imagem do Bumpkin gerada para a fazenda #{farm_id}")
        else:
            log.warning(f"Dicionário 'equipped' não encontrado para a fazenda #{farm_id}.")
            
    except Exception as e:
        log.error(f"Erro ao processar a imagem do Bumpkin para a fazenda #{farm_id}: {e}", exc_info=True)  

    # 4. Processamento dos NODES (recursos por nível) da Expansão Atual.
    try:
        expansion_details = expansions.EXPANSION_DATA.get(context['current_land_type'], {}).get(context['current_land_level'], {})
        nodes_data = expansion_details.get("nodes", {})
        if nodes_data:
            processed_nodes = []
            for node_name, count in nodes_data.items():
                if count > 0:
                    processed_nodes.append({"name": node_name, "count": count})
            context['current_level_nodes'] = sorted(processed_nodes, key=lambda x: x['name'])
    except Exception as e:
        log.error(f"Erro ao processar nodes da expansão atual: {e}")

    # 5. Processamento do ASSESSOR DE EXPANSÃO.
    try:
        expansion_progress_data = expansion_service.analyze_expansion_progress(secondary_farm_data, main_farm_data)
        
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
        if context.get("expansion_construction_info"):
            effective_current_level += 1

        island_order = expansions.ISLAND_ORDER
        current_land_type = context['current_land_type']
        
        if current_land_type in island_order:
            current_island_index = island_order.index(current_land_type)
            
            for island_name in island_order:
                island_index = island_order.index(island_name)
                
                if island_index < current_island_index:
                    continue
                
                levels_data = expansions.EXPANSION_DATA.get(island_name, {})
                
                # --- LÓGICA FINAL E CORRETA ---

                # 1. Verifica se a ilha tem algum requisito. Se não, não é um objetivo válido.
                if not any(info.get("requirements") for info in levels_data.values()):
                    continue # Ignora ilhas como a "Swamp" por enquanto

                # 2. Converte os níveis para números de forma segura
                levels_as_int = []
                for lvl in levels_data.keys():
                    try:
                        levels_as_int.append(int(lvl))
                    except (ValueError, TypeError):
                        continue
                levels_as_int.sort()

                # 3. Determina quais níveis são válidos para a meta
                if island_index == current_island_index:
                    # Para a ilha atual, apenas níveis futuros são válidos
                    valid_levels = [lvl for lvl in levels_as_int if lvl > effective_current_level]
                else:
                    # Para ilhas futuras, todos os níveis são válidos
                    valid_levels = levels_as_int
                
                # 4. Adiciona ao dicionário de metas se houver níveis válidos
                if valid_levels:
                    expansion_goals[island_name] = valid_levels
                    
        context['expansion_goals'] = expansion_goals
    except Exception as e:
        log.error(f"Falha ao calcular metas de expansão: {e}", exc_info=True)

    # 7. Processamento da PESCA.
    try:
        # Chama a função de análise APENAS UMA VEZ e guarda o resultado.
        fishing_info = analysis.analyze_fishing_data(main_farm_data, secondary_farm_data)

        # Se a análise foi bem-sucedida, adiciona a informação da estação.
        if fishing_info:
            current_season = main_farm_data.get("season", {}).get("season", "spring")
            fishing_info['current_season'] = current_season
                
        # Passa o resultado já modificado para o contexto.
        context['fishing_info'] = fishing_info
    except Exception as e:
        log.error(f"Falha ao analisar dados de pesca: {e}", exc_info=True)
    


    # 8. Processamento do Mini-Mapa de Expansão
    try:
        map_plots = []
        # Define os lotes que pertencem a cada tipo de ilha
        island_map = {
            "basic": range(1, 10), "petal": range(10, 16),
            "desert": range(16, 26), "volcano": range(26, 31),
            "swamp": range(31, 37)
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
            # elif plot_number == context['current_land_level'] + 1:
            #    plot_state = "next_available"
            
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

    # 9. Processamento das FLORES.
    try:
        context.update(analysis.process_flower_info(main_farm_data))
    except Exception as e:
        log.error(f"Falha ao analisar dados de flores: {e}", exc_info=True)

    # 10. Processamento de Presentes de NPCs
    try:
        context['npc_gift_info'] = analysis.process_npc_gifts(main_farm_data)
    except Exception as e:
        log.error(f"Falha ao processar dados de presentes de NPCs: {e}", exc_info=True)
        context['npc_gift_info'] = [] # Garante que a chave exista no contexto

    # 11. Processamento do Quadro de Tarefas (Chore Board)
    try:
        context['chore_analysis'] = chores_service.analyze_chore_board(main_farm_data)
        log.info(f"Análise do Chore Board concluída para a fazenda #{farm_id}.")
    except Exception as e:
        log.error(f"Falha ao processar dados do Chore Board: {e}", exc_info=True)

    # 11. Processamento de Escavação de Tesouros (Desert Digging)
    try:
        context['treasure_dig_info'] = treasure_dig_service.analyze_desert_digging_data(
            main_farm_data,
            seasonal_artefact=game_state.GAME_STATE.get('current_artefact_name')
        )
    except Exception as e:
        log.error(f"Falha ao processar dados de digitação de tesouros: {e}", exc_info=True)
        # Garante que a estrutura padrão exista em caso de erro para evitar que o template quebre
        context['treasure_dig_info'] = {
            'grid_mirror': [],
            'stats': {
                'total_digs': 0,
                'items_found': {},
                'tool_usage': {},
                'streak': {}
            },
            'patterns': {'current': [], 'completed': []},
            'hints': []
        }

    # 12. Processamento de Entregas (Deliveries)
    try:
        context['delivery_analysis'] = delivery_service.analyze_deliveries(
            farm_data=main_farm_data, # A função de delivery agora precisa dos dados completos
            game_state=game_state.GAME_STATE
        )
        log.info(f"Análise de entregas concluída para a fazenda #{farm_id}.")
    except Exception as e:
        log.error(f"Falha ao processar dados de entregas: {e}", exc_info=True)

    # 12. Processamento de Buffs de Buds (MOVIDO PARA CIMA para ser usado por outros serviços)
    context['bud_analysis'] = None
    active_bud_buffs = {}  # Inicializa como um dicionário vazio para segurança
    try:
        bud_data = bud_service.analyze_bud_buffs(main_farm_data)
        if bud_data:
            context['bud_analysis'] = bud_data
            # Extrai os bônus ativos do novo formato interno para passar a outros serviços.
            # Acessa de forma segura a estrutura aninhada para obter os bônus.
            active_bud_buffs = bud_data.get("internal", {}).get("active_buffs", {})
            # DEBUG: Log para verificar quais bônus de Bud estão sendo passados para outros serviços.
            log.debug(f"Passing the following active_bud_buffs to services: {active_bud_buffs}")
            log.info(f"Análise de Buds concluída com sucesso para a fazenda #{farm_id}.")
    except Exception as e:
        log.error(f"Falha ao analisar buffs de Buds: {e}", exc_info=True)

    # Lista para agregar todas as análises de recursos para o painel de depuração
    resource_analyses = []
    # 19. Agregação e Padronização de Dados para o Painel Unificado

    # 13. Processamento de Recursos de Madeira (Wood) - CORRIGIDO
    context['wood_analysis'] = None
    wood_data = None
    try:
        # Passa a variável 'active_bud_buffs' que acabamos de criar.
        # Agora o serviço de madeira sempre receberá um dicionário, mesmo que vazio.
        wood_data = chop_service.analyze_wood_resources(main_farm_data)
    
        # Acessa a chave 'view' que contém os dados formatados para o template.
        wood_view_data = wood_data.get("view") if wood_data else None
    
        if wood_view_data and 'summary' in wood_view_data and 'tree_status' in wood_view_data:
            # Passa apenas os dados da view para o contexto, para que o template não precise ser alterado.
            context['wood_analysis'] = wood_view_data
            resource_analyses.append({'name': 'Madeira', 'data': wood_view_data})
            log.info(f"Análise de madeira (com buffs de Bud) processada com sucesso para a fazenda #{farm_id}.")
        else:
            log.warning(f"Dados de análise de madeira ausentes ou incompletos para a fazenda #{farm_id}.")
    except Exception as e:
        log.error(f"Falha ao analisar dados de madeira: {e}", exc_info=True)

    # 14. Processamento de Recursos de Mineração (Mining)
    context['mining_analysis'] = None
    mining_data = None
    try:
        mining_data = mining_service.analyze_mining_resources(main_farm_data)
        mining_view_data = mining_data.get("view") if mining_data else None

        if mining_view_data:
            context['mining_analysis'] = mining_view_data
            resource_analyses.append({'name': 'Mineração', 'data': mining_view_data})
            log.info(f"Análise de mineração processada com sucesso para a fazenda #{farm_id}.")
        else:
            log.warning(f"Dados de análise de mineração ausentes para a fazenda #{farm_id}.")
    except Exception as e:
        log.error(f"Falha ao analisar dados de mineração: {e}", exc_info=True)

    # 15. Processamento de Culturas (Crops)
    context['crop_analysis'] = None
    crop_data = None
    try:
        # NOVO: Chama o calendar_service refatorado para obter bônus para a categoria 'Crop'
        calendar_boosts = calendar_service.get_active_event_boosts(main_farm_data, 'Crop')

        # Passa os boosts de calendário para o serviço de culturas
        crop_data = crop_service.analyze_crop_resources(main_farm_data, calendar_boosts=calendar_boosts)
        crop_view_data = crop_data.get("view") if crop_data else None

        if crop_view_data:
            context['crop_analysis'] = crop_view_data
            resource_analyses.append({'name': 'Culturas', 'data': crop_view_data})
            log.info(f"Análise de culturas processada com sucesso para a fazenda #{farm_id}.")
        else:
            log.warning(f"Dados de análise de culturas ausentes para a fazenda #{farm_id}.")
    except Exception as e:
        log.error(f"Falha ao analisar dados de culturas: {e}", exc_info=True)

    # 16. Processamento da Crop Machine
    context['crop_machine_analysis'] = None
    try:
        machine_data = crop_machine_service.analyze_crop_machine(main_farm_data)
        # A lógica de processamento foi movida para o crop_machine_service.
        # O serviço agora retorna os dados prontos para o template.
        if machine_data:
            context['crop_machine_analysis'] = machine_data.get("view")
            log.info(f"Análise da Crop Machine processada com sucesso para a fazenda #{farm_id}.")
    except Exception as e:
        log.error(f"Falha ao analisar dados da Crop Machine: {e}", exc_info=True)

    # 17. Processamento da Greenhouse (continua abaixo)
    context['greenhouse_analysis'] = None
    try:
        greenhouse_data = greenhouse_service.analyze_greenhouse_resources(main_farm_data)
        if greenhouse_data:
            context['greenhouse_analysis'] = greenhouse_data.get("view")
            # Adiciona o domínio de culturas ao contexto para que o template da estufa possa usá-lo
            context['crops_domain'] = crops_domain
            log.info(f"Análise da Greenhouse processada com sucesso para a fazenda #{farm_id}.")
    except Exception as e:
        log.error(f"Falha ao analisar dados da Greenhouse: {e}", exc_info=True)

    # 18. Processamento de Frutas e Flores (para o painel unificado)
    fruit_data, flower_data, beehive_data = None, None, None
    try:
        fruit_data = fruit_service.analyze_fruit_patches(main_farm_data)
    except Exception as e:
        log.error(f"Falha ao analisar dados de frutas: {e}", exc_info=True)
    
    try:
        flower_data = flower_service.analyze_flower_beds(main_farm_data)
    except Exception as e:
        log.error(f"Falha ao analisar dados de flores: {e}", exc_info=True)

    try:
        beehive_data = flower_service.analyze_beehives(main_farm_data)
    except Exception as e:
        log.error(f"Falha ao analisar dados de colmeias: {e}", exc_info=True)

    # NOVO: Processamento de Cogumelos (movido para o local correto)
    mushroom_data = None
    try:
        mushroom_data = mushrooms_service.analyze_mushroom_spawns(main_farm_data)
        if mushroom_data and mushroom_data.get("view"):
            mushroom_view = mushroom_data["view"]
            mushroom_resources = {
                "Cogumelos": {
                    "nodes": mushroom_view.get("mushroom_status", {}),
                    "summary": mushroom_view.get("summary", {})
                }
            }
            unified_analyses.append({
                "title": "Cogumelos",
                "resources": mushroom_resources
            })
    except Exception as e:
        log.error(f"Falha ao analisar dados de cogumelos: {e}", exc_info=True)

    if wood_data and wood_data.get("view"):
        wood_view = wood_data["view"]
        wood_resources = {
            "Wood": {
                "nodes": wood_view.get("tree_status", {}),
                "summary": wood_view.get("summary", {})
            }
        }
        unified_analyses.append({
            "title": "Madeira",
            "resources": wood_resources
        })
    if mining_data and mining_data.get("view"):
        mining_view = mining_data["view"]
        nodes_by_type = mining_view.get("nodes_by_type", {})
        summaries_by_type = mining_view.get("summary_by_type", {})
        mining_resources = {
            name: {"nodes": nodes, "summary": summaries_by_type.get(name, {})}
            for name, nodes in nodes_by_type.items()
        }
        unified_analyses.append({
            "title": "Mineração",
            "resources": dict(sorted(mining_resources.items()))
        })
    if crop_data and crop_data.get("view"):
        crop_view = crop_data["view"]
        plots_by_crop = defaultdict(dict)
        for plot_id, plot_info in crop_view.get("plot_status", {}).items():
            plots_by_crop[plot_info['crop_name']][plot_id] = plot_info
        
        summaries_by_crop = crop_view.get("summary_by_crop", {})
        crop_resources = {
            name: {"nodes": nodes, "summary": summaries_by_crop.get(name, {})}
            for name, nodes in plots_by_crop.items()
        }
        unified_analyses.append({
            "title": "Culturas",
            "resources": dict(sorted(crop_resources.items()))
        })
    if fruit_data and fruit_data.get("view"):
        fruit_view = fruit_data["view"]
        patches_by_fruit = defaultdict(dict)
        for patch_id, patch_info in fruit_view.get("patch_status", {}).items():
            patches_by_fruit[patch_info['fruit_name']][patch_id] = patch_info
        
        summaries_by_fruit = fruit_view.get("summary_by_fruit", {})
        fruit_resources = {
            name: {"nodes": nodes, "summary": summaries_by_fruit.get(name, {})}
            for name, nodes in patches_by_fruit.items()
        }
        unified_analyses.append({
            "title": "Frutas",
            "resources": dict(sorted(fruit_resources.items()))
        })
    if flower_data and flower_data.get("view"):
        flower_view = flower_data["view"]
        beds_by_flower = defaultdict(dict)
        for bed_id, bed_info in flower_view.get("beds", {}).items():
            beds_by_flower[bed_info['flower_name']][bed_id] = bed_info
        
        summaries_by_flower = flower_view.get("summary_by_flower", {})
        flower_resources = {
            name: {"nodes": nodes, "summary": summaries_by_flower.get(name, {})}
            for name, nodes in beds_by_flower.items()
        }
        unified_analyses.append({
            "title": "Flores",
            "resources": dict(sorted(flower_resources.items()))
        })

    context['unified_resource_analyses'] = unified_analyses

    # Processamento do Mapa da Fazenda
    context['layout_map'] = None
    try:
        # NOVO: Consolida todos os nós analisados em um único dicionário para o mapa.
        # Isso garante que o mapa use os dados calculados (rendimento, minas restantes, etc.)
        # em vez dos dados brutos da API.
        all_analyzed_nodes = {}
        if wood_data and wood_data.get("view"):
            for tree_id, tree_info in wood_data["view"].get("tree_status", {}).items():
                all_analyzed_nodes[f"trees-{tree_id}"] = tree_info
        
        if mining_data and mining_data.get("view"):
            for resource_name, nodes in mining_data["view"].get("nodes_by_type", {}).items():
                api_key = next((key for key, info in mining_service.RESOURCE_NODE_MAP.items() if info["name"] == resource_name), None)
                if api_key:
                    for node_id, node_info in nodes.items():
                        all_analyzed_nodes[f"{api_key}-{node_id}"] = node_info

        if crop_data and crop_data.get("view"):
            for plot_id, plot_info in crop_data["view"].get("plot_status", {}).items():
                all_analyzed_nodes[f"crops-{plot_id}"] = plot_info

        if fruit_data and fruit_data.get("view"):
            for patch_id, patch_info in fruit_data["view"].get("patch_status", {}).items():
                all_analyzed_nodes[f"fruitPatches-{patch_id}"] = patch_info

        if flower_data and flower_data.get("view"):
            for bed_id, bed_info in flower_data["view"].get("beds", {}).items():
                all_analyzed_nodes[f"flowerBeds-{bed_id}"] = bed_info
        
        if mushroom_data and mushroom_data.get("view"):
            for mushroom_id, mushroom_info in mushroom_data["view"].get("mushroom_status", {}).items():
                all_analyzed_nodes[f"mushrooms-{mushroom_id}"] = mushroom_info

        # NOVO: Adiciona os dados da Crop Machine e Greenhouse aos nós analisados.
        # CORREÇÃO: A chave para edifícios deve ser construída usando o ID único do
        # edifício dos dados do jogo, em vez de um índice fixo como '0'.
        # Isso garante que o farm_layout_service possa associar os dados de análise
        # ao edifício correto no mapa.
        if context.get('crop_machine_analysis'):
            crop_machine_buildings = main_farm_data.get("buildings", {}).get("Crop Machine", [])
            if crop_machine_buildings:
                machine_id = crop_machine_buildings[0].get("id")
                all_analyzed_nodes[f"Crop Machine-{machine_id}"] = context['crop_machine_analysis']
        
        if context.get('greenhouse_analysis'):
            greenhouse_buildings = main_farm_data.get("buildings", {}).get("Greenhouse", [])
            if greenhouse_buildings:
                greenhouse_id = greenhouse_buildings[0].get("id")
                all_analyzed_nodes[f"Greenhouse-{greenhouse_id}"] = context['greenhouse_analysis']

        if beehive_data and beehive_data.get("view"):
            for hive_id, hive_info in beehive_data["view"].get("hives", {}).items():
                # ADICIONADO: Garante que o nome do recurso seja 'Honey' para a busca de preços.
                hive_info['resource_name'] = 'Honey'
                all_analyzed_nodes[f"beehives-{hive_id}"] = hive_info

        layout_map_data = farm_layout_service.generate_layout_map(main_farm_data, all_analyzed_nodes)
        if layout_map_data:
            context['layout_map'] = layout_map_data
            log.info(f"Mapa da fazenda gerado com sucesso para a fazenda #{farm_id}.")
        else:
            log.warning(f"Não foi possível gerar o mapa da fazenda para a fazenda #{farm_id}.")
    except Exception as e:
        log.error(f"Falha ao gerar o mapa da fazenda: {e}", exc_info=True)

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

        goal_data = expansion_service.calculate_total_requirements(
            current_land_type=current_land_type,
            current_level=effective_start_level, # Usa o nível efetivo
            goal_land_type=goal_land_type,
            goal_level=goal_level
        )

        if not goal_data or "requirements" not in goal_data:
             return jsonify({"requirements": None, "goal_level_display": goal_level})
        
        unlocks_data = expansion_service.calculate_total_gains(
            start_land_type=current_land_type,
            start_level=effective_start_level,
            goal_land_type=goal_land_type,
            goal_level=goal_level
        )

        # O resto da função permanece igual, pois já está a funcionar corretamente.
        inventory = main_farm_data.get('inventory', {})
        sfl_balance = Decimal(main_farm_data.get('balance', '0'))
        coins_balance = Decimal(main_farm_data.get('coins', '0'))
        item_prices = prices_data.get("data", {}).get("p2p", {})
        
        processed_reqs = []
        total_sfl_cost = Decimal('0')
        total_relative_sfl_cost = Decimal('0')

        for item, needed_total_dec in goal_data["requirements"].items():
            needed_total = Decimal(str(needed_total_dec))
            have = sfl_balance if item == "SFL" else (coins_balance if item == "Coins" else Decimal(inventory.get(item, '0')))
            shortfall = max(needed_total - have, Decimal('0'))
            
            price = Decimal(str(item_prices.get(item, '0')))
            
            value_of_needed = needed_total * price
            value_of_shortfall = shortfall * price
            
            total_sfl_cost += value_of_needed          # Acumula o custo total
            total_relative_sfl_cost += value_of_shortfall # Acumula o custo relativo

            # Define qual valor mostrar no item: o relativo se faltar, ou o total se completo
            sfl_value = value_of_shortfall if shortfall > 0 else value_of_needed

            processed_reqs.append({
                "name": item,
                "shortfall": f"{shortfall:.2f}",
                "needed": f"{needed_total:.2f}",
                "value_of_needed": f"{value_of_needed:.2f}",
                "sfl_value": f"{sfl_value:.2f}",
                "icon": analysis.get_item_image_path(item)
            })

        response_data = {
            "goal_level_display": goal_level, "goal_land_type": goal_land_type,
            "max_bumpkin_level": goal_data["max_bumpkin_level"],
            "total_time_str": goal_data["total_time_str"],
            "total_sfl_cost": f"{total_sfl_cost:.2f}",
            "total_relative_sfl_cost": f"{total_relative_sfl_cost:.2f}",
            "requirements": processed_reqs,
            "unlocks": unlocks_data
        }
        return jsonify(response_data)

    except (IndexError, ValueError):
        return jsonify({"error": "Formato de 'goal_level' inválido."}), 400
    except Exception as e:
        log.error("Erro inesperado no endpoint da API de metas para a fazenda %s: %s", farm_id, e, exc_info=True)
        return jsonify({"error": "Um erro inesperado ocorreu."}), 500

@bp.route('/api/farm/<int:farm_id>/treasure_dig_update')
def api_treasure_dig_update(farm_id):
    """
    Endpoint da API para atualizar os dados do painel de escavação de tesouros.
    """
    try:
        # 1. Limpa o cache para forçar a busca de novos dados
        cache.delete(f"farm_data_{farm_id}")
        cache.delete(f"sfl_world_{farm_id}_land") # Limpa também o cache da API secundária
        log.info(f"Cache para a fazenda #{farm_id} foi limpo para atualização.")

        # 2. Busca os dados mais recentes
        main_farm_data, _, api_error = sunflower_api.get_farm_data(farm_id)
        if api_error or not main_farm_data:
            return jsonify({"error": f"Não foi possível buscar dados atualizados: {api_error}"}), 500

        # 3. Analisa os dados de escavação
        # CORREÇÃO: Obter o 'seasonal_artefact' do estado global do jogo.
        seasonal_artefact = GAME_STATE.get('current_artefact_name')
        if not seasonal_artefact:
            current_app.logger.error("Artefato sazonal não encontrado no GAME_STATE. O estado do jogo pode não ter sido carregado.")
            return jsonify({'success': False, 'error': 'Erro interno: Estado do jogo não inicializado.'}), 500

        # Passar o argumento necessário para a função de análise.
        treasure_dig_info = treasure_dig_service.analyze_desert_digging_data(main_farm_data, seasonal_artefact)

        # 4. Renderiza apenas o painel parcial com os novos dados
        updated_html = render_template(
            'partials/_treasuredig_panel.html',
            treasure_dig_info=treasure_dig_info,
            farm_id=farm_id, # Passa o farm_id para que o botão continue a funcionar
            get_item_image_path=analysis.get_item_image_path,
            enumerate=enumerate
        )

        return jsonify({"success": True, "html": updated_html})

    except Exception as e:
        log.error(f"Erro inesperado ao atualizar dados de escavação para a fazenda {farm_id}: {e}", exc_info=True)
        return jsonify({"error": "Um erro inesperado ocorreu no servidor."}), 500

@bp.route('/farm/<int:farm_id>/wip')
def wip_dashboard(farm_id):
    """
    Exibe uma página de trabalho em progresso (WIP) com a análise de sumário de recursos.
    """
    log.info(f"Iniciando a montagem do painel WIP para a fazenda #{farm_id}")

    # Busca os dados da fazenda
    main_farm_data, secondary_farm_data, api_error = sunflower_api.get_farm_data(farm_id)

    if api_error:
        return render_template('wip.html', error=api_error, farm_id=farm_id)

    if not main_farm_data:
        return render_template('wip.html', error="Não foi possível obter os dados principais da fazenda.", farm_id=farm_id)

    # Adiciona dados secundários, se disponíveis
    if secondary_farm_data:
        if 'bumpkin' not in main_farm_data:
            main_farm_data['bumpkin'] = {}
        main_farm_data['bumpkin']['level'] = secondary_farm_data.get('bumpkin', {}).get('level', 0)
        main_farm_data['land_level'] = secondary_farm_data.get('land', {}).get('level', 0)

    # Executa a análise de sumário
    summary_data = summary_service.analyze_resources_summary(main_farm_data)

    # Renderiza a página WIP com os dados do sumário
    return render_template('wip.html', farm_id=farm_id, summary_data=summary_data, username=main_farm_data.get('username', f"Fazenda #{farm_id}"))
