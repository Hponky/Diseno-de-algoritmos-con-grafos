from copy import deepcopy

from frontend.components.menu.sub_menu_1.sub_menu_2.sub_menu_2 import *

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
    print(grafo, "grafo formateado con peso")
    return grafo

def eliminar_pesos(grafo_con_pesos):
    grafo_sin_pesos = {}

    for nodo, adyacentes in grafo_con_pesos.items():
        grafo_sin_pesos[nodo] = list(adyacentes.keys())

    return grafo_sin_pesos

def convert_to_original_format(subgrafos):
    original_format = []
    graph_data = {}

    # Combinar los subgrafos en un solo diccionario
    for subgrafo in subgrafos:
        graph_data.update(subgrafo)

    for node_label, connections in graph_data.items():
        node_data = {
            'id': str(hash(node_label)),
            'type': 'default',
            'style': {
                'background': '#fff',
                'width': 75,
                'height': 75,
                'align-items': 'center',
                'box-shadow': '-2px 10px 100px 3px rgba(255,255,255,0.25)',
                'text-shadow': '4px 4px 2px rgba(0,0,0,0.3)',
                'font-size': '30px',
                'border-radius': '50%'
            },
            'data': {
                'label': node_label,
                'value': 0
            },
            'position': {
                'x': 50 + 300 * ('A' in node_label),
                'y': 50 + 100 * ('B' in node_label) + 200 * ('C' in node_label)
            },
            'linkedTo': []
        }

        for neighbor, weight in connections.items():
            node_data['linkedTo'].append({
                'nodeId': str(hash(neighbor)),
                'weight': weight
            })

        original_format.append(node_data)

        for neighbor, weight in connections.items():
            edge_data = {
                'id': f'edge-{hash(node_label)}-{hash(neighbor)}',
                'source': str(hash(node_label)),
                'target': str(hash(neighbor)),
                'animated': True
            }
            original_format.append(edge_data)

    flow_styles = {"height": 500, "width": 800}
    react_flow("graph", elements=original_format, flow_styles=flow_styles)
    return original_format

def min_edge_removal_cost_bipartite_subgraphs(datos):
    if not datos:
        st.error("No hay datos para procesar.")
        return None

    grafo_ejemplo = grafo_formateado_con_pesos(datos)

    if not grafo_ejemplo:
        st.error("No se pudo generar un grafo a partir de los datos proporcionados.")
        return None

    cota_global = calcular_cota_superior(grafo_ejemplo)
    combinacion_minima, resultado_minimo, combinacion_minima_original = generar_subgrafos(grafo_ejemplo, cota_global)

    st.success(f"Combinación con la menor pérdida de peso: {combinacion_minima_original}")
    st.success(f"Eliminación de las aristas: {combinacion_minima}")
    st.success(f"Resultado mínimo: {resultado_minimo}")
    convert_to_original_format(combinacion_minima)

def calcular_cota_inferior(grafo, conjunto1, conjunto2, nivel):
    cota_inferior = 0
    valor_estimado = 0
    nodos_restantes = set(grafo.keys()) - conjunto1 - conjunto2

    # Calcular el peso mínimo que se perderá debido a las conexiones entre los conjuntos
    for nodo1 in conjunto1:
       for nodo2 in conjunto2:
           if nodo2 in grafo[nodo1]:
               cota_inferior += grafo[nodo1][nodo2]
               valor_estimado += grafo[nodo1][nodo2]

    # Estimar el peso adicional que se perderá en los niveles restantes
    for nodo in nodos_restantes:
       if grafo[nodo]:
           conexiones_minimas = min(grafo[nodo].values())
           cota_inferior += conexiones_minimas * (len(conjunto1) + len(conjunto2))
           valor_estimado += sum(grafo[nodo].values())

    return cota_inferior, valor_estimado

def calcular_cota_superior(grafo):
    cota_superior = 0
    for nodo, conexiones in grafo.items():
       for nodo_destino, peso in conexiones.items():
           cota_superior += peso
    return cota_superior / 2  # Dividir por 2 porque cada arista se cuenta dos veces

def generar_subgrafos(grafo, cota_global):
    nodos = list(grafo.keys())
    combinaciones_validas = []
    mejor_solucion = float('inf')
    mejor_combinacion = None
    mejor_valor_estimado = float('inf')
    mejor_combinacion_sin_modificar = None

    def backtrack(conjunto1, conjunto2, nivel):
        nonlocal mejor_solucion, mejor_combinacion, mejor_valor_estimado, mejor_combinacion_sin_modificar

        if nivel == len(nodos):
            if conjunto1 and conjunto2:
                subgrafo1 = {nodo: grafo[nodo].copy() for nodo in conjunto1}
                subgrafo2 = {nodo: grafo[nodo].copy() for nodo in conjunto2}
                resultado = calcular_resultado_combinacion(subgrafo1, subgrafo2, grafo)
                if resultado < mejor_solucion:
                    mejor_solucion = resultado
                    mejor_combinacion = (eliminar_aristas_entre_conjuntos(subgrafo1, subgrafo2), eliminar_aristas_entre_conjuntos(subgrafo2, subgrafo1))
                    mejor_combinacion_sin_modificar = (subgrafo1, subgrafo2)
                    mejor_valor_estimado = resultado
            return

        cota_inferior, valor_estimado = calcular_cota_inferior(grafo, conjunto1, conjunto2, nivel)

        if cota_inferior >= mejor_solucion or valor_estimado >= mejor_valor_estimado:
            return

        for nodo in nodos[nivel:]:
            if nodo not in conjunto1 and nodo not in conjunto2:
                conjunto1.add(nodo)
                backtrack(conjunto1, conjunto2, nivel + 1)
                conjunto1.remove(nodo)
                conjunto2.add(nodo)
                backtrack(conjunto1, conjunto2, nivel + 1)
                conjunto2.remove(nodo)
                break

    def eliminar_aristas_entre_conjuntos(subgrafo, otro_subgrafo):
        subgrafo_limpio = {nodo: conexiones.copy() for nodo, conexiones in subgrafo.items()}
        for nodo, conexiones in subgrafo.items():
            conexiones_a_eliminar = [nodo_vecino for nodo_vecino in conexiones if nodo_vecino in otro_subgrafo]
            for nodo_vecino in conexiones_a_eliminar:
                del subgrafo_limpio[nodo][nodo_vecino]
        return subgrafo_limpio

    backtrack(set(), set(), 0)
    return mejor_combinacion, mejor_solucion, mejor_combinacion_sin_modificar


def calcular_resultado_combinacion(subgrafo1, subgrafo2, grafo_original):
    grafo_modificado = deepcopy(grafo_original)

    resultado = 0
    pesos_eliminados_por_nodo = {}

    def actualizar_pesos(nodo_destino, peso):
        if nodo_destino not in pesos_eliminados_por_nodo:
            pesos_eliminados_por_nodo[nodo_destino] = [peso]
        else:
            pesos_eliminados_por_nodo[nodo_destino].append(peso)

    def eliminar_conexion(nodo, nodo_destino):
        del grafo_modificado[nodo][nodo_destino]

    for nodo, conexiones in subgrafo1.items():
        for nodo_destino, peso in conexiones.items():
            if nodo_destino in subgrafo2:
                actualizar_pesos(nodo_destino, peso)
                eliminar_conexion(nodo, nodo_destino)

    for nodo, conexiones in subgrafo2.items():
        for nodo_destino, peso in conexiones.items():
            if nodo_destino in subgrafo1:
                actualizar_pesos(nodo_destino, peso)
                eliminar_conexion(nodo, nodo_destino)

    for nodo_destino, pesos in pesos_eliminados_por_nodo.items():
        peso_maximo = max(pesos)
        suma_pesos = sum(pesos)
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