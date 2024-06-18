import uuid
import pandas as pd
import streamlit as st
import numpy as np
import re
import math

from scipy.stats import wasserstein_distance
from streamlit_react_flow import react_flow
from backend.models.graph import Grafo

'''probabilities = [
                [1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0],
            ]'''

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

def generar_matriz_binaria(m, n):
    # Calcular la longitud fija de los números binarios
    l = math.ceil(math.log2(m))

    # Generar la matriz de números binarios
    matriz_binaria = []
    for i in range(m):
        # Convertir el índice actual a binario y rellenar con ceros a la izquierda
        binario = bin(i)[2:].zfill(l)
        # Invertir el orden de los dígitos binarios
        binario_inverso = binario[::-1]
        # Convertir cada caracter en un entero y agregar a la fila
        fila = [int(b) for b in binario_inverso[:n]]
        matriz_binaria.append(fila)

    return matriz_binaria

#states = generar_matriz_binaria(probabilities, probabilities[0])



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
    # Crear nombres de columnas e índices adecuados
    columns = [f'F{j}' for j in range(len(matriz[0]))]
    index = [f'C{i}' for i in range(len(matriz))]

    # Redondear los elementos de la matriz a dos decimales
    matriz_redondeada = [[round(valor, 2) for valor in fila] for fila in matriz]

    # Crear el DataFrame con los nombres de columnas e índices adecuados
    df = pd.DataFrame(matriz_redondeada, columns=columns, index=index)

    # Mostrar la tabla en Streamlit con formato adecuado
    st.table(df.style.format("{:.2f}"))


def generar_matriz_binaria(m, n):
    # Calcular la longitud fija de los números binarios
    l = math.ceil(math.log2(m))

    # Generar la matriz de números binarios
    matriz_binaria = []
    for i in range(m):
        # Convertir el índice actual a binario y rellenar con ceros a la izquierda
        binario = bin(i)[2:].zfill(l)
        # Invertir el orden de los dígitos binarios
        binario_inverso = binario[::-1]
        # Convertir cada caracter en un entero y agregar a la fila
        fila = [int(b) for b in binario_inverso[:n]]
        matriz_binaria.append(fila)

    return matriz_binaria
def trabajar_sistema():
    global probabilities
    string = st.text_input("Introduce el sistema a trabajar:")

    if st.button("Empezar"):
        eliminar_grafo()  # Clear the existing graph
        crear_grafo()
        print(f"{len(probabilities), len(probabilities[0])}")

        # Llamada a la función y almacenamiento de los resultados
        ns, cs, cs_value = parse_input_string(string)
        decomposition(ns, cs, cs_value)

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

    if csValue == "":
      return indices, 0

    return indices, int(csValue, 2)

def margenaliceNextState(nsIndices, probabilites):
    nsTransitionTable = [[None] * len(nsIndices) for i in range(len(probabilites))]
    currentColumn = 0
    print(f"esto es nsIndices: {len(nsIndices)}")
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

def probabilityTransitionTable(currentState, nextState, probabilities):
    result = []
    csTransitionTable = []
    csIndices, csValueIndex = getIndicesToMargenalice(states, currentState)
    missingCs = any(state is None for state in currentState)

    if (missingCs):
      for i, state in enumerate(nextState):
        if state is not None:
          newNs = [None] * len(nextState)
          newNs[i] = nextState[i]

          nsIndices, _ = getIndicesToMargenalice(states, newNs)
          nsTransitionTable = margenaliceNextState(nsIndices, probabilities)
          csTransitionTable = margenaliceCurrentState(csIndices, nsTransitionTable)
          csValue = csTransitionTable[csValueIndex]

          if len(result) > 0:
            result = np.kron(result, csValue)
          else:
            result = csValue

      #result = reorder_cross_product(result)


    else:
      nsIndices, _ = getIndicesToMargenalice(states, nextState)
      nsTransitionTable = margenaliceNextState(nsIndices, probabilities)

      csTransitionTable = margenaliceCurrentState(csIndices, nsTransitionTable)
      result = csTransitionTable[csValueIndex]


    return result

def functionTensor(dividedSystem1, dividedSystem2):
    dividedSystem = np.outer(dividedSystem1, dividedSystem2)
    return dividedSystem

def decomposition(ns, cs, cs_value):

    min_emd = None
    best_partitioned_system = None
    best_ns1 = None
    best_cs1 = None
    best_ns2 = None
    best_cs2 = None

    def replace_if_empty(s):
        return 'Ø' if len(s) == 0 else s
    print(f"sistema original: {cs_to_array(cs, cs_value), ns_to_array(ns), probabilities}")
    original_system = probabilityTransitionTable(cs_to_array(cs, cs_value), ns_to_array(ns), probabilities)
    memory = {}
    impresos = set()

    def descomponer(ns, cs, memory):
        if memory.get(cs) is not None and memory.get(cs).get(ns) is not None:
            if any(memory.get(cs).get(ns)):
                return memory.get(cs).get(ns)

        if len(ns) == 1:
            value = probabilityTransitionTable(cs_to_array(cs, cs_value), ns_to_array(ns), probabilities)
            return value

        value = []
        for i in range(0, len(ns)):
            if len(value) > 0:
                cross_product = np.kron(value, descomponer(ns[i], cs, memory))
                value = reorder_cross_product(cross_product)
            else:
                value = np.array(descomponer(ns[i], cs, memory))

                if memory.get(cs) is None:
                    memory[cs] = {}

                memory[cs][ns[i]] = value
        return value

    for lenNs in range(len(ns) + 1):
        for i in range(len(ns) - lenNs + 1):
            j = i + lenNs - 1
            ns1, ns2 = ns[i:j+1], ns[:i] + ns[j+1:]

            for lenCs in range(len(cs) + 1):
                for x in range(len(cs) - lenCs + 1):
                    z = x + lenCs - 1
                    cs1, cs2 = cs[x:z+1], cs[:x] + cs[z+1:]

                    if ns2 == ns and cs2 == cs:
                        continue

                    # Verificar duplicados
                    combinacion_actual = ((ns1, cs1), (ns2, cs2))
                    combinacion_inversa = ((ns2, cs2), (ns1, cs1))

                    if (combinacion_actual not in impresos and combinacion_inversa not in impresos) or (ns1 == ns and ns2 == "" and cs1 == "" and cs2 == ""):
                        arr1 = np.array(descomponer(ns2, cs2, memory))
                        arr2 = np.array(descomponer(ns1, cs1, memory))

                        partitioned_system = []

                        if len(arr1) > 0 and len(arr2) > 0:
                            cross_product = np.kron(arr1, arr2)
                            partitioned_system = reorder_cross_product(cross_product)
                        elif len(arr1) > 0:
                            partitioned_system = arr1
                        elif len(arr2) > 0:
                            partitioned_system = arr2

                        # Calcular la Distancia de Wasserstein (EMD)
                        emd_distance = wasserstein_distance(original_system, partitioned_system)

                        if min_emd is None or emd_distance < min_emd:
                            min_emd = emd_distance
                            best_partitioned_system = partitioned_system
                            best_ns1, best_cs1, best_ns2, best_cs2 = ns1, cs1, ns2, cs2

                        impresos.add(combinacion_actual)
                        impresos.add(combinacion_inversa)

    # Imprimir y graficar la mejor combinación encontrada
    if best_partitioned_system is not None:
        st.success(f"El mejor EMD encontrado es: {min_emd}")
        st.success(f"Mejor combinación: p({replace_if_empty(best_ns2)}ᵗ⁺¹ | {replace_if_empty(best_cs2)}ᵗ) × p({replace_if_empty(best_ns1)}ᵗ⁺¹ | {replace_if_empty(best_cs1)}ᵗ)")
        cambiar_grafo(list(cs), list(ns), cs_value, f"{replace_if_empty(best_ns2)} | {replace_if_empty(best_cs2)}", f"{replace_if_empty(best_ns1)} | {replace_if_empty(best_cs1)}")

def parse_input_string(input_string):
    # Extraer present_states, future_states e iState de la cadena
    match = re.match(r"([A-Za-z-Ø]+)ᵗ⁺¹\|([A-Za-z-Ø]+)ᵗ\s*=\s*(\d+)", input_string)

    if not match:
        raise ValueError("Formato de cadena no válido")

    pr_states = match.group(1)
    fu_states = match.group(2)
    iState = [int(digit) for digit in match.group(3)]
    return pr_states, fu_states, iState

def reorder_cross_product(cross_product):
  len_cross = len(cross_product)

  if (len_cross == 4):
    new_order = [0, 2, 1, 3]
    return cross_product[new_order]

  elif (len_cross == 8):
    new_order = [0, 1, 2, 3, 4, 6, 5, 7]
    return cross_product[new_order]

  return cross_product

def ns_to_array(letras):
    ns_arr = [0] * len(letras)
    print(f"esto es ns to array {ns_arr} y tambien letras len: {len(letras)} y letras: {letras}")
    return ns_arr

def cs_to_array(cs, cs_value):
    # Crear un nuevo arreglo con None en las posiciones especificadas por cs
    cs_arr = [cs_value[i] if chr(65 + i) in cs else None for i in range(len(cs_value))]

    return cs_arr

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
                        element['style']['box-shadow'] = "-2px 10px 80px 10px rgba(0, 0, 255, 1)"
            else:
                sum = 0
                for presente in presentes:
                    if element['data']['label'] == presente:
                        if inicial[sum] == 1:
                            colorear_nodos_amarillo(element)
                    sum += 1
                element['style']['box-shadow'] = "-2px 10px 80px 10px rgba(255, 0, 0, 1)"
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

#Esto recibe de entrada de datos, ejemplo:
#presentes, futuros, inicial, resultado1, resultado2
#['A', 'B', 'C'], ['A', 'B', 'C'], [1, 0, 0], A | Ø, BC | ABC
def cambiar_grafo(presentes, futuros, inicial, resultado1, resultado2):
    grafo = cambiar_nodos(presentes,futuros, inicial)
    cambiar_aristas(resultado1, resultado2, grafo)
    aristas_cortadas(presentes,futuros,grafo)

    flow_styles = {"height": 500, "width": 800}
    react_flow("graph", elements=grafo, flow_styles=flow_styles)

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

def eliminar_grafo():
    global graph
    graph = []