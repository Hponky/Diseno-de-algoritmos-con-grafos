import random
from .sub_menu_3.sub_menu_3 import *
from backend.utils import file_json
from backend.generators import json_elements
from backend.models.graph import Elements
from backend.generators import graph_generator
from streamlit_react_flow import react_flow


counter = random.randint(100000,999999)
def new_grafo_menu():
    options = ["Personalizado", "Aleatorio"]
    selected_option = st.sidebar.selectbox("Seleccionar tipo de nuevo grafo", options, index=0)
    if selected_option is not None:
        st.write(f"Seleccionaste la opción de nuevo grafo: {selected_option}")
        if selected_option == "Personalizado":
            options_1 = ["Agregar Nodo", "Agregar Arista"]
            selected_option_1 = st.selectbox(f"Seleccione la opción que desea", options_1, index=0)
            if selected_option_1 is not None:
                if selected_option_1 == "Agregar Nodo":
                    add_node()
                elif selected_option_1 == "Agregar Arista":
                    graph_generator.manual_conection(Elements.get_elements())
        if selected_option == "Aleatorio":
            num_nodes = st.number_input("Cantidad de nodos", min_value=1, value=5)

            directed = st.checkbox("Dirigido")
            weighted = st.checkbox("Ponderado")
            connected = st.checkbox("Conexo")
            complete = st.checkbox("Completo")

            grafo_aleatorio = graph_generator.random_graph(num_nodes=num_nodes,
                                                  directed=directed,
                                                  weighted=weighted,
                                                  connected=connected,
                                                  complete=complete)
            Elements.set_elements(grafo_aleatorio)

        Elements.set_elements(json_elements.transform_graph(Elements.get_elements()))
        Elements.set_elements(json_elements.create_elements_from_list(Elements.get_elements()))
        flow_styles = {"height": 500, "width": 800}
        react_flow("graph", elements=Elements.get_elements(), flow_styles=flow_styles)


def export_data_menu():
    options = ["Excel", "Imagen"]
    selected_option = st.sidebar.selectbox("Seleccionar tipo de exportación de datos", options)
    st.write(f"Seleccionaste la opción de exportación de datos: {selected_option}")
    if selected_option == "Excel":
        nombreArchivo = st.text_input("Ingrese el nombre con que desea exportar el archivo:")
        if nombreArchivo != "":
            file_json.export_graph_to_excel(Elements.get_elements(), "exported/" + nombreArchivo + ".xlsx")
            st.write(f"Grafo exportado exitosamente: {nombreArchivo}.xlsx")


def edit_nodo_menu():
    options = ["Agregar", "Editar", "Eliminar"]
    selected_option = st.sidebar.selectbox("Seleccionar tipo de edición de nodo", options, index=0)

    if selected_option == "Agregar":
        add_node()
    elif selected_option == "Eliminar":
        # Obtener los nombres de los nodos que tienen la clave 'label'
        opciones = []

        for element in Elements.get_elements():
            if 'data' in element and 'label' in element['data']:
                opciones.append(element['data']['label'])

        if opciones:
            # Seleccionar nodo a eliminar
            label_container = st.empty()
            index = -1
            label = st.selectbox(f"Seleccione la opción que desea", opciones, index)

            if label is not None and st.button("Confirmar"):
                node_id = Elements.find_index_node_by_label(label, Elements.get_elements())
                if node_id is not -1:
                    st.success("Se ha eliminado el nodo satisfactoriamente")
                    Elements.get_elements().pop(node_id)
                    # Actualizar la lista de opciones y reinicializar el selectbox
                opciones = [element.get("label", "") for element in Elements.get_elements() if 'data' in element and 'label' in element['data']]
                label_container.empty()
        else:
            st.warning("No hay nodos disponibles para eliminar.")

def add_node():
    global counter
    counter = Elements.generate_numeric_guid(counter)
    nombre = st.text_input("Ingrese el nombre del nodo:")
    if nombre != "":
        repetido = False
        for element in Elements.get_elements():
            if 'data' in element and 'label' in element['data'] and nombre == element['data']["label"]:
                repetido = True
        if not repetido:
            change = Elements.add_node(Elements.get_elements(), counter, nombre)
            Elements.set_elements(change)
            st.success(f"Nodo '{nombre}' agregado correctamente")
        else:
            st.warning("Ya existe un nodo con ese nombre")

def edit_arco_menu():
    options = ["Agregar", "Editar", "Eliminar"]
    selected_option = st.sidebar.selectbox("Seleccionar tipo de edición de arista", options, index= 0)
    if selected_option is not None:
        st.write(f"Seleccionaste la opción de edición de arista: {selected_option}")
        if selected_option == "Agregar":
            graph_generator.manual_conection(Elements.get_elements())
        if selected_option == "Eliminar":
            # Obtener los IDs de los nodos conectados
            nodos_conectados = set()
            for element in Elements.get_elements():
                if 'source' in element:
                    nodos_conectados.add(element['source'])
                if 'target' in element:
                    nodos_conectados.add(element['target'])

            # Filtrar los nodos que tienen alguna conexión para los nodos de origen
            opciones_origen = [element['data']['label'] for element in Elements.get_elements()
                               if
                               'data' in element and 'label' in element['data'] and element['id'] in nodos_conectados]

            # Filtrar los nodos que tienen alguna conexión para los nodos de destino
            opciones_destino = [element['data']['label'] for element in Elements.get_elements()
                                if
                                'data' in element and 'label' in element['data'] and element['id'] in nodos_conectados]

            # Seleccionar nodo origen y destino para eliminar la conexión
            origen = st.selectbox("Selecciona el nodo de origen:", opciones_origen, index=0)
            destino = st.selectbox("Selecciona el nodo de destino:", opciones_destino, index=0)
            if st.button("Eliminar"):
                if origen is not None and destino is not None:
                    # Encontrar los IDs de los nodos de origen y destino
                    source_id = ''
                    target_id = ''
                    for element in Elements.get_elements():
                        if 'data' in element and 'label' in element['data']:
                            if element['data']['label'] == origen:
                                source_id = element['id']
                            if element['data']['label'] == destino:
                                target_id = element['id']

                    # Eliminar la conexión entre los nodos
                    updated_elements = []
                    found = False
                    for element in Elements.get_elements():
                        if 'source' in element and 'target' in element:
                            if element['source'] == source_id and element['target'] == target_id and source_id != target_id:
                                # No agregamos esta conexión a la lista de elementos actualizados
                                st.success(f"Conexión de '{origen}' a '{destino}' eliminado correctamente")
                                found = True
                                continue
                        # Agregamos todas las otras conexiones y nodos a la lista de elementos actualizados
                        updated_elements.append(element)
                    if not found:
                        st.warning("Seleccionaste una opción inválida")
                    # Actualizar los elementos en Elements
                    Elements.set_elements(updated_elements)


def processes_menu():
    options = ["Proceso 1", "Proceso 2", "Proceso 3"]
    selected_option = st.sidebar.selectbox("Seleccionar proceso", options)
    st.write(f"Seleccionaste la opción de ejecución de procesos: {selected_option}")