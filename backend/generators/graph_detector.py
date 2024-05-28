import random
import streamlit as st
from streamlit_react_flow import react_flow
from collections import deque
from backend.models.graph import Grafo
import itertools
import numpy as np
from scipy.stats import wasserstein_distance

def grafo_formateado(datos):
   grafo = {}
   graph = Grafo()

   for elemento in datos:
       if 'data' in elemento and 'label' in elemento['data']:
           nodo = elemento['data']['label']
           grafo[nodo] = []
           if 'linkedTo' in elemento:
               for adyacente in elemento['linkedTo']:
                   if 'nodeId' in adyacente:
                       for otro_elemento in datos:
                           if 'id' in otro_elemento and str(otro_elemento['id']) == str(adyacente['nodeId']):
                               if 'data' in otro_elemento and 'label' in otro_elemento['data']:
                                   nodo_adyacente = otro_elemento['data']['label']
                                   grafo[nodo].append(nodo_adyacente)
                                   break
   for elemento in datos:
       if 'source' in elemento and 'target' in elemento:
           if elemento['animated'] == False:
               for nodo, conexiones in grafo.items():
                   if nodo == graph.get_element_label_by_id(elemento['source']):
                       grafo[nodo].append(graph.get_element_label_by_id(elemento['target']))
                   if nodo == graph.get_element_label_by_id(elemento['target']):
                       grafo[nodo].append(graph.get_element_label_by_id(elemento['source']))

   return grafo

def grafo_formateado_con_pesos(datos):
    grafo = {}

    for elemento in datos:
        if 'data' in elemento and 'label' in elemento['data']:
            nodo = elemento['data']['label']
            grafo[nodo] = {}
            if 'linkedTo' in elemento:
                for adyacente in elemento['linkedTo']:
                    if 'nodeId' in adyacente and 'weight' in adyacente:
                        for otro_elemento in datos:
                            if 'id' in otro_elemento and str(otro_elemento['id']) == str(adyacente['nodeId']):
                                if 'data' in otro_elemento and 'label' in otro_elemento['data']:
                                    nodo_adyacente = otro_elemento['data']['label']
                                    peso = adyacente['weight']
                                    grafo[nodo][nodo_adyacente] = peso
                                    break
    return grafo

def colorear_nodo(nodo_actual, color_actual, sumador0, sumador1):
    if color_actual == 0:
        sumador0 += 120
    else:
        sumador1 += 120
    nodo_coloreado = {
        "id": str(random.randint(10000,99999)),
        "type": "default",
        "data": {"label": f"{str(nodo_actual)}"},
        "style": {
            "background": "blue" if color_actual == 0 else "red",
            "width": 75,
            "height": 75,
            "align-items": "center",
            "box-shadow": "-2px 10px 100px 3px rgba(255,255,255,0.25)",
            "text-shadow": "4px 4px 2px rgba(0,0,0,0.3)",
            "font-size": "30px",
            "border-radius": "50%"
        },
        "position": {"x": 200 if color_actual == 0 else 400, "y": sumador0 if color_actual == 0 else sumador1},
        # Define las coordenadas según sea necesario
        "linkedTo": []  # Inicializa la lista de nodos conectados
    }
    return nodo_coloreado, sumador0, sumador1

def arista_coloreado(nodo_actual, vecino, animated):
    enlace = {
        "id": f"edge-{nodo_actual}-{vecino}",
        "source": str(nodo_actual),
        "target": str(vecino),
        "animated": animated
    }
    return enlace

def arista_lista(nodo_coloreado, vecino):
    nodo_coloreado["linkedTo"].append(
        {"nodeId": str(vecino), "weight": 1})  # Puedes ajustar el peso según sea necesario

def definir_colores(grafo):
    aislado = True
    visitados = []
    color = {}

    for nodo, conexiones in grafo.items():
        if not conexiones:
            for nodo2, conexiones2 in grafo.items():
                if nodo in conexiones2:
                    aislado = False
                    break
            if aislado:
                visitados.append(nodo)
                color[nodo] = random.randint(0, 1)
        if nodo not in visitados:
            visitados.append(nodo)
            for con in conexiones:
                if con in visitados:
                    color[nodo] = 1 - color[con]
                    break
                else:
                    col = True
                    for nodo2, colour in color.items():
                        if nodo == nodo2:
                            col = False
                    if col:
                        color[nodo] = 0
                        color[con] = 1



            if not conexiones:
                color[nodo] = 1

    return color

def definir_componentes(grafo):
    componentes = []
    componente = set()
    visitados = []
    for nodo, conexiones in grafo.items():
        aislado = True
        if not conexiones:
            for nodo2, conexiones2 in grafo.items():
                if nodo in conexiones2:
                    aislado = False
            if aislado:
                visitados.append(nodo)
                componentes.append({nodo})
        else:
            if nodo not in componente and nodo not in visitados:
                visitados.append(nodo)
                componente.add(nodo)
            for con in conexiones:
                if con not in componente and con not in visitados:
                    visitados.append(con)
                    componente.add(con)
            for nodo2, conexiones2 in grafo.items():
                if nodo2 in componente:
                    for con2 in conexiones2:
                        if con2 not in componente and con2 not in visitados:
                            visitados.append(con2)
                            componente.add(con2)
                else:
                    for con2 in conexiones2:
                        if con2 in componente:
                            for con3 in conexiones2:
                                if con3 not in componente:
                                    visitados.append(con3)
                                    componente.add(con3)
                            break

            for nodo3, conexiones3 in grafo.items():
                for con in conexiones3:
                    if con in componente:
                        visitados.append(nodo3)
                        componente.add(nodo3)
        if componente:
            if componente not in componentes:
                componentes.append(componente)
            if len(componente) == len(grafo):
                break
            else:
                componente = set()

    return componentes

def es_bipartito_y_componente(colores, grafo):
    for nodo, conexiones in grafo.items():
        for nodo_color, color in colores.items():
            if nodo == nodo_color:
                for con in conexiones:
                    if color == colores[con]:
                        return False
    return True


def componentes_conexas_bipartito(grafo):
    g = Grafo()
    # Se inicializa el grafo
    graph = []
    print(grafo, "grafoooo")
    # Se definen las componentes del grafo
    componentes_conexas = definir_componentes(grafo)

    # Se definen los colores del grafo
    colores = definir_colores(grafo)

    # Es bipartito ¿?
    if not es_bipartito_y_componente(colores,grafo):
        st.error("El grafo no es bipartito.")
        return
    # Continuar si el grafo es bipartito
    else:
        # Colorear los nodos del color determinado
        sumador_color0 = 0
        sumador_color1 = 0
        for nodo, color in colores.items():
            nodo_coloreado, sumador_color0, sumador_color1 = colorear_nodo(nodo,color,sumador_color0, sumador_color1)
            for nodo2, conexiones in grafo.items():
                if nodo == nodo2:
                    for con in conexiones:
                        arista_lista(nodo_coloreado,con)

            graph.append(nodo_coloreado)

        # Graficar aristas
        for nodo, conexiones in grafo.items():
            for con in conexiones:
                conexion1 = []
                conexion2 = []
                if f'{nodo},{con}' in g.get_nodos_no_dirigidos() or f'{con},{nodo}' in g.get_nodos_no_dirigidos():
                    for nodo2, conexiones2 in grafo.items():
                        if nodo2 == con:
                            count = 0
                            for con2 in conexiones2:
                                if con2 != nodo or count != 0:
                                    conexion1.append(con2)
                                else:
                                    count += 1

                    g.add_edge(graph,g.get_element_by_label(graph,nodo),g.get_element_by_label(graph,con),False,0)

                    grafo[con] = conexion1

                    for nodo2, conexiones2 in grafo.items():
                        if nodo2 == nodo:
                            conexion = []
                            count = 0
                            for con2 in conexiones2:
                                if con2 != con or count != 0:
                                    conexion2.append(con2)
                                else:
                                    count += 1

                    g.add_edge(graph,g.get_element_by_label(graph,con),g.get_element_by_label(graph,nodo),False,0)

                    grafo[nodo] = conexion2
                else:
                    n = g.get_element_by_label(graph, nodo)
                    c = g.get_element_by_label(graph, con)
                    arista = arista_coloreado(n['id'], c['id'], True)
                    graph.append(arista)

        num_componentes_conexas = len(componentes_conexas)

        if num_componentes_conexas == 0:
            st.error("El grafo no es bipartito o no se ha cargado el archivo.")
        else:
            st.success(
                f"El grafo es bipartito y tiene {num_componentes_conexas} {'componente' if num_componentes_conexas == 1 else 'componentes'} conexas: {componentes_conexas}")
            flow_styles = {"height": 500, "width": 800}
            react_flow("graph", elements=graph, flow_styles=flow_styles)
            return

def min_edge_removal_cost_bipartite_subgraphs(datos):
    grafo_ejemplo = grafo_formateado_con_pesos(datos)
    combinacion_minima, resultado_minimo = encontrar_resultado_minimo(grafo_ejemplo)
    st.success(f"Combinación con la menor pérdida de peso: {combinacion_minima}")
    st.success(f"Resultado mínimo: {resultado_minimo}")

def encontrar_resultado_minimo(grafo):
    nodos = list(grafo.keys())
    n = len(nodos)

    # Inicializar la tabla de memoización para almacenar los resultados de los subproblemas
    dp = {}

    # Inicializar variables para almacenar la combinación de subgrafos con el resultado mínimo
    combinacion_minima = None
    resultado_minimo = float('inf')

    # Calcular el resultado mínimo utilizando programación dinámica
    for i in range(1, n):
        for conjunto1 in itertools.combinations(nodos, i):
            conjunto1 = set(conjunto1)
            conjunto2 = set(nodos) - conjunto1
            subgrafo1 = {nodo: grafo[nodo] for nodo in conjunto1}
            subgrafo2 = {nodo: grafo[nodo] for nodo in conjunto2}
            resultado = calcular_resultado_combinacion(subgrafo1, subgrafo2, grafo, dp)
            if resultado < resultado_minimo:
                resultado_minimo = resultado
                combinacion_minima = (list(conjunto1), list(conjunto2))

    return combinacion_minima, resultado_minimo


def calcular_resultado_combinacion(subgrafo1, subgrafo2, grafo_original, dp):
    # Verificar si ya hemos calculado el resultado para esta combinación de subgrafos
    if (frozenset(subgrafo1.keys()), frozenset(subgrafo2.keys())) in dp:
        return dp[(frozenset(subgrafo1.keys()), frozenset(subgrafo2.keys()))]

    # Calcular el resultado para la combinación de subgrafos
    resultado = 0

    # Recorrer las conexiones del subgrafo1
    for nodo, conexiones in subgrafo1.items():
        for nodo_destino, peso in conexiones.items():
            # Verificar si el nodo destino está en el subgrafo2
            if nodo_destino in subgrafo2:
                resultado += int(peso)

    # Recorrer las conexiones del subgrafo2
    for nodo, conexiones in subgrafo2.items():
        for nodo_destino, peso in conexiones.items():
            # Verificar si el nodo destino está en el subgrafo1
            if nodo_destino in subgrafo1:
                resultado += int(peso)

    # Almacenar el resultado en la tabla de memoización
    dp[(frozenset(subgrafo1.keys()), frozenset(subgrafo2.keys()))] = resultado

    return resultado

def generar_divisiones_sistema_original(sistema_original):
    nodos = list(sistema_original.keys())
    n = len(nodos)
    divisiones = []

    # Generar todas las combinaciones posibles de subconjuntos de nodos
    for i in range(1, n):
        for subconjunto_nodos in itertools.combinations(nodos, i):
            subconjunto_nodos = set(subconjunto_nodos)
            divisiones.append(subconjunto_nodos)

    return divisiones


def calcular_diferencia_informacion(sistema_original, sistema_dividido):
    # Convertir las distribuciones de probabilidad en matrices numpy
    original_matrix = np.array([sistema_original[nodo] for nodo in sistema_original])
    dividido_matrix = np.array([sistema_dividido[nodo] for nodo in sistema_dividido])

    # Calcular la diferencia de información utilizando la distancia de Wasserstein (EMD)
    diferencia_informacion = wasserstein_distance(original_matrix.flatten(), dividido_matrix.flatten())

    return diferencia_informacion


def encontrar_division_optima(sistema_original):
    divisiones = generar_divisiones_sistema_original(sistema_original)
    mejor_division = None
    mejor_diferencia_informacion = float('inf')

    for division in divisiones:
        sistema_dividido = obtener_sistema_dividido(sistema_original, division)
        diferencia_informacion = calcular_diferencia_informacion(sistema_original, sistema_dividido)
        if diferencia_informacion < mejor_diferencia_informacion:
            mejor_division = division
            mejor_diferencia_informacion = diferencia_informacion

    return mejor_division


def obtener_sistema_dividido(sistema_original, division):
    sistema_dividido = {}
    for nodo, distribucion in sistema_original.items():
        if nodo in division:
            sistema_dividido[nodo] = distribucion

    return sistema_dividido
