import ast
import streamlit as st
import time
from backend.generators.graph_probability import *
from frontend.components.menu.sub_menu_1.sub_menu_2 import sub_menu_2
from streamlit_react_flow import react_flow
from scipy.stats import wasserstein_distance
from itertools import combinations

# Datos globales
probabilities = []
original = []
states = []
graph = []


def create_distance_matrix(n):
    distance_matrix = np.abs(np.arange(n).reshape(-1, 1) - np.arange(n))
    return distance_matrix


def presente_vacio(elemento, futuro, futuros, dic1, iState, combinations):
    valor1 = []
    global matrices
    global states
    print(elemento)
    letra = futuro[0]
    indice = futuros[letra]
    for i in range(len(matrices)):
        if i == indice:
            valores = [0, 0]
            for matriz in matrices[i]:
                valores[1] += matriz[len(matriz) - 1]
            valores[1] = valores[1] / len(matrices[i])
            valores[0] = 1 - valores[1]
            valor1 = valores
            print(valores, 'valores')
    complemento = combinations[int(len(combinations) - (indice + 1))]
    futuros2 = complemento[1]
    presentes2 = complemento[0]
    aux = {}
    print('futuros: ', futuros, futuros2)
    for clave, valor in futuros.items():
        if clave not in futuros2:
            for clave2, valor2 in dic1.items():
                l = []
                for i in range(len(valor2)):
                    if i != valor:
                        l.append(valor2[i])
                aux[clave2] = l
    # Aux devuelve 0...31 con valor de 1 []
    print(aux, 'aux')
    aux2 = {}
    new_states = convertir_y_cambiar(states)
    for i in range(len(new_states)):
        for clave, valor in futuros.items():
            l = []
            if clave in presentes2:
                l.append(new_states[i][valor])
        aux2[i] = l
    # Aux2 devuelve 0..31 con valores repetidos littleE
    print(aux2, 'aux2')
    aux3 = {}
    for clave, valor in aux2.items():
        l = []
        for clave2, valor2 in aux2.items():
            if valor == valor2:
                l.append(clave2)
        aux3[clave] = l
    # Aux3 devuelve 0...n
    print(aux3, 'aux3')
    # {0: [0,2,3,4], }
    margin = {}
    i = 0
    for clave, valor in aux3.items():
        isin = False
        for cl, val in margin.items():
            if valor == valor:
                isin = True
        if not isin:
            for clave2, valor2 in aux3.items():
                if valor == valor2:
                    margin[i] = valor
                    i += 1

    # {0:[0,0,0],1:[0,1,0],2:[0,0,0]}
    # {0:17, 1:8}


def matriz_original(indice):
    global matrices
    matriz = []
    for elemento in matrices[indice]:
        matriz.append(elemento)
    return matriz


def convertir_y_cambiar(bin_list):
    # Convertir cada cadena binaria a una lista de enteros y cambiar el orden
    result = [[int(bit) for bit in reversed(bin_str)] for bin_str in bin_list]
    return result


def empezar_trabajo(string, execution_time, dic1):
    global states
    estados = []
    pr_states, fu_states, iState = parse_input_string(string)
    presentes, futuros = sistema_original(fu_states, pr_states)
    if len(iState) == len(presentes):
        combinations = generate_combinations(pr_states, fu_states)
        primera = 'A'
        for i in range(len(matrices)):
            estados.append(primera)
            primera = siguiente_letra_mayuscula(primera)
        matriz = matriz_sistema_original(dic1, pr_states, fu_states, futuros, presentes)
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
                complemento = combinations[int(len(combinations) - (indice + 1))]
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
                    i += 1


def trabajar_sistema3(dic1, dic2, matrices):
    global probabilities
    print(dic1, f'\n{dic2}')
    string = st.text_input("Introduce el sistema a trabajar:")
    execution_time = 0
    print("ola")
    if st.button("Empezar"):
        print("Estas son las matrices", matrices)
        matriz_a_llenar = verificar_y_generar_matriz(matrices)
        comb_y_valor_on = verificar_y_obtener_valores_on(matrices)
        actualizar_matriz(matriz_a_llenar, comb_y_valor_on)

        #empezar_trabajo(string, execution_time, dic1)
    else:
        crear_grafo()

def verificar_y_generar_matriz(matrices):
    # Verificar que todas las matrices tienen la misma longitud
    longitud = len(matrices[0])
    for matriz in matrices:
        if len(matriz) != longitud:
            raise ValueError("Todas las matrices deben tener la misma longitud")

    # Imprimir la longitud común
    print(f"Longitud común de las matrices: {longitud}")

    # Generar una matriz de tamaño n x n donde n es la longitud común
    matriz_resultante = [[0 for _ in range(longitud)] for _ in range(longitud)]

    # Imprimir la matriz resultante
    print(matriz_resultante)

    return matriz_resultante


def verificar_y_obtener_valores_on(matrices):
    # Verificar que todas las matrices tienen la misma longitud
    longitud = len(matrices[0])
    for matriz in matrices:
        if len(matriz) != longitud:
            raise ValueError("Todas las matrices deben tener la misma longitud")

    # Imprimir la longitud común
    print(f"Longitud común de las matrices: {longitud}")

    # Determinar el número de matrices
    num_matrices = len(matrices)

    # Crear una lista para almacenar los valores On de cada combinación
    combinaciones_y_valores_on = []

    # Función para convertir una lista binaria a decimal
    def binario_a_decimal(binario):
        return int(''.join(str(int(b)) for b in reversed(binario)), 2)

    # Recorrer cada combinación y extraer el valor On (último índice)
    for i in range(longitud):
        combinacion_binaria = matrices[0][i][
                              :num_matrices]  # Los primeros n elementos representan la combinación binaria
        combinacion_decimal = binario_a_decimal(combinacion_binaria)

        valor_on_binario = [matriz[i][-1] for matriz in
                            matrices]  # Obtener el último índice de cada matriz en la misma combinación
        valor_on_decimal = binario_a_decimal(valor_on_binario)

        combinaciones_y_valores_on.append((combinacion_decimal, valor_on_decimal))
        print(f"Combinación {combinacion_decimal}: Valor On = {valor_on_decimal}")
    print(combinaciones_y_valores_on)
    return combinaciones_y_valores_on

def actualizar_matriz(matriz, combinaciones_y_valores_on):
    for combinacion, valor_on in combinaciones_y_valores_on:
        if combinacion < len(matriz) and valor_on < len(matriz):
            matriz[combinacion][valor_on] = 1
        else:
            print(f"Combinación {combinacion} o valor_on {valor_on} fuera de rango para la matriz")
    for m in matriz:
        print(m)
    return matriz

def measure_execution_time(func, *args):
    """
    Mide el tiempo de ejecución de una función.

    :param func: Función a ejecutar.
    :param args: Argumentos de la función.
    :return: Tiempo de ejecución en segundos.
    """
    start_time = time.time()
    func(*args)
    end_time = time.time()
    return end_time - start_time


def editar_matriz():
    global probabilities
    x = st.number_input("Ingrese las coordenadas X (Filas):", value=0)
    y = st.number_input("Ingrese las coordenadas Y (Columnas):", value=0)
    st.write(f"Coordenadas ingresadas: X = {x}, Y = {y}")
    new_value = st.number_input("Ingrese el nuevo valor para las coordenadas ingresadas:")
    if st.button("Actualizar Matriz"):
        update_matrix(x, y, new_value)


def update_matrix(x, y, new_value):
    """
    Actualiza la matriz de probabilidades con un nuevo valor.

    :param x: Coordenada X.
    :param y: Coordenada Y.
    :param new_value: Nuevo valor.
    """
    global probabilities
    if 0 <= new_value <= 1 and x > 0 and y > 0:
        probabilities = [
            [round(new_value if i == x and j == y else probabilities[i][j], 2) for j in range(len(probabilities[i]))]
            for i in range(len(probabilities))
        ]
    else:
        st.warning("Ingrese valores válidos para las coordenadas y el valor debe estar entre 0 y 1.")


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


def getIndicesToMargenalice(states, state):
    availableIndices = []
    indices = {}
    csValue = ""
    for i in range(len(state)):
        if state[i] != None:
            availableIndices.append(i)
            csValue = str(state[i]) + csValue

    for i in range(len(states)):
        key = "".join(str(states[i][index]) for index in availableIndices)
        indices[key] = indices.get(key, []) + [i]

    return indices, int(csValue, 2) if csValue else 0


def margenaliceNextState(nsIndices, probabilities):
    nsTransitionTable = [[None] * len(nsIndices) for _ in range(len(probabilities))]
    for currentColumn, indices in enumerate(nsIndices.values()):
        for i in range(len(nsTransitionTable)):
            nsTransitionTable[i][currentColumn] = sum(probabilities[i][index] for index in indices)
    return nsTransitionTable


def margenaliceCurrentState(csIndices, nsTransitionTable):
    csTransitionTable = [[None] * len(nsTransitionTable[0]) for _ in range(len(csIndices))]
    for currentRow, indices in enumerate(csIndices.values()):
        for i in range(len(csTransitionTable[0])):
            csTransitionTable[currentRow][i] = sum(nsTransitionTable[index][i] for index in indices) / len(indices)
    return csTransitionTable


def functionTensor(dividedSystem1, dividedSystem2):
    return np.outer(dividedSystem1, dividedSystem2)


def calc_emd(original_distribution, divided_distribution):
    original_array = np.array(original_distribution)
    divided_array = np.array(divided_distribution)
    emd = wasserstein_distance(np.arange(len(original_array)), np.arange(len(divided_array)), original_array,
                               divided_array)
    return round(emd / 2, 2)


def translate_systems(system_tuple, initialState):
    letters = [chr(65 + i) for i in range(cantidad_nodos())]
    results = []
    for i, tuple_item in enumerate(system_tuple):
        result_tuple = [0 if letter in tuple_item else None for letter in letters]
        if i % 2 == 0:
            result_tuple = [1 if initialState[idx] == 1 and letter in tuple_item else val for idx, (letter, val) in
                            enumerate(zip(letters, result_tuple))]
        results.append(tuple(result_tuple))
    return results


def parse_input_string(input_string):
    match = re.match(r"([A-Za-z-Ø]+)ᵗ⁺¹\|([A-Za-z-Ø]+)ᵗ\s*=\s*(\d+)", input_string)
    if not match:
        raise ValueError("Formato de cadena no válido")
    pr_states = tuple(match.group(1))
    fu_states = tuple(match.group(2))
    iState = [int(digit) for digit in match.group(3)]
    return pr_states, fu_states, iState


def primera_particion(resultado1):
    destinos1, origenes1 = [], []
    div = False
    for char in resultado1:
        if char == '|':
            div = True
        elif char != ' ':
            (origenes1 if div else destinos1).append(char)
    return destinos1, origenes1


def segunda_particion(resultado2):
    destinos2, origenes2 = [], []
    div = False
    for char in resultado2:
        if char == '|':
            div = True
        elif char != ' ':
            (origenes2 if div else destinos2).append(char)
    return destinos2, origenes2


def get_element_by_label(grafo, label):
    return next((element for element in grafo if 'data' in element and element['data']['label'] == label), None)


def get_element_by_id(grafo, id):
    return next((element for element in grafo if element['id'] == id), None)


def cambiar_aristas(resultado1, resultado2, grafo):
    graph = Grafo()
    destinos1, origenes1 = primera_particion(resultado1)
    if 'Ø' not in destinos1 and 'Ø' not in origenes1:
        for origen in origenes1:
            for destino in destinos1:
                if origen != destino:
                    graph.add_edge(grafo, get_element_by_label(grafo, origen),
                                   get_element_by_label(grafo, f"{destino}'"), True, 0)
    destinos2, origenes2 = segunda_particion(resultado2)
    if 'Ø' not in destinos2 and 'Ø' not in origenes2:
        for origen in origenes2:
            for destino in destinos2:
                if origen != destino and get_element_by_label(grafo, origen) and get_element_by_label(grafo,
                                                                                                      f"{destino}'"):
                    graph.add_edge(grafo, get_element_by_label(grafo, origen),
                                   get_element_by_label(grafo, f"{destino}'"), True, 0)


def calculate_lower_bound(original_distribution, divided_dist):
    return np.max(np.abs(np.array(original_distribution).flatten() - np.array(divided_dist).flatten()))


def cantidad_nodos():
    return int(len(probabilities))

def agregar_nodos3(cantidad_nodos):
    grafo = Grafo()
    global graph

    nombre = 'A'
    for i in range(cantidad_nodos):
        if i == 0:
            grafo.add_node(graph, nombre, nombre, 150, 70)
        else:
            nombre = siguiente_letra_mayuscula(nombre)
            grafo.add_node(graph, nombre, nombre, 150, (i * 150) + 70)

    nombre = 'A'
    for i in range(cantidad_nodos):
        if i == 0:
            grafo.add_node(graph, f'{nombre}2', f"{nombre}'", 450, 70)
        else:
            nombre = siguiente_letra_mayuscula(nombre)
            grafo.add_node(graph, f'{nombre}2', f"{nombre}'", 450, (i * 150) + 70)

def crear_grafo():
    global graph
    agregar_nodos3(cantidad_nodos())
    agregar_conexiones()
    flow_styles = {"height": 8000, "width": 800}
    react_flow("graph", elements=graph, flow_styles=flow_styles)

def pad_sublists(lista_de_listas):
    max_length = max(len(sublista) for sublista in lista_de_listas)
    for sublista in lista_de_listas:
        if len(sublista) < max_length:
            sublista.extend([0] * (max_length - len(sublista)))
    return lista_de_listas


def string_a_lista_de_listas(string):
    lista = []
    l = []
    for i, j in enumerate(string):  # Corregimos el uso de enumerate
        if i != 0 and i != len(string) - 1:
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


def mostrar_tabla():
    global probabilities
    columns = [f'F{i}' for i in range(len(probabilities))]
    index = [f'C{i}' for i in range(len(probabilities))]
    matriz_redondeada = [[round(valor, 2) for valor in fila] for fila in probabilities]
    df = pd.DataFrame(matriz_redondeada, columns=columns, index=index)
    st.table(df.style.format("{:.2f}"))


def mostrar_tablas(text, letra):
    matriz = string_a_lista_de_listas(text)
    print(matriz)
    st.write(f'Matriz de {letra}:')
    columns = [f'F{i}' for i in range(len(matriz[0]))]
    index = [f'C{i}' for i in range(len(matriz))]
    df = pd.DataFrame(matriz, columns=columns, index=index)
    st.table(df.style.format("{:.2f}"))
    return matriz

def crear_dict_pr(pr_states):
    primera = 'A'
    pr = {}
    j = 0

    while (len(pr_states) != len(pr)):
        if primera in pr_states:
            pr[primera] = j
        j += 1
        primera = siguiente_letra_mayuscula(primera)

    return pr

def siguiente_letra_mayuscula(letra):
    if letra == 'Z':
        return 'A'
    return chr(ord(letra) + 1)

def crear_dict_fu(fu_states):
    primera = 'A'
    fu = {}
    j = 0

    while (len(fu_states) != len(fu)):
        if primera in fu_states:
            fu[primera] = j
        j += 1
        primera = siguiente_letra_mayuscula(primera)

    return fu


def crear_diccionarios(fu_states, pr_states):
    return crear_dict_pr(pr_states), crear_dict_fu(fu_states)


def sistema_original(fu_states, pr_states):
    fu, pr = crear_diccionarios(fu_states, pr_states)
    return pr, fu


def generate_remaining_states(combinations_list, complete_present_state, complete_future_state):
    return [(tuple(sorted(set(complete_present_state) - set(present_state))),
             tuple(sorted(set(complete_future_state) - set(future_state))))
            for present_state, future_state in combinations_list]


def binario_a_decimal(binario_reverso):
    # Reversar la lista para que esté en el orden correcto
    binario_correcto = binario_reverso[::-1]

    # Convertir la lista binaria a una cadena
    binario_str = ''.join(map(str, binario_correcto))

    # Convertir la cadena binaria a un número decimal
    decimal = int(binario_str, 2)

    return decimal


def matriz_sistema_original(estados, fu, pr, futuros, presentes):
    global probabilities
    matriz = []
    for clave_fu, valor_fu in futuros.items():  # {A:0,B:1...}
        if clave_fu not in fu:  # [A,C...]
            for clave, valor in estados.items():  # {0: [0,0,0]...}
                pos = []
                aux1 = []
                aux2 = []
                for i in range(len(valor)):  # [0,0,0,0,0]
                    if i != valor_fu:
                        pos.append(valor[i])  # [0,0,0,0]
                        aux2.append(valor[i])
                    else:
                        aux2.append(1 - valor[i])
                    aux1 = valor[i]

                y1 = binario_a_decimal(aux1)
                y2 = binario_a_decimal(aux2)

                suma = probabilities[clave][y1] + probabilities[clave][y2]

                estado = []
                for i in range(len(estados) / 2):
                    estado.append(0)
                matriz.append(estado)

                matriz[clave][binario_a_decimal(pos)] = suma


def procesar_string(input_string):
    # Eliminar espacios y caracteres innecesarios
    input_string = input_string.strip("")

    # Convertir el string a una lista de listas
    listas = ast.literal_eval(input_string)

    # Extraer los últimos números de cada lista
    ultimos_numeros = [lista[-1] for lista in listas]

    # Calcular la suma de los últimos números
    suma = sum(ultimos_numeros)

    # Dividir la suma por el número de listas
    resultado = suma / len(ultimos_numeros)

    return resultado