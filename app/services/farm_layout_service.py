# app/services/farm_layout_service.py

import hashlib
import logging
import json
import re
from collections import defaultdict
from decimal import Decimal

from ..analysis import get_item_image_path
from ..domain import collectiblesItemBuffs as collectibles_domain
from ..domain import dimensions as dimensions_domain
from ..domain import skills as skills_domain

log = logging.getLogger(__name__)

# Mapeia chaves da API para um nome de tipo de nó mais limpo
API_KEY_TO_NODE_TYPE = {
    "trees": "Tree", "crops": "Crop Plot", "stones": "Stone Rock",
    "iron": "Iron Rock", "gold": "Gold Rock", "crimstones": "Crimstone Rock",
    "sunstones": "Sunstone Rock", "fruitPatches": "Fruit Patch", "mushrooms": "Mushroom",
    "flowerBeds": "Flower Bed", "beehives": "Beehive",
    "oilReserves": "Oil Reserve", "lavaPits": "Lava Pit",
    "Crop Machine": "Building", "Greenhouse": "Building",
}

# Mapeia o tipo de nó para o nome do recurso que ele produz, para o ícone.
NODE_TYPE_TO_RESOURCE_ICON_NAME = {
    "Tree": "Wood", "Stone Rock": "Stone", "Iron Rock": "Iron",
    "Gold Rock": "Gold", "Crimstone Rock": "Crimstone",
    "Sunstone Rock": "Sunstone", "Oil Reserve": "Oil",
    "Beehive": "Honey", "Lava Pit": "Obsidian",
}

def get_hsl_color_from_string(text: str) -> tuple[int, int, int]:
    hash_object = hashlib.md5(text.encode())
    hash_hex = hash_object.hexdigest()
    hue = int(hash_hex[:6], 16) % 360
    saturation = 75
    lightness = 60
    return (hue, saturation, lightness)

def _get_item_dimensions(item_name: str) -> dict:
    return dimensions_domain.PLACEABLE_DIMENSIONS.get(item_name, {"width": 1, "height": 1})

def _create_dynamic_legend(grid_data: dict) -> dict:
    dynamic_map_legend_icons = {}
    icons_to_find = {'bonus_reward', 'has_yield_fertiliser', 'beeSwarm'}
    for cell in grid_data.values():
        if not icons_to_find: break
        if not cell.get("resource"): continue
        details = cell["resource"].get('details', {})
        if 'bonus_reward' in icons_to_find and details.get('bonus_reward'):
            dynamic_map_legend_icons['bonus_reward'] = {
                'icon_type': 'bi', 'icon_class': 'bi-gift-fill text-primary', 'text': 'Recompensa Extra'
            }
            icons_to_find.remove('bonus_reward')
        if 'has_yield_fertiliser' in icons_to_find and details.get('has_yield_fertiliser'):
            dynamic_map_legend_icons['has_yield_fertiliser'] = {
                'icon_type': 'img', 'src': get_item_image_path('Yield Fertiliser'), 'text': 'Fertilizante'
            }
            icons_to_find.remove('has_yield_fertiliser')
        if 'beeSwarm' in icons_to_find and details.get('beeSwarm'):
            dynamic_map_legend_icons['beeSwarm'] = {
                'icon_type': 'img', 'src': get_item_image_path('Bee Swarm'), 'text': 'Enxame de Abelhas'
            }
            icons_to_find.remove('beeSwarm')
    return dynamic_map_legend_icons

def generate_layout_map(farm_data: dict, analyzed_nodes: dict = None):
    analyzed_nodes = analyzed_nodes or {}
    grid = defaultdict(lambda: {"resource": None, "aoe_source": None, "aoe_items": []})
    overlay_items = []
    all_coords = []
    legend_item_names = set()
    crops_in_machine_list = []
    player_skills = set(farm_data.get("bumpkin", {}).get("skills", {}).keys())

    resource_sources = [
        "trees", "crops", "stones", "iron", "gold", "crimstones", "sunstones",
        "fruitPatches", "flowerBeds", "beehives", "oilReserves", "lavaPits", "mushrooms",
        "Crop Machine", "Greenhouse"
    ]

    for source_key in resource_sources:
        if source_key == "flowerBeds":
            items = farm_data.get("flowers", {}).get(source_key, {})
        elif source_key == "mushrooms":
            items = farm_data.get("mushrooms", {}).get("mushrooms", {})
        elif source_key in ["Crop Machine", "Greenhouse"]:
            items = {p['id']: p for p in farm_data.get("buildings", {}).get(source_key, [])}
        else:
            items = farm_data.get(source_key, {})
        
        node_type = API_KEY_TO_NODE_TYPE.get(source_key)
        if not node_type: continue
        
        for item_id, item_data in items.items():
            lookup_key = f"{source_key}-{item_id}"
            analyzed_data = analyzed_nodes.get(lookup_key, {})

            if (source_key == "mushrooms" and not analyzed_data.get("name")) or \
               (source_key == "crops" and not analyzed_data.get("crop_name")) or \
               (source_key == "fruitPatches" and not analyzed_data.get("fruit_name")) or \
               (source_key == "flowerBeds" and not analyzed_data.get("flower_name")):
                continue

            coords = item_data.get("coordinates") or {"x": item_data.get("x"), "y": item_data.get("y")}
            if not (coords and coords.get("x") is not None): continue
            
            x, y = coords["x"], coords["y"]
            all_coords.append((x, y))
            
            item_name_for_dim = source_key
            dimensions = _get_item_dimensions(item_name_for_dim)
            width, height = dimensions['width'], dimensions['height']
            is_large_building = source_key in ["Crop Machine", "Greenhouse"]

            icon_name, base_building_icon, overlay_icon = None, None, None
            
            if source_key == "Greenhouse":
                icon_name = "Greenhouse"
                base_building_icon = get_item_image_path("Greenhouse")

                if analyzed_data:
                    unique_plants = sorted(list(set(p.get("plant_name") for p in analyzed_data.get("pots", {}).values() if p.get("plant_name"))))
                    analyzed_data['growing_plants'] = unique_plants

                    if unique_plants:
                        legend_item_names.update(unique_plants)
                        # NOVO: Passa uma lista de ícones para o frontend para exibir múltiplos overlays.
                        analyzed_data['overlay_icons'] = [get_item_image_path(plant) for plant in unique_plants]

                    if not unique_plants: 
                        analyzed_data['resource_name'] = "Estufa (Vazia)"
                    elif len(unique_plants) == 1: analyzed_data['resource_name'] = f"Estufa ({unique_plants[0]})"
                    else: analyzed_data['resource_name'] = f"Estufa ({len(unique_plants)} plantas diferentes)"

            elif source_key == "Crop Machine":
                icon_name = "Crop Machine"
                base_building_icon = get_item_image_path(source_key)

                if analyzed_data and analyzed_data.get("queue") and analyzed_data["queue"]:
                    # Get unique crop names from the queue
                    crops_in_queue = sorted(list(set(item.get("crop") for item in analyzed_data["queue"] if item.get("crop"))))
                    crops_in_machine_list.extend(crops_in_queue)
                    # Rename to 'growing_plants' to match Greenhouse data structure for the frontend
                    analyzed_data['growing_plants'] = crops_in_queue
                    
                    if crops_in_queue:
                        # Add the names of the crops in the queue to the legend
                        legend_item_names.update(crops_in_queue)
                        # Create a list of overlay icons, just like the Greenhouse
                        analyzed_data['overlay_icons'] = [get_item_image_path(crop) for crop in crops_in_queue]
                        analyzed_data['resource_name'] = f"Crop Machine ({', '.join(crops_in_queue)})"
                else:
                    analyzed_data['resource_name'] = "Crop Machine (Vazia)"
            else:
                if node_type == "Crop Plot": icon_name = analyzed_data.get("crop_name")
                elif node_type == "Fruit Patch": icon_name = analyzed_data.get("fruit_name")
                elif node_type == "Flower Bed": icon_name = analyzed_data.get("flower_name")
                elif node_type == "Mushroom":
                    icon_name = analyzed_data.get("name")
                else: icon_name = NODE_TYPE_TO_RESOURCE_ICON_NAME.get(node_type, node_type)
                if icon_name: legend_item_names.add(icon_name)

            if not icon_name: continue

            icon_path = get_item_image_path(icon_name)
            filter_id = re.sub(r'[^a-z0-9]+', '-', icon_name.lower()).strip('-')
            
            if analyzed_data:
                analyzed_data.update({'filter_id': filter_id, 'position': {'x': x, 'y': y}})
                if 'resource_name' not in analyzed_data or not analyzed_data['resource_name']: analyzed_data['resource_name'] = icon_name
                # CORREÇÃO: Garante que o 'icon_path' da análise (usado para overlay) não seja
                # sobrescrito se já foi definido (pela Crop Machine ou Greenhouse).
                # Para outros recursos, define-o como o ícone principal.
                if 'icon_path' not in analyzed_data:
                    analyzed_data['icon_path'] = icon_path

            details = {"id": item_id}
            # CORREÇÃO DO ERRO 1: 'none' trocado por 'None'
            if node_type == "Mushroom" and 'total_amount' in analyzed_data:
                details['amount'] = "%.2f" % analyzed_data['total_amount']
            elif analyzed_data.get('calculations', {}).get('yield', {}).get('final_deterministic') is not None:
                details['amount'] = "%.2f" % analyzed_data['calculations']['yield']['final_deterministic']
            details.update({k: v for k, v in analyzed_data.items() if k in ['mines_left', 'harvests_left', 'bonus_reward'] and v is not None})
            if analyzed_data.get('has_yield_fertiliser'):
                details.update({'has_yield_fertiliser': True, 'yield_fertiliser_icon': get_item_image_path('Yield Fertiliser')})
            if analyzed_data.get('beeSwarm'):
                details.update({'beeSwarm': True, 'bee_swarm_icon': get_item_image_path('Bee Swarm')})

            resource_payload = {
                "type": source_key, "icon": icon_path, "details": details, "analysis": analyzed_data,
                "filter_id": filter_id, "base_building_icon": base_building_icon, 
                "x": x, "y": y, "width": width, "height": height
            }

            # Adiciona os filtros de plantas específicos da estufa ao payload
            if source_key == "Greenhouse" and analyzed_data and 'growing_plants' in analyzed_data:
                plant_names = analyzed_data['growing_plants']
                resource_payload['greenhouse_plant_filters'] = " ".join([re.sub(r'[^a-z0-9]+', '-', p.lower()).strip('-') for p in plant_names])
            
            # NOVO: Espelha a lógica de filtro da estufa para a crop machine,
            # permitindo que ela seja filtrada pelos itens que está processando.
            if source_key == "Crop Machine" and analyzed_data and 'growing_plants' in analyzed_data:
                crop_names = analyzed_data['growing_plants']
                resource_payload['greenhouse_plant_filters'] = " ".join([re.sub(r'[^a-z0-9]+', '-', c.lower()).strip('-') for c in crop_names])
            
            if is_large_building:
                overlay_items.append(resource_payload)
            else:
                grid[(x, y)]['resource'] = resource_payload

    aoe_source_names = set()
    placed_collectibles = {**farm_data.get("collectibles", {}), **farm_data.get("home", {}).get("collectibles", {})}
    for item_name, placements in placed_collectibles.items():
        item_details = collectibles_domain.COLLECTIBLES_ITEM_BUFFS.get(item_name)
        if not item_details or "aoe" not in item_details: continue
        hue, sat, light = get_hsl_color_from_string(item_name)
        base_color, extended_color = f"hsla({hue}, {sat}%, {light}%, 0.35)", f"hsla({hue}, {sat - 10}%, {light + 10}%, 0.25)"
        filter_id = re.sub(r'[^a-z0-9]+', '-', item_name.lower()).strip('-')
        base_aoe, skill_aoe = item_details["aoe"], None
        for skill_name in player_skills:
            skill_details = skills_domain.BUMPKIN_REVAMP_SKILLS.get(skill_name)
            if skill_details and any(e.get("name") == "MODIFY_ITEM_AOE" and e.get("target_item") == item_name for e in skill_details.get("effects", [])):
                skill_aoe = next(e["new_aoe"] for e in skill_details.get("effects", []) if e.get("name") == "MODIFY_ITEM_AOE" and e.get("target_item") == item_name)
                break
        for placement in placements:
            coords = placement.get("coordinates", {})
            ax, ay = coords.get("x"), coords.get("y")
            if ax is None or ay is None: continue
            grid[(ax, ay)]["aoe_source"] = {"name": item_name, "icon": get_item_image_path(item_name), "filter_id": filter_id}
            aoe_source_names.add(item_name)
            all_coords.append((ax, ay))
            def get_plots_coords(aoe_def):
                if not aoe_def: return set()
                if aoe_def.get("shape") == "custom": return {tuple(p.values()) for p in aoe_def.get("plots", [])}
                if aoe_def.get("shape") == "circle":
                    r = aoe_def.get("radius", 0)
                    return {(dx, dy) for dx in range(-r, r + 1) for dy in range(-r, r + 1) if not (dx == 0 and dy == 0)}
                return set()
            base_plots, skill_plots = get_plots_coords(base_aoe), get_plots_coords(skill_aoe)
            for dx, dy in base_plots: grid[(ax + dx, ay + dy)]["aoe_items"].append({"name": item_name, "type": "base", "color": base_color, "filter_id": filter_id})
            for dx, dy in (skill_plots - base_plots): grid[(ax + dx, ay + dy)]["aoe_items"].append({"name": item_name, "type": "extended", "color": extended_color, "filter_id": filter_id})
            all_coords.extend([(ax + dx, ay + dy) for dx, dy in base_plots.union(skill_plots)])

    for cell_data in grid.values():
        if cell_data["aoe_items"]:
            colors = sorted(list(set(item["color"] for item in cell_data["aoe_items"] if item.get("color"))))
            cell_data["aoe_sources_str"] = " ".join(sorted(list(set(item.get("filter_id") for item in cell_data["aoe_items"] if item.get("filter_id")))))
            if len(colors) == 1: cell_data.update({"aoe_class": "has-aoe-color", "aoe_background_style": f"--cell-bg-color: {colors[0]};"})
            elif len(colors) > 1: cell_data.update({"aoe_class": "has-aoe-gradient", "aoe_background_style": f"--cell-bg-gradient: linear-gradient(135deg, {', '.join(colors)});"})

    if not all_coords: return None
    min_x, max_x, min_y, max_y = min(c[0] for c in all_coords), max(c[0] for c in all_coords), min(c[1] for c in all_coords), max(c[1] for c in all_coords)

    final_grid_rows = []
    for y_coord in range(max_y, min_y - 1, -1):
        row = []
        for x_coord in range(min_x, max_x + 1):
            row.append(grid.get((x_coord, y_coord), {}))
        final_grid_rows.append(row)

    legend_data = {}
    for name in sorted(list(legend_item_names.union(aoe_source_names))):
        # Adiciona condicional para ignorar cogumelos na legenda
        if name == "Mushroom": continue
        filter_id = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-') 
        legend_data[name] = {"icon": get_item_image_path(name), "aoe_info": None, "filter_id": filter_id}
        if name in aoe_source_names:
            details = collectibles_domain.COLLECTIBLES_ITEM_BUFFS.get(name, {})
            if "aoe" in details:
                hue, sat, light = get_hsl_color_from_string(name)
                aoe_info = {"base_color": f"hsla({hue}, {sat}%, {light}%, 0.5)", "filter_id": filter_id}
                for skill in player_skills:
                    s_details = skills_domain.BUMPKIN_REVAMP_SKILLS.get(skill, {})
                    if any(e.get("name") == "MODIFY_ITEM_AOE" and e.get("target_item") == name for e in s_details.get("effects", [])):
                        aoe_info["extended_color"], aoe_info["skill_name"] = f"hsla({hue}, {sat - 10}%, {light + 10}%, 0.4)", skill
                        break
                legend_data[name]["aoe_info"] = aoe_info
    
    dynamic_legend = _create_dynamic_legend(grid)


    return {
        "final_grid_rows": final_grid_rows,
        "overlay_items": overlay_items,
        "min_x": min_x, "max_x": max_x,
        "min_y": min_y, "max_y": max_y,
        "width": max_x - min_x + 1,
        "height": max_y - min_y + 1,
        "legend": legend_data,
        "crops_in_machine": crops_in_machine_list,
        "dynamic_legend": dynamic_legend
    }

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)