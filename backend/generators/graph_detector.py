import random
import streamlit as st
from streamlit_react_flow import react_flow
from collections import deque
from backend.models.graph import Elements
from itertools import combinations as comb

def procesar_entrada(datos):
   grafo = []
   for elemento in datos:
       nodo = {}
       if 'id' in elemento and 'data' in elemento and 'label' in elemento['data']:
           nodo['id'] = str(elemento['id'])
           nodo['type'] = 'default'
           nodo['style'] = {
               'background': '#fff',
               'width': 75,
               'height': 75,
               'align-items': 'center',
               'box-shadow': '-2px 10px 100px 3px rgba(255,255,255,0.25)',
               'text-shadow': '4px 4px 2px rgba(0,0,0,0.3)',
               'font-size': '30px',
               'border-radius': '50%'
           }
           nodo['data'] = {'label': elemento['data']['label']}
           nodo['position'] = {'x': elemento['position']['x'], 'y': elemento['position']['y']}
           nodo['linkedTo'] = [{'nodeId': enlace['nodeId'], 'weight': enlace['weight']} for enlace in elemento.get('linkedTo', [])]
           grafo.append(nodo)
   return grafo


def detectar_bipartito(datos):
   st.subheader("Determinar si el grafo es bipartito")
   grafo = {}
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
   print(procesar_datos(datos), "lo que devuelve la nueva funcion")
   grafo_ejemplo = procesar_datos(datos)
   subgrafos = g_subgrafos(grafo_ejemplo)

   # Imprimir subgrafos
   for idx, (subgrafo1, subgrafo2) in enumerate(subgrafos, start=1):
       print(f"Subgrafo {idx}:")
       print(subgrafo1)
       print(subgrafo2)
       print()

   return grafo


def procesar_datos(datos):
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

def g_subgrafos(grafo):
    nodos = grafo.keys()

    # Generar todas las combinaciones posibles de nodos en dos conjuntos
    combinaciones_validas = []
    for i in range(1, len(nodos)):
        for conjunto1 in itertools.combinations(nodos, i):
            conjunto1 = set(conjunto1)
            conjunto2 = set(nodos) - conjunto1
            if len(conjunto2) > 0:
                combinaciones_validas.append((conjunto1, conjunto2))

    # Filtrar combinaciones válidas según la suma de nodos
    combinaciones_filtradas = []
    for conjunto1, conjunto2 in combinaciones_validas:
        if len(conjunto1) + len(conjunto2) == len(nodos):
            subgrafo1 = {nodo: grafo[nodo] for nodo in conjunto1}
            subgrafo2 = {nodo: grafo[nodo] for nodo in conjunto2}
            combinaciones_filtradas.append((subgrafo1, subgrafo2))

    # Convertir cada subgrafo a la misma estructura de datos que grafo_ejemplo
    subgrafos_formateados = []
    for idx, (subgrafo1, subgrafo2) in enumerate(combinaciones_filtradas, start=1):
        subgrafo1_format = {nodo: grafo[nodo] for nodo in subgrafo1}
        subgrafo2_format = {nodo: grafo[nodo] for nodo in subgrafo2}
        subgrafos_formateados.append((subgrafo1_format, subgrafo2_format))

    return subgrafos_formateados

def colorear_bipartito(grafo):
    # Inicializa un diccionario de colores para almacenar los colores de los nodos (0 o 1)
    colores = {}

    # Inicializa una cola para el recorrido BFS
    cola = []

    # Comienza el recorrido BFS desde un nodo arbitrario
    nodo_inicial = obtener_nodo_inicial(grafo)
    if nodo_inicial is None:
        return True, {}, []  # Grafo vacío (caso base)

    cola.append(nodo_inicial)
    colores[nodo_inicial] = 0

    grafo_coloreado = []

    while cola:
        nodo_actual = cola.pop(0)
        color_actual = colores[nodo_actual]

    # Agrega el nodo actual al grafo coloreado
        nodo_coloreado = crear_nodo_coloreado(nodo_actual, color_actual)
        grafo_coloreado.append(nodo_coloreado)
    # Procesa los vecinos del nodo actual
        for vecino in grafo.get(nodo_actual, []):
            if vecino not in colores:
                # Asigna el color opuesto al vecino
                colores[vecino] = 1 - color_actual
                cola.append(vecino)
            elif colores[vecino] == color_actual:
                # Si el vecino tiene el mismo color que el nodo actual, el grafo no es bipartito
                return False, None, []

            # Agrega la conexión entre el nodo actual y el vecino al grafo coloreado
            enlace = crear_enlace(nodo_actual, vecino)
            grafo_coloreado.append(enlace)

            # Agrega el nodo vecino a la lista de nodos conectados del nodo actual
            nodo_coloreado["linkedTo"].append({"nodeId": str(vecino), "weight": 1})

    return True, colores, grafo_coloreado

def obtener_nodo_inicial(grafo):
    for nodo, conexiones in grafo.items():
        if conexiones:
            return nodo
    return None

def crear_nodo_coloreado(nodo, color):
    return {
        "id": str(nodo),
        "type": "default",
        "data": {"label": f"{str(nodo)}"},
        "style": {
            "background": "blue" if color == 0 else "red",
            "width": 75,
            "height": 75,
            "align-items": "center",
            "box-shadow": "-2px 10px 100px 3px rgba(255,255,255,0.25)",
            "text-shadow": "4px 4px 2px rgba(0,0,0,0.3)",
            "font-size": "30px",
            "border-radius": "50%"
        },
        "position": {"x": random.randint(100, 400), "y": random.randint(100, 200)},
        "linkedTo": []
    }


def crear_enlace(nodo1, nodo2):
    return {
        "id": f"edge-{nodo1}-{nodo2}",
        "source": str(nodo1),
        "target": str(nodo2),
        "animated": True
    }

def componentes_conexas_bipartito(grafo):
    def es_bipartito_y_componente(subgrafo):
        es_bipartito, colores, grafo = colorear_bipartito(subgrafo)
        if not es_bipartito:
            return False, set()
        return True, set(colores.keys()), grafo

    print(grafo, "esto es grafo bipártito")
    graph = []
    visitados_global = set()
    componentes = []
    es_bipartito_global = True

    for nodo in grafo:
        if nodo not in visitados_global:
            subgrafo = {n: grafo[n] for n in grafo if n not in visitados_global}
            es_bipartito, componente, graph2 = es_bipartito_y_componente(subgrafo)
            for element in graph2:
                if element not in graph:
                    graph.append(element)
            if not es_bipartito:
                es_bipartito_global = False
                break
            componentes.append(componente)
            visitados_global.update(componente)

    if not es_bipartito_global:
        st.error("El grafo no es bipartito.")
        return

    # Fusionar componentes que están conectadas entre sí
    for i in range(len(componentes)):
        for j in range(i + 1, len(componentes)):
            if not componentes[i].isdisjoint(componentes[j]):
                componentes[i].update(componentes[j])
    update = True
    for nodo, conexiones in grafo.items():
        if not conexiones:
            for nodo2, conexiones in grafo.items():
                if nodo in conexiones:
                    update = False
            if update:
                componentes.append({nodo})

    # Eliminar componentes vacías y devolver las componentes conexas
    componentes_conexas = [c for c in componentes if c]
    print("componentes conexas: ", componentes_conexas)
    num_componentes_conexas = len(componentes_conexas)

    if num_componentes_conexas == 0:
        st.error("El grafo no es bipartito o no se ha cargado el archivo.")
    else:
        st.success(
            f"El grafo es bipartito y tiene {num_componentes_conexas} {'componente' if num_componentes_conexas == 1 else 'componentes'} conexas: {componentes_conexas}")
        flow_styles = {"height": 500, "width": 800}
        react_flow("graph", elements=graph, flow_styles=flow_styles)
        return
