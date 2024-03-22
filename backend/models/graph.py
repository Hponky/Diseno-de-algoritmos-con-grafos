import streamlit as st
import string
import json
from backend.generators.json_elements import *
from streamlit_react_flow import react_flow
from documents.saved import *

elementos = []

class Elements:
    def get_elements():
        global elementos
        return elementos

    def set_elements(elements):
        global elementos
        elementos = elements

    def find_index_node_by_label(label, elements):
        elements = create_elements_from_list(elements)
        for i, element in enumerate(elements):  # Utiliza enumerate para obtener tanto el índice como el elemento
            if 'data' in element and 'label' in element['data']:
                if label == element['data']['label']:  # Utiliza == en lugar de 'is' para comparar cadenas
                    node_found = i
                    return node_found
                    break  # Termina el bucle una vez que se ha encontrado el nodo
            else:
                print("El elemento no tiene la estructura esperada:", element)
        return -1

    def generate_numeric_guid(counter):
        counter += 1
        return counter

    def show_node_coordinates(graph_data):
        # Función para actualizar las coordenadas de los nodos en tiempo real
        def update_coordinates(event):
            if event["core_as_json"]:
                st.write("Coordenadas actualizadas en tiempo real:")
                for node in event["core_as_json"]["elements"]["nodes"]:
                    node_id = node["data"]["id"]
                    node_position = node["position"]
                    st.write(f"Nodo {node_id}: ({node_position['x']}, {node_position['y']})")

    def find_element(lista, elemento):
        """
        Encuentra la primera aparición del elemento en la lista.

        Args:
        lista (list): La lista en la que se busca el elemento.
        elemento: El elemento que se desea encontrar en la lista.

        Returns:
        int: El índice de la primera aparición del elemento en la lista.
             Retorna -1 si el elemento no se encuentra en la lista.
        """
        try:
            indice = lista.index(elemento)
            return indice
        except ValueError:
            return -1
    # Otras funciones de la clase

    # Pila para almacenar los cambios realizados
    cambios_realizados = []

    @staticmethod
    def add_node(graph, node_id, node_label):
        # Función para añadir un nodo al grafo
        # Código de la función ...

        """
                Añade un nodo al grafo.

                Args:
                - graph: Lista que representa el grafo.
                - node_id: Identificador único del nodo a añadir.
                - node_data: Información asociada al nodo a añadir.
                """
        new_node = {
            "id": str(node_id),
            "type": "default",
            "data": {"label": node_label},
            "position": {"x": 0, "y": 0}
        }
        graph.append(new_node)

        # Guardar el cambio realizado en la pila
        Elements.cambios_realizados.append(("add_node", (node_id, node_label)))
        return graph

    @staticmethod
    def delete_edge(graph, source_id, target_id):
        # Función para eliminar una conexión entre nodos en el grafo
        # Código de la función ...

        # Guardar el cambio realizado en la pila
        Elements.cambios_realizados.append(("delete_edge", (source_id, target_id)))
        return graph

    @staticmethod
    def undo_last_change(graph):
        # Función para deshacer el último cambio realizado
        if Elements.cambios_realizados:
            # Obtener el último cambio realizado de la pila
            ultimo_cambio = Elements.cambios_realizados.pop()

            # Deshacer el último cambio
            if ultimo_cambio[0] == "add_node":
                # Si el último cambio fue agregar un nodo, eliminamos el nodo
                _, (node_id, _) = ultimo_cambio
                graph = [node for node in graph if node['id'] != node_id]
            elif ultimo_cambio[0] == "delete_edge":
                # Si el último cambio fue eliminar una conexión entre nodos, volvemos a conectar los nodos
                _, (source_id, target_id) = ultimo_cambio
                for node in graph:
                    if node['id'] == source_id:
                        node['linkedTo'].append({"nodeId": target_id, "weight": None})
                    elif node['id'] == target_id:
                        node['linkedTo'].append({"nodeId": source_id, "weight": None})
            return graph
        else:
            return graph

    def open_txt():
        # Cargar archivo
        uploaded_file = st.file_uploader("Cargar archivo", type=["txt"])

        if uploaded_file is not None:
            if uploaded_file.type == 'text/plain':  # Si el archivo es de tipo txt
                txt_content = uploaded_file.getvalue().decode("utf-8")
                st.text_area("Contenido TXT", value=txt_content, height=400)
                Elements.set_elements(create_elements_from_json(uploaded_file))
                Elements.set_elements(transform_graph(Elements.get_elements()))
                Elements.set_elements(create_elements_from_list(Elements.get_elements()))
                flow_styles = {"height": 500, "width": 800}
                react_flow("graph", elements=Elements.get_elements(), flow_styles=flow_styles)

    def open_json():
        # Cargar archivo
        uploaded_file = None
        uploaded_file = st.file_uploader("Cargar archivo", type=["json"])

        if uploaded_file is not None:
            # Cargar el archivo JSON
            if uploaded_file.type == 'application/json':
                Elements.set_elements(create_elements_from_json(uploaded_file))
                flow_styles = {"height": 500, "width": 800}
                react_flow("graph", elements=Elements.get_elements(), flow_styles=flow_styles)
