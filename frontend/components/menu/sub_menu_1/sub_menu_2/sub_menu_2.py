from backend.generators.estrategia_propia import matriz_sistema_original, presente_vacio, convertir_y_cambiar
from .sub_menu_3.sub_menu_3 import *
from backend.utils import file_json
from backend.generators import graph_generator, estrategia_propia
from backend.generators import graph_probability
from itertools import product
import streamlit as st
from backend.models.graph import Grafo
from itertools import combinations

Elements = Grafo()
clicks = 0

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
   global clicks


   options = ['Editar la Matriz de Probabilidades', 'Volver a la Matriz Original', 'Ingresar Sistema a Trabajar']
   selected_option = st.sidebar.selectbox('Opciones:', options, index = 2)


   if selected_option == 'Editar la Matriz de Probabilidades':
       st.write("Editar Matriz de Probabilidades")
       graph_probability.editar_matriz()


   if selected_option == 'Volver a la Matriz Original':
       st.write("Volver a la Matriz Original")
       graph_probability.restablecer_matriz()


   st.write("Matriz de Probabilidades:")
   graph_probability.mostrar_tabla(graph_probability.probabilities)


   if selected_option == 'Ingresar Sistema a Trabajar':
       graph_probability.trabajar_sistema()

def string_a_lista_de_listas(string):
    lista = []
    l = []
    for i, j in enumerate(string):  # Corregimos el uso de enumerate
        if i != 0 and i != len(string)-1:
            if j == '[':
                for ii, jj in enumerate(string):  # Corregimos el uso de enumerate
                    if ii > i:  # Corregimos la lógica de comparación
                        if jj == ']':
                            break
                        if jj.isdigit() or jj.replace('.', '').isdigit():  # Corregimos la verificación numérica
                            l.append(float(jj))  # Convertimos a float en lugar de int para manejar decimales
                lista.append(l)
                l = []  # Reiniciamos la lista interna para la próxima sublista

    return lista


def trabajar_sistema(dic1, dic2):
    global probabilities
    global matrices
    print(dic1,f'\n{dic2}')
    string = st.text_input("Introduce el sistema a trabajar:")
    execution_time = 0
    if st.button("Empezar"):
        empezar_trabajo(string, execution_time,dic1)
    else:
        graph_probability.crear_grafo()

def generate_combinations(present_states, future_states):
    return [
        (present_state, future_state)
        for i in range(len(present_states) + 1)
        for present_state in combinations(present_states, i)
        for j in range(len(future_states) + 1)
        for future_state in combinations(future_states, j)
        if not (present_state == future_state and present_state != ())
           and not (present_state == () and future_state == ())
           and not (present_state == tuple(present_states) and future_state == tuple(future_states))
    ]

def empezar_trabajo(string, execution_time, dic1):
    global states
    estados = []
    pr_states, fu_states, iState = graph_probability.parse_input_string(string)
    presentes, futuros = sistema_original(fu_states, pr_states)
    if len(iState) == len(presentes):
        combinations = generate_combinations(pr_states, fu_states)
        primera = 'A'
        for i in range(len(matrices)):
            estados.append(primera)
            primera = graph_probability.siguiente_letra_mayuscula(primera)
        matriz = matriz_sistema_original(dic1,pr_states, fu_states, futuros, presentes)
        print(futuros, presentes, iState)
        # Recorrer cada elemento de la lista
        for elemento in combinations:
            futuro, presente = elemento
            # Validar si el presente elemento es ()
            if presente == () and len(futuro) == 1:
                presente_vacio(elemento, futuro, futuros, dic1, iState, combinations)
            # Validar si el futuro elemento es ()
            if futuro == () and len(presente) == 1:
                print(elemento)
                valor = [1]
                print(valor)
                letra = presente[0]
                indice = presentes[letra]
                complemento = combinations[int(len(combinations)-(indice+1))]
                presentes2 = complemento[1]
                aux = {}
                print('presentes: ', presentes, presentes2)
                new_states = convertir_y_cambiar(states)
                for i in range(len(new_states)):
                    l = []
                    for clave, valor in presentes.items():
                        if clave in presentes2:
                            for j in range(len(new_states[i])):
                                if j == valor:
                                    l.append(new_states[i][j])
                            aux[i] = l
                print(aux)
                pot = 0
                i = 0
                for estado in iState:
                    if estado == 1:
                        pot += sub_menu_2.pot(i)
                    i+=1

def sistema_original(fu_states, pr_states):
    fu, pr = crear_diccionarios(fu_states, pr_states)
    return pr, fu

def crear_dict_pr(pr_states):
    primera = 'A'
    pr = {}
    j = 0

    while (len(pr_states) != len(pr)):
        if primera in pr_states:
            pr[primera] = j
        j += 1
        primera = graph_probability.siguiente_letra_mayuscula(primera)

    return pr

def crear_dict_fu(fu_states):
    primera = 'A'
    fu = {}
    j = 0

    while (len(fu_states) != len(fu)):
        if primera in fu_states:
            fu[primera] = j
        j += 1
        primera = graph_probability.siguiente_letra_mayuscula(primera)

    return fu

def crear_diccionarios(fu_states, pr_states):
    return crear_dict_pr(pr_states), crear_dict_fu(fu_states)

def strategy_3_menu():
    st.subheader('Estrategia 3')

    options = ['Editar la Matriz de Probabilidades', 'Volver a la Matriz Original', 'Ingresar Sistema a Trabajar']
    selected_option = st.sidebar.selectbox('Opciones:', options, index=2)

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
    cant = st.number_input('Ingrese la cantidad de nodos', min_value=1, value=1)
    dimension = pot(cant)
    combinaciones = generate_binary_combinations(cant)
    graph_probability.probabilities = crear_matriz_cero(dimension)
    graph_probability.states = combinaciones
    graph_probability.matrices = []
    matrices = []
    for i in range(cant):
        text = st.text_input(f'Ingresar matriz para {primera}:')
        if text != '':
            matrices.append(estrategia_propia.mostrar_tablas(text, primera))
        primera = graph_probability.siguiente_letra_mayuscula(primera)

    if selected_option == 'Ingresar Sistema a Trabajar':
        dic1, dic2 = llenar_unos()
        estrategia_propia.trabajar_sistema3(dic1, dic2, matrices)

def validar_posicion(dic):
    dic2 = {}
    for clave, valor in dic.items():
        new = 0
        for i in range(len(valor)):
            new += pot(i) * valor[i]
            dic2[clave] = new
    return dic2

def llenar_unos():
    matrices = graph_probability.matrices
    probabilities = graph_probability.probabilities
    dic = {}
    for i in range(len(matrices)):
        for j in range(len(matrices[i])):
            dic[j] = []
    for i in range(len(matrices)):
        for j in range(len(matrices[i])):
            dic[j].append(matrices[i][j][len(matrices[i][j])-1])
    dic2 = validar_posicion(dic)
    for clave, valor in dic.items():
        probabilities[int(clave)][int(len(valor))] = 1
    return dic, dic2

def pot(n):
    return 2**n

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