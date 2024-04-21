import random
import streamlit as st
from streamlit_react_flow import react_flow
from collections import deque
from backend.models.graph import Elements

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
   return grafo

def colorear_nodo(nodo_actual, color_actual):
    nodo_coloreado = {
        "id": str(nodo_actual),
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
        "position": {"x": random.randint(100, 400), "y": random.randint(100, 200)},
        # Define las coordenadas según sea necesario
        "linkedTo": []  # Inicializa la lista de nodos conectados
    }
    return nodo_coloreado

def arista_coloreado(nodo_actual, vecino):
    enlace = {
        "id": f"edge-{nodo_actual}-{vecino}",
        "source": str(nodo_actual),
        "target": str(vecino),
        "animated": True
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
                    color[nodo] = 0
            if not conexiones:
                color[nodo] = 1

    print(color, "coloooooor")
    return color

def definir_componentes(grafo):
    aislado = True
    componentes = []
    componente = set()
    visitados = []
    for nodo, conexiones in grafo.items():
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
    # Se inicializa el grafo
    graph = []

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
        for nodo, color in colores.items():
            nodo_coloreado = colorear_nodo(nodo,color)
            for nodo2, conexiones in grafo.items():
                if nodo == nodo2:
                    for con in conexiones:
                        arista_lista(nodo_coloreado,con)

            graph.append(nodo_coloreado)

        # Graficar aristas
        for nodo, conexiones in grafo.items():
            for con in conexiones:
                arista = arista_coloreado(nodo,con)
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