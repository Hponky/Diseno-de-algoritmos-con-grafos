from backend.models.graph import Grafo
from streamlit_react_flow import react_flow
from backend.utils.probability import *

graph = []

def cambiar_grafo(presentes, futuros, inicial, resultado1, resultado2):
    grafo = cambiar_nodos(presentes, futuros, inicial)
    cambiar_aristas(resultado1, resultado2, grafo)
    aristas_cortadas(presentes, futuros, grafo)
    flow_styles = {"height": 500, "width": 800}
    react_flow("graph", elements=grafo, flow_styles=flow_styles)

def agregar_nodos(cantidad_nodos):
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

def agregar_conexiones():
    grafo = Grafo()
    global graph
    for element in graph:
        for element2 in graph:
            if 'data' in element and not element['data']['label'].endswith("'"):
                if 'data' in element2 and element2['data']['label'].endswith("'"):
                    if element['data']['label'][0] != element2['data']['label'][0]:
                        graph = grafo.add_edge(graph,element,element2,True,0)


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

def siguiente_letra_mayuscula(letra):
    if letra == 'Z':
        return 'A'
    return chr(ord(letra) + 1)
