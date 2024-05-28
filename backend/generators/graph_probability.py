import uuid
import pandas as pd
import streamlit as st
import timeit
import time
import matplotlib.pyplot as plt
import numpy as np
import re
import queue

from scipy.stats import wasserstein_distance
from streamlit_react_flow import react_flow
from queue import PriorityQueue
from itertools import combinations, chain
from backend.models.graph import Grafo
from frontend.components.menu.sub_menu_1.sub_menu_2 import sub_menu_2

probabilities = [
    [1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0],
]

states = [
    [0, 0, 0],
    [1, 0, 0],
    [0, 1, 0],
    [1, 1, 0],
    [0, 0, 1],
    [1, 0, 1],
    [0, 1, 1],
    [1, 1, 1],
]

graph = []



def restablecer_matriz():
    original = [
                [1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0],
            ]
    global probabilities
    if probabilities != original :
        st.warning("Se perderán los cambios actuales")
        if st.button("Confirmar"):
            probabilities = original
    else:
        st.success("Se restableció la matriz original")

def mostrar_tabla(matriz):
    columns = []
    index = []
    for i in range(len(matriz)):
        columns.append(f'F{i}')
        index.append(f'C{i}')
    # Redondear los elementos de la matriz a dos decimales
    matriz_redondeada = [[round(valor, 2) for valor in fila] for fila in matriz]

    df = pd.DataFrame(matriz_redondeada, columns=columns, index=index)
    st.table(df.style.format("{:.2f}"))

def trabajar_sistema():
    global probabilities
    global states
    string = st.text_input("Introduce el sistema a trabajar:")
    execution_time = 0
    if st.button("Empezar"):
        # Llamada a la función y almacenamiento de los resultados
        fu_states, pr_states, iState = parse_input_string(string)

        def branch_and_bound_example():
            indices_minimos, minimos_valores = branch_and_bound(list(pr_states), list(fu_states), probabilities, states,
                                                                iState)

        # Medir el tiempo de inicio
        start_time = time.time()

        # Llamar a la función cuya duración quieres medir
        branch_and_bound_example()

        # Medir el tiempo de finalización
        end_time = time.time()

        # Calcular el tiempo total de ejecución
        execution_time = end_time - start_time
        st.success(f"El tiempo de ejecución de branch_and_bound_example fue de {execution_time:.4f} segundos.")
    else:
        crear_grafo()

def editar_matriz():
    global probabilities
    x = st.number_input("Ingrese las coordenadas X (Filas):", value=0)
    y = st.number_input("Ingrese las coordenadas Y (Columnas):", value=0)
    # Mostrar las coordenadas ingresadas
    st.write(f"Coordenadas ingresadas: X = {x}, Y = {y}")

    # Obtener el nuevo valor y validar que sea menor o igual a 1 y mayor o igual a 0
    new_key = str(uuid.uuid4()) #Genera una clave unica para new
    new = st.number_input("Ingrese el nuevo valor para las coordenadas ingresadas:")

    if st.button("Actualizar Matriz"):
        if new >= 0 and new <= 1:
            if x != 0 and y != 0:
                nueva_matriz = []
                i = 0
                for filas in probabilities:
                    i += 1
                    fila = []
                    j = 0
                    for elemento in filas:
                        j += 1
                        if i == x and j == y:
                            fila.append(round(new,2))
                        else:
                            fila.append(round(elemento,2))
                    nueva_matriz.append(fila)
                print(nueva_matriz)
                probabilities = nueva_matriz
            else:
                st.warning("Ingrese valores validos para las coordenadas")
        else:
            st.warning("Recuerde que el valor debe estar entre 0 y 1")

def generate_combinations(present_states, future_states):
    return [(present_state, future_state) for i in range(len(present_states) + 1) for present_state in combinations(present_states, i)
            for j in range(len(future_states) + 1) for future_state in combinations(future_states, j)
            if not (present_state == future_state and present_state != ()) and not (present_state == () and future_state == ()) and not (present_state == tuple(present_states) and future_state == tuple(future_states))]

def generate_remaining_states(combinations_list, complete_present_state, complete_future_state):
    return [(tuple(sorted(set(complete_present_state) - set(present_state))), tuple(sorted(set(complete_future_state) - set(future_state))))
            for present_state, future_state in combinations_list]

def getIndicesToMargenalice(states, state):
    availableIndices = []
    indices = {}
    csValue = ""
    for i in range(len(state)):
        if state[i] != None:
            availableIndices.append(i)
            csValue = str(state[i]) + csValue

    for i in range(len(states)):
        key = ""
        for j in range(len(availableIndices)):
            key += str(states[i][availableIndices[j]])

        indices[key] = indices.get(key) + [i] if indices.get(key) else [i]
    if not csValue:
        return indices, 0
    return indices, int(csValue, 2)

def margenaliceNextState(nsIndices, probabilites):
    nsTransitionTable = [[None] * len(nsIndices) for i in range(len(probabilites))]
    currentColumn = 0
    for indices in nsIndices.values():
        for i in range(len(nsTransitionTable)):
            probability = 0
            for j in range(len(indices)):
                probability += probabilites[i][indices[j]]

            nsTransitionTable[i][currentColumn] = probability

        currentColumn += 1

    return nsTransitionTable

def margenaliceCurrentState(csIndices, nsTransitionTable):
    csTransitionTable = [
        [None] * len(nsTransitionTable[0]) for i in range(len(csIndices))
    ]

    currentRow = 0
    for indices in csIndices.values():
        for i in range(len(csTransitionTable[0])):
            probability = 0
            for j in range(len(indices)):
                probability += nsTransitionTable[indices[j]][i]

            csTransitionTable[currentRow][i] = probability / len(indices)

        currentRow += 1

    return csTransitionTable

def probabilityTransitionTable(probabilities, states, currentState, nextState):
    nsIndices, _ = getIndicesToMargenalice(states, nextState)
    #print(nsIndices)
    csIndices, csValue = getIndicesToMargenalice(states, currentState)
    #print(csIndices, csValue)
    nsTransitionTable = margenaliceNextState(nsIndices, probabilities)
    csTransitionTable = margenaliceCurrentState(csIndices, nsTransitionTable)

    return csTransitionTable[csValue]

def functionTensor(dividedSystem1, dividedSystem2):
    dividedSystem = np.outer(dividedSystem1, dividedSystem2)
    return dividedSystem


def calc_emd(original_distribution, divided_distribution):
    # Convertimos las distribuciones en arrays de numpy
    original_array = np.array(original_distribution)
    divided_array = np.array(divided_distribution)

    # Calculamos el EMD usando la función wasserstein_distance de scipy
    emd = wasserstein_distance(np.arange(len(original_array)), np.arange(len(divided_array)), original_array,
                               divided_array)
    emd /= 2
    emd = round(emd,2)
    return emd

def translate_systems(system_tuple, initialState):
    results = []
    letters = []
    primera = 'A'
    for i in range(cantidad_nodos()):
        letters.append(primera)
        primera = siguiente_letra_mayuscula(primera)

    letters_to_check = letters

    for i, tuple_item in enumerate(system_tuple):

        result_tuple = [0 if letter in tuple_item else None for letter in letters_to_check]

        if i % 2 == 0:
            for index, initial in enumerate(initialState):
                if initial == 1 and letters_to_check[index] in tuple_item:
                    result_tuple[index] = 1

        results.append(tuple(result_tuple))
    return results

def parse_input_string(input_string):
    # Extraer present_states, future_states e iState de la cadena
    match = re.match(r"([A-Za-z-Ø]+)ᵗ⁺¹\|([A-Za-z-Ø]+)ᵗ\s*=\s*(\d+)", input_string)

    if not match:
        raise ValueError("Formato de cadena no válido")

    pr_states = tuple(match.group(1))
    fu_states = tuple(match.group(2))
    iState = [int(digit) for digit in match.group(3)]

    return pr_states, fu_states, iState

def branch_and_bound(present_states, future_states, probabilities, states, initial_state):
    if len(present_states) > len(initial_state):
        st.warning('Asegurese de ingresar correctamente el sistema a trabajar')
        return [],[]
    else:
        combinations = generate_combinations(present_states, future_states)
        remaining_states = generate_remaining_states(combinations, present_states, future_states)
        translated_combinations = [translate_systems(combination, initial_state) for combination in combinations]
        translated_remaining = [translate_systems(complement, initial_state) for complement in remaining_states]

        current_states_combinations, future_states_combinations = zip(*translated_combinations)
        current_states_remaining, future_states_remaining = zip(*translated_remaining)

        combined_states = (present_states, future_states)
        translated_states = translate_systems(combined_states, initial_state)

        result_combination = [probabilityTransitionTable(probabilities, states, list(current), list(next_state))
                              for current, next_state in zip(current_states_combinations, future_states_combinations)]

        result_complement = [probabilityTransitionTable(probabilities, states, list(current), list(next_state))
                             for current, next_state in zip(current_states_remaining, future_states_remaining)]

        divided_distribution = [functionTensor(combination_result, complement_result)
                                for combination_result, complement_result in zip(result_combination, result_complement)]

        original_distribution = probabilityTransitionTable(probabilities, states, translated_states[0], translated_states[1])

        # Verificar si divided_distribution está vacío
        if not divided_distribution:
            print("No hay distribuciones divididas para analizar.")
            return None, None

        # Ordenar divided_distribution por cota inferior ascendente
        divided_distribution = sorted(divided_distribution, key=lambda dist: calculate_lower_bound(original_distribution, dist))

        minimum_value, minimum_index = branch_and_bound_helper(original_distribution, divided_distribution)

        if minimum_index is not None:
            # Invertir el orden de las letras en cada subsistema y ordenar alfabéticamente
            inverted_comb = " | ".join("".join(sorted(c)) if c and c != ('',) else 'Ø' for c in combinations[minimum_index][::-1])
            inverted_comb_comp = " | ".join("".join(sorted(c)) if c and c != ('',) else 'Ø' for c in remaining_states[minimum_index][::-1])

            # Reemplazar el primer ' | ' por 'Ø | ' si el primer subsistema es vacío
            inverted_comb = inverted_comb.replace(' | ', 'Ø | ', 1) if inverted_comb.startswith(' | ') else inverted_comb
            inverted_comb_comp = inverted_comb_comp.replace(' | ', 'Ø | ', 1) if inverted_comb_comp.startswith(' | ') else inverted_comb_comp

            # Imprimir la información con el nuevo formato
            st.success(f"El mínimo valor es: {minimum_value}, y estos subsistemas cumplen con ello: {inverted_comb} y {inverted_comb_comp}.")
            cambiar_grafo(present_states,future_states,initial_state,inverted_comb,inverted_comb_comp)
        return minimum_index, minimum_value

def colear_nodos_gris(element):
    element['style'] = {
        "background": "#808080",
        "width": 75,
        "height": 75,
        "align-items": "center",
        "box-shadow": "rgba(255,255,255,0.25)",
        "text-shadow": "4px 4px 2px rgba(0,0,0,0.3)",
        "font-size": "30px",
        "border-radius": "50%"
    }

def colorear_nodos_amarillo(element):
    element['style'] = {
        "background": "#FFFF00",
        "width": 75,
        "height": 75,
        "align-items": "center",
        "box-shadow": "-2px 10px 100px 3px rgba(255,255,255,0.25)",
        "text-shadow": "4px 4px 2px rgba(0,0,0,0.3)",
        "font-size": "30px",
        "border-radius": "50%"
    }

def primera_particion(resultado1):
    div = False
    destinos1 = []
    origenes1 = []
    for i in range(len(resultado1)):
        if resultado1[i] == '|':
            div = True
        else:
            if resultado1[i] != ' ' and not div:
                destinos1.append(resultado1[i])
            if resultado1[i] != ' ' and div:
                origenes1.append(resultado1[i])
    return destinos1, origenes1

def segunda_particion(resultado2):
    div = False
    destinos2 = []
    origenes2 = []
    for i in range(len(resultado2)):
        if resultado2[i] == '|':
            div = True
        else:
            if resultado2[i] != ' ' and not div:
                destinos2.append(resultado2[i])
            if resultado2[i] != ' ' and div:
                origenes2.append(resultado2[i])
    return destinos2,origenes2

def get_element_by_label(grafo, label):
    for element in grafo:
        if 'data' in element:
            if element['data']['label'] == label:
                return element

def get_element_by_id(grafo, id):
    for element in grafo:
        if element['id'] == id:
                return element

def cambiar_aristas(resultado1,resultado2,grafo):
    graph = Grafo()
    destinos1, origenes1 = primera_particion(resultado1)
    if 'Ø' not in destinos1 and 'Ø' not in origenes1:
        for i in origenes1:
            for j in destinos1:
                if i != j:
                    graph.add_edge(grafo, get_element_by_label(grafo, i), get_element_by_label(grafo, f"{j}'"), True, 0)

    destinos2, origenes2 = segunda_particion(resultado2)
    if 'Ø' not in destinos2 and 'Ø' not in origenes2:
        for i in origenes2:
            for j in destinos2:
                if i != j:
                    if get_element_by_label(grafo, i) is not None and get_element_by_label(grafo, f"{j}'") is not None:
                        graph.add_edge(grafo, get_element_by_label(grafo, i), get_element_by_label(grafo, f"{j}'"), True, 0)

def cambiar_nodos(presentes, futuros, inicial):
    global graph
    grafo = []
    for element in graph:
        if 'data' in element:
            if element['data']['label'] not in presentes:
                colear_nodos_gris(element)
                if element['data']['label'].endswith("'"):
                    if element['data']['label'][0] in futuros:
                        element['style']['box-shadow'] = "-2px 10px 100px 3px rgba(0, 0, 255, 0.5)"
            else:
                sum = 0
                for presente in presentes:
                    if element['data']['label'] == presente:
                        if inicial[sum] == 1:
                            colorear_nodos_amarillo(element)
                    sum += 1
                element['style']['box-shadow'] = "-2px 10px 100px 3px rgba(255, 0, 0, 0.5)"
            aux = element['linkedTo']
            element['linkedTo'] = []
            grafo.append(element)
    return grafo

def aristas_cortadas(presentes, futuros, grafo):
    graph = Grafo()
    for i in presentes:
        for j in futuros:
            if i != j:
                counter = 0
                origen = {}
                destino = {}
                for element in grafo:
                    if 'data' in element and element['data']['label'] == i:
                        origen = element
                    if 'data' in element and element['data']['label'] == f"{j}'":
                        destino = element
                    if element['id'] == f"edge-{i}-{j}'":
                        counter += 1
                if counter == 0:
                    graph.add_edge(grafo,origen,destino,True,0)
                    element = get_element_by_id(grafo,f"edge-{origen['id']}-{destino['id']}")
                    element['style'] = {'stroke': 'red'}

def cambiar_grafo(presentes, futuros, inicial, resultado1, resultado2):
    grafo = cambiar_nodos(presentes,futuros, inicial)
    cambiar_aristas(resultado1, resultado2, grafo)
    aristas_cortadas(presentes,futuros,grafo)

    flow_styles = {"height": 500, "width": 800}
    react_flow("graph", elements=grafo, flow_styles=flow_styles)


def calculate_lower_bound(original_distribution, divided_dist):
    # Convertir a arreglos de NumPy
    original_distribution = np.array(original_distribution)
    divided_dist = np.array(divided_dist)

    # Aplanar las distribuciones para asegurar formas compatibles
    original_distribution = original_distribution.flatten()
    divided_dist = divided_dist.flatten()

    # Calcular la diferencia absoluta máxima elemento a elemento
    max_diff = np.max(np.abs(original_distribution - divided_dist))
    return max_diff

def branch_and_bound_helper(original_distribution, divided_distribution):
    minimum_value = float('inf')
    minimum_index = -1

    def calculate_upper_bound(original_distribution, divided_dist):
        original_distribution = np.array(original_distribution)
        divided_dist = np.array(divided_dist)

        original_distribution = original_distribution.flatten()
        divided_dist = divided_dist.flatten()

        max_diff = np.max(np.abs(original_distribution - divided_dist))

        return max_diff

    def branch_and_bound_helper(original_distribution, divided_distribution):
        minimum_value = float('inf')
        minimum_index = -1

    def branch(distributions, original_distribution_copy, current_index, current_emd):
        nonlocal minimum_value, minimum_index

        if current_index == len(distributions):
            return

        distribution = distributions[current_index]
        result_emd = calc_emd(original_distribution_copy, distribution)

        # Actualizar el mínimo si encontramos una menor diferencia
        if result_emd < minimum_value:
            minimum_value = result_emd
            minimum_index = current_index

        # Podar si ya encontramos una diferencia de 0
        if result_emd == 0:
            return

        upper_bound = calculate_upper_bound(original_distribution_copy, distributions[current_index])

        # Podar si el límite superior es mayor que el mínimo actual
        if upper_bound < minimum_value:
            return

        branch(distributions, original_distribution_copy, current_index + 1, upper_bound)

    distributions = [divided_dist.flatten().tolist() for divided_dist in divided_distribution]
    original_distribution_copy = np.copy(original_distribution)
    branch(distributions, original_distribution_copy, 0, 0)

    return minimum_value, minimum_index

def siguiente_letra_mayuscula(letra):
    if (letra == 'Z'):
        return 'A'
    return chr(ord(letra) + 1)

def cantidad_nodos():
    global probabilities
    l = len(probabilities)
    cant = 0
    while(l != 1):
        l = l/2
        cant += 1
    return cant

def agregar_nodos():
    grafo = Grafo()
    global graph

    nombre = 'A'
    for i in range(cantidad_nodos()):
        if i == 0:
            grafo.add_node(graph, nombre, nombre, 150, 70)
        else:
            nombre = siguiente_letra_mayuscula(nombre)
            grafo.add_node(graph, nombre, nombre, 150, (i * 150) + 70)

    nombre = 'A'
    for i in range(cantidad_nodos()):
        if i == 0:
            grafo.add_node(graph, f'{nombre}2', f"{nombre}'", 450, 70)
        else:
            nombre = siguiente_letra_mayuscula(nombre)
            grafo.add_node(graph, f'{nombre}2', f"{nombre}'", 450, (i * 150) + 70)

def agregar_conexiones():
    grafo = Grafo()
    global graph
    for element in graph:
        for element2 in graph:
            if 'data' in element and not element['data']['label'].endswith("'"):
                if 'data' in element2 and element2['data']['label'].endswith("'"):
                    if element['data']['label'][0] != element2['data']['label'][0]:
                        graph = grafo.add_edge(graph,element,element2,True,0)

def crear_grafo():
    global graph
    agregar_nodos()
    agregar_conexiones()
    flow_styles = {"height": 8000, "width": 800}
    react_flow("graph", elements=graph, flow_styles=flow_styles)
