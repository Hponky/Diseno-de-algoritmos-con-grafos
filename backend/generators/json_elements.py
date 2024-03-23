import json
import random
import streamlit as st
from streamlit_react_flow import react_flow

def convert_to_save_elements(elements):
    react_elements = []
    added_nodes = set()  # Conjunto para rastrear nodos ya agregados
    edge_ids = set()  # Conjunto para rastrear las IDs de los bordes agregados

    # Crear nodos con posición (x: 0, y: 0) y clave linkedTo
    for element in elements:
        node_id = element["id"]
        if not node_id.startswith("edge-"):  # Evitar agregar nodos de conexión
            node_data = element.get("data", {})
            x = random.randint(100, 400)
            y = random.randint(100, 200)
            react_node = {
                "id": node_id,
                "label": node_data.get("label", ""),
                "data": {},
                "type": "default",
                "linkedTo": [],  # Inicializar lista de conexiones
                "radius": 0.5,
                "coordinates": {"x": x, "y": y},
            }
            react_elements.append(react_node)
            added_nodes.add(node_id)

    # Agregar conexiones entre nodos
    for element in elements:
        if element["id"].startswith("edge-"):  # Verificar si es un nodo de conexión
            edge_id = element["id"]
            if edge_id not in edge_ids:  # Verificar si el borde ya ha sido procesado
                source_id, target_id = element["source"], element["target"]
                for node in react_elements:
                    if node["id"] == source_id:
                        react_edge2 = {
                            "nodeId": target_id,
                            "weight": random.randint(10, 99)
                        }
                        node["linkedTo"].append(react_edge2)
                edge_ids.add(edge_id)  # Agregar el ID del borde al conjunto de bordes procesados

    return react_elements

def convert_to_react_flow(elements):
    react_elements = []
    added_nodes = set()  # Conjunto para rastrear nodos ya agregados

    # Crear nodos con posición (x: 0, y: 0) y clave linkedTo
    for element in elements:
        node_id = element["id"]
        if not node_id.startswith("edge-"):  # Evitar agregar nodos de conexión
            node_data = element.get("data", {})
            x = random.randint(100,400)
            y = random.randint(100,200)
            react_node = {
                "id": node_id,
                "type": "default",
                "data": {"label": node_data.get("label", "")},
                "position": {"x": x, "y": y},
                "linkedTo": []  # Inicializar lista de conexiones
            }
            react_elements.append(react_node)
            added_nodes.add(node_id)

    # Agregar conexiones entre nodos
    for element in elements:
        node_id = element["id"]
        if node_id.startswith("edge-"):  # Verificar si es un nodo de conexión
            source_id, target_id = element["source"], element["target"]
            for element in elements:
                node_id = element["id"]
                if node_id.startswith("edge-"):  # Verificar si es un nodo de conexión
                    source_id, target_id = element["source"], element["target"]

                    for node in react_elements:
                        if node["id"] == source_id:
                            react_edge2 = {
                                "nodeId": target_id,
                                "weight": random.randint(10, 99)
                            }
                            node["linkedTo"].append(react_edge2)

                    for node in react_elements:
                        if node["id"] == source_id:
                            edge_id = f"edge-{source_id}-{target_id}"
                            react_edge = {
                                "id": edge_id,
                                "source": source_id,
                                "target": target_id,
                                "animated": True  # Opcional: para animación entre nodos
                            }
                            node["linkedTo"].append(react_edge)

    return react_elements

def extract_node_data(node_data):
    node_id = str(node_data["id"])
    node_label = node_data.get("label", node_id)
    node_type = node_data.get("type", "default")
    node_position = node_data.get("coordenates", {"x": 0, "y": 0})
    return {
        "id": node_id,
        "type": node_type,
        "data": {"label": node_label},
        "position": {"x": node_position["x"], "y": node_position["y"]}
    }

def extract_edge_data(node_id, link):
    target_id = str(link["nodeId"])
    return {
        "id": f"edge-{node_id}-{target_id}",
        "source": node_id,
        "target": target_id,
        "animated": True
    }

def transform_graph(elements):
    transformed_elements = []
    for element in elements:
        if isinstance(element, dict) and "data" in element and isinstance(element["data"], dict) and "label" in element["data"]:
            transformed_elements.append({
                'id': element['id'],
                'type': element['type'],
                'data': {'label': element['data']['label']},
                'position': {'x': 0, 'y': 0},
                'linkedTo': [] if 'linkedTo' not in element else element['linkedTo']
            })
    return transformed_elements


def create_elements_from_list(data_list):
    elements = []

    for node_data in data_list:
        elements.append(node_data)

        linked_to = node_data.get("linkedTo", [])
        for link in linked_to:
            edge = extract_edge_data(node_data["id"], link)
            elements.append(edge)
    return elements

def create_elements_from_json(uploaded_file):
    elements = []

    json_data = json.load(uploaded_file)
    print(json_data, "json neto")
    nodes = json_data["graph"][0]["data"]

    for node_data in nodes:
        node = extract_node_data(node_data)
        elements.append(node)

        linked_to = node_data.get("linkedTo", [])
        for link in linked_to:
            edge = extract_edge_data(node["id"], link)
            elements.append(edge)
    print(elements, "create elements  from json")
    return elements