import random
import pandas as pd

from itertools import product
from .sub_menu_3.sub_menu_3 import *
from backend.utils import file_json
from backend.generators import json_elements
from backend.models.graph import Grafo
from backend.generators import graph_generator
from streamlit_react_flow import react_flow
from backend.generators import graph_probability

Elements = Grafo()
matrices = []
import ast

def procesar_entrada(entrada, matriz_probabilidad):

    for conjunto in entrada:
        for vector in conjunto:
            # Convertir cada vector en una cadena para usarla como índice
            index = int("".join(map(str, vector)), 2)
            # Determinar la fila y columna donde debe ir el "1"
            fila = index // 32
            columna = index % 32
            # Colocar el "1" en la posición correspondiente de la matriz
            matriz_probabilidad[fila][columna] = 1

def crear_matriz_cero(n):
    return [[0 for _ in range(n)] for _ in range(n)]

def strategy_1_menu():
    st.subheader('Estrategia 1')
    global matrices

    options = ['Editar la Matriz de Probabilidades', 'Volver a la Matriz Original', 'Ingresar Sistema a Trabajar']
    selected_option = st.sidebar.selectbox('Opciones:', options, index = 2)

    if selected_option == 'Editar la Matriz de Probabilidades':
        st.write("Editar Matriz de Probabilidades")
        graph_probability.editar_matriz()

    if selected_option == 'Volver a la Matriz Original':
        st.write("Volver a la Matriz Original")
        graph_probability.restablecer_matriz()

    st.write('Ingrese las matrices en el siguiente formato: ')
    st.write('[\n[0, 0, 0, 0, 1],\n[1, 0, 0, 1, 0],\n[0, 1, 0, 1, 0],\n[1, 1, 0, 0, 1],\n[0, 0, 1, 1, 0],'
             '\n[1, 0, 1, 0, 1],\n[0, 1, 1, 0, 1],\n[1, 1, 1, 1, 0],]')
    primera = 'A'
    cant = st.number_input('Ingrese la cantidad de nodos',  min_value=1, value=1)
    pot = 1
    for i in range(cant):
        pot *= 2
        matrices.append('')

    graph_probability.probabilities = crear_matriz_cero(pot)
    combinaciones = generate_binary_combinations(cant)
    graph_probability.states = combinaciones
    x = 0
    for i in range(pot):
        c = combinaciones[i]
        lista = []
        for i in c:
            lista.append(int(i))
        cambio_matriz(lista,cant)
        print(lista)

    for i in range(cant):
        text = st.text_input(f'Ingresar matriz para {primera}:')
        primera = graph_probability.siguiente_letra_mayuscula(primera)
        matrices[i]=text
    print(matrices)
    st.write("Matriz de Probabilidades:")
    graph_probability.mostrar_tabla(graph_probability.probabilities)

    if selected_option == 'Ingresar Sistema a Trabajar':
        graph_probability.trabajar_sistema()

def generate_binary_combinations(n):
    """
    Genera todas las combinaciones binarias posibles de n bits.

    Args:
    n (int): Número de bits.

    Returns:
    List[str]: Lista de combinaciones binarias en formato de cadenas.
    """
    combinations = [''.join(bits) for bits in product('01', repeat=n)]
    return combinations


def cambio_matriz(lista, cant):
    global matrices
    # Crear la representación de texto de la lista
    text = '[' + ','.join(map(str, lista)) + ','

    # Calcular el valor x
    x = 0
    pot = 1
    for i in lista:
        x += i * pot
        pot *= 2
    print("Lista:", lista)

    # Inicializar y y pot para la segunda parte
    pot = 1
    y = 0

    # Imprimir el texto para depuración
    print("Texto de búsqueda:", text + "0,1]")

    # Verificar la presencia en las matrices
    for matriz in matrices:
        print("Evaluando matriz:", matriz)
        if f'{text}0,1]' in matriz:
            print('Encontrado en:', matriz)
            y += pot
        pot *= 2

    # Actualizar la matriz de probabilidades
    graph_probability.probabilities[x][y] = 1

    # Imprimir x y y para depuración
    print("x:", x)
    print("y:", y)

def new_grafo_menu():
    options = ["Personalizado", "Aleatorio"]
    selected_option = st.sidebar.selectbox("Seleccionar tipo de nuevo grafo", options, index=0)
    if selected_option is not None:
        st.write(f"Seleccionaste la opción de nuevo grafo: {selected_option}")
        if selected_option == "Personalizado":
            graph_generator.custom_graph()
        if selected_option == "Aleatorio":
            Elements.set_elements([])
            num_nodes = st.number_input("Cantidad de nodos", min_value=1, value=5)

            directed = st.checkbox("Dirigido")
            weighted = st.checkbox("Ponderado")
            connected = st.checkbox("Conexo")
            complete = st.checkbox("Completo")

            graph_generator.random_graph(num_nodes=num_nodes,
                                                  directed=directed,
                                                  weighted=weighted,
                                                  connected=connected,
                                                  complete=complete)
        Elements.display_flow()

def export_data_menu():
    options = ["Excel", "Imagen"]
    selected_option = st.sidebar.selectbox("Seleccionar tipo de exportación de datos", options)
    st.write(f"Seleccionaste la opción de exportación de datos: {selected_option}")
    if selected_option == "Excel":
        nombreArchivo = st.text_input("Ingrese el nombre con que desea exportar el archivo:")
        if nombreArchivo != "":
            file_json.create_directory('documents/exported')
            file_json.export_graph_to_excel(Elements.get_elements(), "documents/exported/" + nombreArchivo + ".xlsx")
            st.write(f"Grafo exportado exitosamente: {nombreArchivo}.xlsx")

def edit_nodo_menu():

    options = ["Agregar", "Editar", "Eliminar"]
    selected_option = st.sidebar.selectbox("Seleccionar tipo de edición de nodo", options, index=0)

    if selected_option == "Agregar":
        graph_generator.add_custom_node()
    elif selected_option == "Editar":
        handle_edit_node()
    elif selected_option == "Eliminar":
        handle_remove_node()
    Elements.display_flow()

def handle_edit_node():
    edit_options = ["Cambiar color", "Cambiar nombre", "Cambiar valor"]
    selected_edit_option = st.sidebar.selectbox("Selecciona lo que deseas editar del nodo", edit_options, index=0)

    if selected_edit_option == "Cambiar color":
        edit_node_color()
    elif selected_edit_option == "Cambiar nombre":
        edit_node_label()
    elif selected_edit_option == "Cambiar valor":
        edit_node_value()

def edit_node_color():
    color = st.color_picker('Elige un color', '#00f900')
    st.write('El color actual es', color)
    nodes = [element['data']['label'] for element in Elements.get_elements()
             if 'data' in element and 'label' in element['data']]

    label = st.selectbox(f"Seleccione el nodo que desea colorear", nodes, index=0)

    if label is not None and st.button("Confirmar"):
        node_index = Elements.find_index_node_by_label(label, Elements.get_elements())
        if node_index != -1:
            st.success("Se ha coloreado el nodo satisfactoriamente")
            Elements.get_elements()[node_index]['style']['background'] = color


def edit_node_label():
    new_label = st.text_input('Escribe el nuevo nombre')
    nodes = [element['data']['label'] for element in Elements.get_elements()
             if 'data' in element and 'label' in element['data']]

    label = st.selectbox(f"Seleccione el nodo que desea renombrar", nodes, index=0)

    if label is not None and st.button("Confirmar"):
        node_index = Elements.find_index_node_by_label(label, Elements.get_elements())
        if node_index != -1:
            st.success("Se ha renombrado el nodo satisfactoriamente")
            Elements.get_elements()[node_index]['data']['label'] = new_label


def edit_node_value():
    new_value = st.number_input('Escribe el nuevo valor')
    nodes = [element['data']['label'] for element in Elements.get_elements()
             if 'data' in element and 'label' in element['data']]

    label = st.selectbox(f"Seleccione el nodo que desea revaluar", nodes, index=0)

    if label is not None and st.button("Confirmar"):
        node_index = Elements.find_index_node_by_label(label, Elements.get_elements())
        if node_index != -1:
            st.success("Se ha revaluado el nodo satisfactoriamente")
            Elements.get_elements()[node_index]['data']['value'] = new_value


def handle_remove_node():
    nodes = [element['data']['label'] for element in Elements.get_elements()
             if 'data' in element and 'label' in element['data']]

    if nodes:
        label = st.selectbox(f"Seleccione el nodo que desea eliminar", nodes, index=0)

        if label is not None and st.button("Confirmar"):
            node_id = Elements.find_index_node_by_label(label, Elements.get_elements())
            if node_id != -1:
                st.success("Se ha eliminado el nodo satisfactoriamente")
                Elements.get_elements().pop(node_id)
    else:
        st.warning("No hay nodos disponibles para eliminar.")

def edit_arco_menu():
    options = ["Agregar", "Editar", "Eliminar"]
    selected_option = st.sidebar.selectbox("Seleccionar tipo de edición de arista", options, index=0)
    tipo_arista = st.sidebar.radio("Tipo de arista", ["Dirigida", "No dirigida"])
    if selected_option is not None:
        st.write(f"Seleccionaste la opción de edición de arista: {selected_option}")
        st.write(f"Tipo de arista seleccionada: {tipo_arista}")
        if selected_option == "Agregar":
            graph_generator.manual_conection(tipo_arista)
        elif selected_option == "Eliminar":
            eliminar_conexion()
    Elements.display_flow()


def obtener_nodos_conectados(elementos):
    nodos_conectados_origen = {}
    nodos_conectados_destino = {}
    for element in elementos:
        if 'source' in element:
            nodos_conectados_origen[str(element.get('source'))] = (str(element.get('source')))
            if 'animated' in element:
                if not element['animated']:
                    nodos_conectados_destino[str(element.get('source'))] = (str(element.get('source')))
        if 'target' in element:
            nodos_conectados_destino[str(element.get('target'))]=(str(element.get('target')))
            if 'animated' in element:
                if not element['animated']:
                    nodos_conectados_origen[str(element.get('target'))] = (str(element.get('target')))

    return nodos_conectados_origen, nodos_conectados_destino


def filtrar_opciones(nodos_conectados, elementos):
    return [element['data']['label'] for element in elementos
            if 'data' in element and 'label' in element['data']
            and str(element['id']) in nodos_conectados]


def encontrar_id_nodo(label, elementos):
    return next((str(element['id']) for element in elementos if
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
                    Elements.delete_conetion(elementos,source_id,target_id, origen, destino)
                else:
                    st.warning("No se encontraron los nodos de origen y destino especificados")
    else:
        st.subheader("No hay aristas a eliminar")

def processes_menu():
    options = ["Proceso 1", "Proceso 2", "Proceso 3"]
    selected_option = st.sidebar.selectbox("Seleccionar proceso", options)
    st.write(f"Seleccionaste la opción de ejecución de procesos: {selected_option}")
