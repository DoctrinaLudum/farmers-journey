import json
import logging
from collections import defaultdict
from decimal import Decimal

from .. import analysis
from ..domain import treasure_dig as treasure_domain
from ..services import pricing_service
from ..services import resource_analysis_service

log = logging.getLogger(__name__)

def _get_digging_history_stats(bumpkin_data: dict) -> dict:
    """
    Analyzes bumpkin activity to find total dug items and the most frequent one.

    Args:
        bumpkin_data: The 'bumpkin' section of the farm data.

    Returns:
        A dictionary containing total_items_dug and most_dug_item.
    """
    dug_item_counts = defaultdict(int)
    activity = bumpkin_data.get('activity', {})
    previous_activity = bumpkin_data.get('previousActivity', {})
    
    # Keys to ignore as they are general counters, not specific items.
    IGNORE_KEYS = {"Treasure Dug"}

    # Combine both activity logs for a complete history
    for item, count in list(activity.items()) + list(previous_activity.items()):
        if item.endswith(' Dug') and item not in IGNORE_KEYS:
            item_name = item.removesuffix(' Dug')
            dug_item_counts[item_name] += count

    total_items_dug = sum(dug_item_counts.values())
    most_dug_item = None

    if dug_item_counts:
        most_dug_item_name = max(dug_item_counts, key=dug_item_counts.get)
        most_dug_item = {
            'name': most_dug_item_name,
            'amount': dug_item_counts[most_dug_item_name],
            'image': analysis.get_item_image_path(most_dug_item_name)
        }

    return {
        'total_items_dug': total_items_dug,
        'most_dug_item': most_dug_item
    }

def analyze_desert_digging_data(main_farm_data: dict, seasonal_artefact: str) -> dict:
    """
    Analisa todos os dados de escavação de tesouros da Ilha do Deserto.

    Args:
        main_farm_data: O dicionário principal de dados da fazenda vindo da API.
        seasonal_artefact: O nome do artefato sazonal atual, vindo do estado global.

    Returns:
         Um dicionário contendo o espelho do grid, estatísticas e padrões.
        Retorna uma estrutura vazia se os dados não forem encontrados.
    """
    default_structure = {
        'grid_mirror': [],
        'stats': {
            'total_digs': 0,
            'items_found': {},
            'tool_usage': {},
            'streak': {}
        },
        'patterns': {
            'current': [],
            'completed': []
        },
        'hints': []
    }

    # 1. Acesso seguro aos dados
    digging_data = main_farm_data.get('desert', {}).get('digging', {})
    if not digging_data:
        log.warning("Chave 'desert' ou 'digging' não encontrada nos dados da fazenda.")
        return default_structure

    # 2. Processamento do Grid e Estatísticas
    grid_mirror = [[None for _ in range(10)] for _ in range(10)]
    items_found_counts = defaultdict(int)
    tool_usage = defaultdict(int)
    total_digs = 0

    grid_entries = digging_data.get('grid', [])
    all_digs = []
    # A API pode retornar uma lista mista de escavações. Esta lógica normaliza
    # os dados para análise e conta o uso de ferramentas corretamente.
    for entry in grid_entries:
        if isinstance(entry, list):
            # Sand Drill: uma lista de escavações conta como um único uso de ferramenta.
            if entry:
                tool_name = entry[0].get('tool', 'Sand Drill')
                tool_usage[tool_name] += 1
            all_digs.extend(entry)
        elif isinstance(entry, dict):
            # Sand Shovel: um dicionário de escavação conta como um uso.
            tool_name = entry.get('tool', 'Unknown Tool')
            tool_usage[tool_name] += 1
            all_digs.append(entry)

    for dig_entry in all_digs:
        if not isinstance(dig_entry, dict):
            log.warning(f"Item de escavação ignorado por não ser um dicionário: {dig_entry}")
            continue

        total_digs += 1
        x = dig_entry.get('x')
        y = dig_entry.get('y')
        items = dig_entry.get('items', {})

        # Pega o primeiro (e geralmente único) item encontrado no buraco
        item_name = next(iter(items), "Unknown")
        item_count = items.get(item_name, 0)
        items_found_counts[item_name] += item_count

        if x is not None and y is not None and 0 <= x < 10 and 0 <= y < 10:
            grid_mirror[y][x] = {
                'item_name': item_name,
                'image': analysis.get_item_image_path(item_name)
            }

    # Obter itens do jogador para análise de buffs
    player_items = resource_analysis_service._get_player_items(main_farm_data)

    # Processa os valores de SFL e Moedas para itens encontrados e ferramentas usadas
    processed_items_found = []
    total_sfl_value = Decimal("0")
    total_coins_value = Decimal("0")

    # Obter buffs de preço de venda de tesouros
    sale_price_boost_catalogue = resource_analysis_service.filter_boosts_from_domains(
        {"boost_category_names": ["Treasure"]}
    )
    active_sale_price_boosts = resource_analysis_service.get_active_player_boosts(
        player_items,
        sale_price_boost_catalogue,
        farm_data=main_farm_data
    )
    log.debug(f"Active Sale Price Boosts: {active_sale_price_boosts}")

    for item_name, count in sorted(items_found_counts.items()):
        prices = pricing_service.get_item_prices(item_name)
        sfl_price_base = Decimal(str(prices.get('sfl', 0)))
        coin_price_base = Decimal(str(prices.get('coins', 0)))

        item_specific_boosts = []
        item_sale_price_multiplier = Decimal('1')

        for boost in active_sale_price_boosts:
            if boost.get("type") == "SALE_PRICE" and boost.get("operation") == "percentage":
                conditions = boost.get("conditions", {})
                if conditions.get("category") == "TREASURE_SALE":
                    boost_value = Decimal(str(boost["value"]))
                    item_sale_price_multiplier += boost_value
                    
                    individual_bonus_value = coin_price_base * boost_value * Decimal(count)
                    
                    item_specific_boosts.append({
                        "name": boost.get("source_item"),
                        "type": "SALE_PRICE",
                        "value": float(boost_value),
                        "bonus_coin_value": int(individual_bonus_value) if individual_bonus_value > 0 else None
                    })

        final_sfl_price = sfl_price_base * item_sale_price_multiplier
        final_coin_price = coin_price_base * item_sale_price_multiplier

        item_sfl_value = final_sfl_price * Decimal(count)
        item_coin_value = final_coin_price * Decimal(count)

        total_item_bonus_coins = (final_coin_price - coin_price_base) * Decimal(count)

        total_sfl_value += item_sfl_value
        total_coins_value += item_coin_value
        processed_items_found.append({
            'name': item_name, 'amount': count,
            'sfl_value': float(item_sfl_value) if item_sfl_value > 0 else None,
            'coin_value': int(item_coin_value) if item_coin_value > 0 else None,
            'boosts': item_specific_boosts if item_specific_boosts else None,
            'bonus_coin_value': int(total_item_bonus_coins) if total_item_bonus_coins > 0 else None
        })

    processed_tool_usage = []
    total_sfl_cost = Decimal("0")
    total_coins_cost = Decimal("0")
    for tool_name, count in sorted(tool_usage.items()):
        prices = pricing_service.get_item_prices(tool_name)
        sfl_price = Decimal(str(prices.get('sfl', 0)))
        coin_price = Decimal(str(prices.get('coins', 0)))
        item_sfl_cost = sfl_price * Decimal(count)
        item_coin_cost = coin_price * Decimal(count)
        total_sfl_cost += item_sfl_cost
        total_coins_cost += item_coin_cost
        processed_tool_usage.append({
            'name': tool_name, 'amount': count,
            'sfl_cost': float(item_sfl_cost) if item_sfl_cost > 0 else None,
            'coin_cost': int(item_coin_cost) if item_coin_cost > 0 else None,
        })

    # 3. Processamento dos Padrões de Tesouro (Objetivos)
    def _process_patterns(pattern_list):
        processed = []
        for pattern_name in pattern_list:
            # Caminho da imagem estática (usado para padrões completos)
            filename = f"{pattern_name.lower()}.png"
            image_path = f"static/assets/desert/patterns/{filename}"

            # --- LÓGICA ATUALIZADA PARA USAR DIGGING_FORMATIONS ---
            pattern_formation = treasure_domain.DIGGING_FORMATIONS.get(pattern_name)
            grid_data = {'mini_grid': None}

            if pattern_formation:
                TARGET_GRID_SIZE = 4
                mini_grid = [[None for _ in range(TARGET_GRID_SIZE)] for _ in range(TARGET_GRID_SIZE)]

                # Extrai coordenadas e resolve o nome do item "SEASONAL"
                items_with_coords = []
                for item_data in pattern_formation:
                    name = "SEASONAL" if item_data['name'] == "SEASONAL" else item_data['name']
                    if name == "SEASONAL":
                        name = seasonal_artefact
                    items_with_coords.append({'name': name, 'x': item_data['x'], 'y': item_data['y']})
                
                if items_with_coords:
                    coords = [(item['x'], item['y']) for item in items_with_coords]
                    min_x = min(c[0] for c in coords)
                    max_x = max(c[0] for c in coords)
                    min_y = min(c[1] for c in coords)
                    max_y = max(c[1] for c in coords)
                    pattern_width = max_x - min_x + 1
                    pattern_height = max_y - min_y + 1
                    offset_x = (TARGET_GRID_SIZE - pattern_width) // 2
                    offset_y = (TARGET_GRID_SIZE - pattern_height) // 2

                    # Preenche o mini-grid com os dados dos itens
                    for item in items_with_coords:
                        cx = item['x'] - min_x + offset_x
                        cy = item['y'] - min_y + offset_y
                        if 0 <= cx < TARGET_GRID_SIZE and 0 <= cy < TARGET_GRID_SIZE:
                            mini_grid[cy][cx] = {'item_name': item['name'], 'image': analysis.get_item_image_path(item['name'])}
                    
                    grid_data['mini_grid'] = mini_grid


            processed.append({
                'name': pattern_name.replace("_", " ").title(),
                'image': image_path,
                'grid_data': grid_data
            })
        return processed

    current_patterns = _process_patterns(digging_data.get('patterns', []))
    completed_patterns = _process_patterns(digging_data.get('completedPatterns', []))

    # Get a set of names for completed patterns for quick lookup
    completed_pattern_names = {p['name'] for p in completed_patterns}

    # Add completion status to current patterns
    for p in current_patterns:
        p['is_completed'] = p['name'] in completed_pattern_names

    # Calculate profit/loss
    total_sfl_profit = total_sfl_value - total_sfl_cost
    total_coins_profit = total_coins_value - total_coins_cost

    activity = main_farm_data.get('bumpkin', {}).get('activity', {})
    sand_shovels_crafted = activity.get('Sand Shovel Crafted', 0)
    sand_drills_crafted = activity.get('Sand Drill Crafted', 0)
    digging_history = _get_digging_history_stats(main_farm_data.get('bumpkin', {}))

    # 4. Geração de Dicas Preditivas (Lógica de Encaixe Orientado por Peças Refatorada)
    pattern_location_hints = []
    MIN_DIGS_FOR_HINTS = 5

    # A. A função só gera dicas se um número mínimo de escavações foi feito.
    if total_digs >= MIN_DIGS_FOR_HINTS:
        dug_items_map = {(x, y): cell['item_name'] for y, row in enumerate(grid_mirror) for x, cell in enumerate(row) if cell}

        # B. Setup das regras e âncoras
        NON_TREASURE_ITEMS = {"Sand", "Crab"}

        forbidden_coords = set()
        for (x, y), item_name in dug_items_map.items():
            if item_name == "Sand":
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    forbidden_coords.add((x + dx, y + dy))

        crab_locations = [pos for pos, name in dug_items_map.items() if name == "Crab"]
        treasure_anchors = [(pos, name) for pos, name in dug_items_map.items() if name not in NON_TREASURE_ITEMS]

        # C. Lógica Principal de Encaixe (só executa se houver âncoras de tesouro)
        if treasure_anchors:
            uncompleted_patterns = [p for p in current_patterns if not p.get('is_completed')]

            for pattern in uncompleted_patterns:
                pattern_name_key = pattern['name'].upper().replace(" ", "_")
                formation = treasure_domain.DIGGING_FORMATIONS.get(pattern_name_key)
                if not formation: continue

                pattern_items = [{'name': (seasonal_artefact if item['name'] == "SEASONAL" else item['name']), 'x': item['x'], 'y': item['y']} for item in formation]
                if not pattern_items: continue

                min_px, min_py = min(p['x'] for p in pattern_items), min(p['y'] for p in pattern_items)
                normalized_pattern = [{'name': p['name'], 'x': p['x'] - min_px, 'y': p['y'] - min_py} for p in pattern_items]

                possible_locations = []
                tested_placements = set()

                # Itera sobre cada tesouro já encontrado como um ponto de partida ("âncora")
                for (anchor_gx, anchor_gy), dug_item_name in treasure_anchors:
                    # Para cada âncora, tenta encaixar cada peça do padrão que seja do mesmo tipo
                    for p_item in normalized_pattern:
                        if p_item['name'] == dug_item_name:
                            hypothetical_anchor_x = anchor_gx - p_item['x']
                            hypothetical_anchor_y = anchor_gy - p_item['y']

                            placement_key = (hypothetical_anchor_x, hypothetical_anchor_y)
                            if placement_key in tested_placements: continue
                            tested_placements.add(placement_key)

                            matches, conflicts, is_possible = 0, 0, True
                            hypothetical_placements = {}

                            # Valida a posição hipotética inteira
                            for p_validate_item in normalized_pattern:
                                gx, gy = hypothetical_anchor_x + p_validate_item['x'], hypothetical_anchor_y + p_validate_item['y']
                                hypothetical_placements[(gx, gy)] = p_validate_item['name']

                                if not (0 <= gx < 10 and 0 <= gy < 10): is_possible = False; break
                                if p_validate_item['name'] not in NON_TREASURE_ITEMS and (gx, gy) in forbidden_coords:
                                    conflicts += 1; break
                                if (gx, gy) in dug_items_map:
                                    if dug_items_map[(gx, gy)] == p_validate_item['name']: matches += 1
                                    else: conflicts += 1; break

                            if not is_possible or conflicts > 0: continue

                            # Validação da Regra do Caranguejo (como Bônus de Pontuação)
                            crab_bonus_score = 0
                            for cx, cy in crab_locations:
                                crab_is_satisfied = False
                                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                                    nx, ny = cx + dx, cy + dy
                                    if ((nx, ny) in dug_items_map and dug_items_map[(nx, ny)] not in NON_TREASURE_ITEMS) or \
                                       ((nx, ny) in hypothetical_placements and hypothetical_placements[(nx, ny)] not in NON_TREASURE_ITEMS):
                                        crab_is_satisfied = True
                                        break
                                if crab_is_satisfied:
                                    crab_bonus_score += 1

                            # A pontuação final dá um peso maior para correspondências diretas
                            # e um bônus menor para a conformidade com as regras.
                            score = (matches * 10) + crab_bonus_score
                            undug_cells = [f"(X:{hypothetical_anchor_x + p['x']}, Y:{hypothetical_anchor_y + p['y']})" for p in normalized_pattern if (hypothetical_anchor_x + p['x'], hypothetical_anchor_y + p['y']) not in dug_items_map]
                            if undug_cells:
                                anchor_str = f"(X:{hypothetical_anchor_x}, Y:{hypothetical_anchor_y})"
                                all_pattern_coords = [(hypothetical_anchor_x + p['x'], hypothetical_anchor_y + p['y']) for p in normalized_pattern]
                                possible_locations.append({'anchor': anchor_str, 'matches': matches, 'undug_cells': undug_cells, 'highlight_coords': all_pattern_coords, 'score': score})
                
                # Ordena as localizações pela pontuação e formata as dicas
                if possible_locations:
                    sorted_locations = sorted(possible_locations, key=lambda x: x['score'], reverse=True)
                    hints_for_this_pattern = []
                    for loc in sorted_locations[:5]:
                        hints_for_this_pattern.append({
                            'text': f"Pode estar em {loc['anchor']}. Células a cavar: {', '.join(loc['undug_cells'])}.",
                            'highlight_coords': json.dumps(loc['highlight_coords'])
                        })
                    
                    if hints_for_this_pattern:
                        pattern_location_hints.append({
                            'pattern_name': pattern['name'],
                            'possible_locations': hints_for_this_pattern
                        })
        
        # D. Preparar dados para a máscara de regras
        rules_mask_data = {
            'sand_blocks': [list(coords) for coords in forbidden_coords],
            'crab_hints': []
        }
        crab_hints_set = set()
        for (cx, cy) in crab_locations:
            # Para cada caranguejo, adicione todas as 4 células adjacentes
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = cx + dx, cy + dy
                # Verifica se a célula adjacente está dentro dos limites do grid
                # e se não é um bloco de areia (já que areia não pode ter tesouros)
                if 0 <= nx < 10 and 0 <= ny < 10 and (nx, ny) not in forbidden_coords:
                    crab_hints_set.add((nx, ny))
        rules_mask_data['crab_hints'] = [list(coords) for coords in crab_hints_set]

        # 5. Montagem do resultado final com dicas e dados da máscara
        return {
            'grid_mirror': grid_mirror, 
            'stats': {
                'total_digs': total_digs, 'items_found': processed_items_found, 'tool_usage': processed_tool_usage,
                'streak': digging_data.get('streak', {}),
                'total_sfl_value': float(total_sfl_value), 'total_coins_value': int(total_coins_value),
                'total_sfl_cost': float(total_sfl_cost), 'total_coins_cost': int(total_coins_cost),
                'total_sfl_profit': float(total_sfl_profit),
                'total_coins_profit': int(total_coins_profit),
                'sand_shovels_crafted': sand_shovels_crafted,
                'sand_drills_crafted': sand_drills_crafted,
                **digging_history
            },
            'patterns': { 'current': current_patterns, 'completed': completed_patterns },
            'hints': pattern_location_hints,
            'rules_mask_data': rules_mask_data
        }

    # Se a função chega aqui, significa que total_digs < MIN_DIGS_FOR_HINTS.
    # Retorna a estrutura de dados padrão.
    return {
        'grid_mirror': grid_mirror,
        'stats': {
            'total_digs': total_digs,
            'items_found': processed_items_found,
            'tool_usage': processed_tool_usage,
            'streak': digging_data.get('streak', {}),
            'total_sfl_value': float(total_sfl_value),
            'total_coins_value': int(total_coins_value),
            'total_sfl_cost': float(total_sfl_cost), 'total_coins_cost': int(total_coins_cost),
            'total_sfl_profit': float(total_sfl_profit),
            'total_coins_profit': int(total_coins_profit),
            'sand_shovels_crafted': sand_shovels_crafted,
            'sand_drills_crafted': sand_drills_crafted,
            **digging_history
        },
        'patterns': { 'current': current_patterns, 'completed': completed_patterns },
        'hints': [],
        'rules_mask_data': {'sand_blocks': [], 'crab_hints': []}
    }