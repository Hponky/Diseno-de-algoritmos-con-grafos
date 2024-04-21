import random
import streamlit as st
from streamlit_react_flow import react_flow
from collections import deque
from backend.models.graph import Elements
import itertools

def grafo_formateado(datos):
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
        "position": {"x": 200 if color_actual == 0 else 400, "y": sumador0 if color_actual == 0 else sumador1},
        # Define las coordenadas según sea necesario
        "linkedTo": []  # Inicializa la lista de nodos conectados
    }
    return nodo_coloreado, sumador0, sumador1

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

def min_edge_removal_cost_bipartite_subgraphs(datos):
    print(grafo_formateado_con_pesos(datos), "lo que devuelve la nueva funcion")
    grafo_ejemplo = grafo_formateado_con_pesos(datos)
    subgrafos, resultados = generar_subgrafos(grafo_ejemplo)
    # Llamar a la función para encontrar la combinación con la menor pérdida de peso
    combinacion_minima, resultado_minimo = encontrar_combinacion_minima(subgrafos, resultados)
    print("Combinación con la menor pérdida de peso:")
    print(combinacion_minima)
    print("Resultado mínimo:", resultado_minimo)

def generar_subgrafos(grafo):
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

    # Calcular el resultado para cada combinación
    resultados_combinaciones = []
    for subgrafo1, subgrafo2 in subgrafos_formateados:
        resultado_combinacion = calcular_resultado_combinacion(subgrafo1, subgrafo2, grafo)
        resultados_combinaciones.append(resultado_combinacion)

    # Devolver las combinaciones de subgrafos y sus resultados correspondientes
    return subgrafos_formateados, resultados_combinaciones

def calcular_resultado_combinacion(subgrafo1, subgrafo2, grafo_original):
    # Hacer una copia profunda del grafo original para evitar modificar el original
    grafo_modificado = {nodo: conexiones.copy() for nodo, conexiones in grafo_original.items()}

    # Inicializar el resultado
    resultado = 0

    # Diccionario para almacenar los pesos de las conexiones eliminadas por nodo destino
    pesos_eliminados_por_nodo = {}

    # Recorrer las conexiones del subgrafo1
    for nodo, conexiones in subgrafo1.items():
        for nodo_destino, peso in conexiones.items():
            # Verificar si el nodo destino está en el subgrafo2
            if nodo_destino in subgrafo2:
                # Si es la primera conexión hacia este nodo, guardar su peso
                if nodo_destino not in pesos_eliminados_por_nodo:
                    pesos_eliminados_por_nodo[nodo_destino] = [peso]
                else:
                    pesos_eliminados_por_nodo[nodo_destino].append(peso)
                # Eliminar la conexión del grafo modificado
                del grafo_modificado[nodo][nodo_destino]

    # Recorrer las conexiones del subgrafo2
    for nodo, conexiones in subgrafo2.items():
        for nodo_destino, peso in conexiones.items():
            # Verificar si el nodo destino está en el subgrafo1
            if nodo_destino in subgrafo1:
                # Si es la primera conexión hacia este nodo, guardar su peso
                if nodo_destino not in pesos_eliminados_por_nodo:
                    pesos_eliminados_por_nodo[nodo_destino] = [peso]
                else:
                    pesos_eliminados_por_nodo[nodo_destino].append(peso)
                # Eliminar la conexión del grafo modificado
                del grafo_modificado[nodo][nodo_destino]

    # Calcular el resultado para cada nodo destino
    for nodo_destino, pesos in pesos_eliminados_por_nodo.items():
        # Obtener el peso máximo y la suma de todos los pesos
        peso_maximo = max(pesos)
        suma_pesos = sum(pesos)
        # Calcular el resultado como un valor aleatorio entre el peso máximo y la suma de todos los pesos
        resultado += random.uniform(peso_maximo, suma_pesos)

    return resultado

def encontrar_combinacion_minima(subgrafos, resultados):
    # Inicializamos las variables para almacenar la combinación mínima y su resultado
    combinacion_minima = None
    resultado_minimo = float('inf')  # Inicializamos con un valor infinito

    # Iteramos sobre cada combinación y su resultado
    for idx, (subgrafo1, subgrafo2) in enumerate(subgrafos, start=1):
        resultado = resultados[idx - 1]
        # Si el resultado actual es menor que el mínimo registrado, actualizamos la combinación mínima
        if resultado < resultado_minimo:
            resultado_minimo = resultado
            combinacion_minima = (subgrafo1, subgrafo2)

    # Retornamos la combinación mínima y su resultado
    return combinacion_minima, resultado_minimo