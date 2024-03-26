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
            Elements.set_elements(json_elements.transform_graph(Elements.get_elements()))
        if selected_option == "Aleatorio":
            if not Elements.get_created():
                Elements.set_elements([])
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
                    print(node_id, "indice a eliminar")
                    Elements.get_elements().pop(node_id)
                    # Actualizar la lista de opciones y reinicializar el selectbox
                opciones = [element.get("label", "") for element in Elements.get_elements() if 'data' in element and 'label' in element['data']]
                label_container.empty()
        else:
            st.warning("No hay nodos disponibles para eliminar.")
    Elements.set_elements(json_elements.create_elements_from_list(Elements.get_elements()))
    flow_styles = {"height": 500, "width": 800}
    react_flow("graph", elements=Elements.get_elements(), flow_styles=flow_styles)

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
    selected_option = st.sidebar.selectbox("Seleccionar tipo de edición de arista", options, index=0)
    tipo_arista = st.sidebar.radio("Tipo de arista", ["Dirigida", "No dirigida"])
    if selected_option is not None:
        st.write(f"Seleccionaste la opción de edición de arista: {selected_option}")
        st.write(f"Tipo de arista seleccionada: {tipo_arista}")

        if selected_option == "Agregar":
            graph_generator.manual_conection(Elements.get_elements())
        elif selected_option == "Eliminar":
            # Eliminar la conexión entre los nodos
            eliminar_conexion()

    actualizar_elementos_y_mostrar_flujo()


def obtener_nodos_conectados(elementos):
    nodos_conectados_origen = {element.get('source') for element in elementos if 'source' in element}
    nodos_conectados_destino = {int(element.get('target')) for element in elementos if 'target' in element}
    return nodos_conectados_origen, nodos_conectados_destino


def filtrar_opciones(nodos_conectados, elementos):
    return [element['data']['label'] for element in elementos
            if 'data' in element and 'label' in element['data']
            and element['id'] in nodos_conectados]


def encontrar_id_nodo(label, elementos):
    return next((element['id'] for element in elementos if
                 'data' in element and 'label' in element['data'] and element['data']['label'] == label), None)


def eliminar_conexion():
    elementos = Elements.get_elements()
    nodos_conectados_origen, nodos_conectados_destino = obtener_nodos_conectados(elementos)

    opciones_origen = filtrar_opciones(nodos_conectados_origen, elementos)
    opciones_destino = filtrar_opciones(nodos_conectados_destino, elementos)

    if opciones_origen and opciones_destino:
        origen = st.selectbox("Selecciona el nodo de origen:", opciones_origen, index=0)
        destino = st.selectbox("Selecciona el nodo de destino:", opciones_destino, index=0)

        if st.button("Eliminar"):
            if origen is not None and destino is not None:
                source_id = encontrar_id_nodo(origen, elementos)
                target_id = encontrar_id_nodo(destino, elementos)

                if source_id is not None and target_id is not None:
                    updated_elements = [element for element in elementos
                                        if not ('source' in element and 'target' in element
                                                and element['source'] == source_id
                                                and int(element['target']) == target_id)]

                    for element in updated_elements:
                        if element.get('id') == source_id:
                            element['linkedTo'] = [link for link in element.get('linkedTo', []) if
                                                   link.get('nodeId') != target_id]

                    if len(updated_elements) < len(elementos):
                        st.success(f"Conexión de '{origen}' a '{destino}' eliminada correctamente")
                        Elements.set_elements(updated_elements)
                    else:
                        st.warning("No se encontró la conexión para eliminar")
                else:
                    st.warning("No se encontraron los nodos de origen y destino especificados")


def actualizar_elementos_y_mostrar_flujo():
    Elements.set_elements(json_elements.create_elements_from_list(Elements.get_elements()))
    flow_styles = {"height": 500, "width": 800}
    react_flow("graph", elements=Elements.get_elements(), flow_styles=flow_styles)


def processes_menu():
    options = ["Proceso 1", "Proceso 2", "Proceso 3"]
    selected_option = st.sidebar.selectbox("Seleccionar proceso", options)
    st.write(f"Seleccionaste la opción de ejecución de procesos: {selected_option}")