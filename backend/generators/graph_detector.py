import random
import streamlit as st


from collections import deque
from backend.models.graph import Elements


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


   return grafo




import random


def colorear_bipartito(grafo):
   # Inicializa un diccionario de colores para almacenar los colores de los nodos (0 o 1)
   color = {}


   # Inicializa una cola para el recorrido BFS
   cola = []
   # Comienza el recorrido BFS desde un nodo arbitrario
   nodo_inicial = ''
   for nodo, conexiones in grafo.items():
       if not conexiones:
           continue
       else:
           nodo_inicial = nodo
           cola.append(nodo_inicial)
           color[nodo_inicial] = 0
           break
   grafo_coloreado = []


   # Recorre la cola hasta que esté vacía
   while cola:
       nodo_actual = cola.pop(0)
       color_actual = color[nodo_actual]


       # Agrega el nodo actual al grafo coloreado
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
           "position": {"x": random.randint(100,400), "y": random.randint(100,200)},  # Define las coordenadas según sea necesario
           "linkedTo": []  # Inicializa la lista de nodos conectados
       }
       grafo_coloreado.append(nodo_coloreado)


       # Procesa los vecinos del nodo actual
       for vecino in grafo.get(nodo_actual, []):
           if vecino not in color:
               # Asigna el color opuesto al vecino
               color[vecino] = 1 - color_actual
               cola.append(vecino)
           elif color[vecino] == color_actual:
               # Si el vecino tiene el mismo color que el nodo actual, el grafo no es bipartito
               return False, None


           # Agrega la conexión entre el nodo actual y el vecino al grafo coloreado
           enlace = {
               "id": f"edge-{nodo_actual}-{vecino}",
               "source": str(nodo_actual),
               "target": str(vecino),
               "animated": True
           }
           grafo_coloreado.append(enlace)


           # Agrega el nodo vecino a la lista de nodos conectados del nodo actual
           nodo_coloreado["linkedTo"].append({"nodeId": str(vecino), "weight": 1})  # Puedes ajustar el peso según sea necesario


   # Agregar nodos con conexiones vacías
   for nodo, conexiones in grafo.items():
       if nodo not in color:
           colour = random.randint(0, 1)
           nodo_coloreado = {
               "id": str(nodo),
               "type": "default",
               "data": {"label": f"{str(nodo)}"},
               "style": {
                   "background": "blue" if colour == 0 else "red",
                   "width": 75,
                   "height": 75,
                   "align-items": "center",
                   "box-shadow": "-2px 10px 100px 3px rgba(255,255,255,0.25)",
                   "text-shadow": "4px 4px 2px rgba(0,0,0,0.3)",
                   "font-size": "30px",
                   "border-radius": "50%"
               },
               "position": {"x": random.randint(100, 400), "y": random.randint(100, 200)},
               "linkedTo": []  # Inicializa la lista de nodos conectados
           }
           grafo_coloreado.append(nodo_coloreado)


   return True, color, grafo_coloreado
def componentes_conexas_bipartito(grafo):
   def es_bipartito_y_componente(subgrafo):
       es_bipartito, colores, grafo = colorear_bipartito(subgrafo)
       if not es_bipartito:
           return False, set()
       return True, set(colores.keys())


   visitados_global = set()
   componentes = []
   es_bipartito_global = True


   for nodo in grafo:
       if nodo not in visitados_global:
           subgrafo = {n: grafo[n] for n in grafo if n not in visitados_global}
           es_bipartito, componente = es_bipartito_y_componente(subgrafo)
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
   num_componentes_conexas = len(componentes_conexas)
   if num_componentes_conexas == 0:
       st.error("El grafo no es bipartito o no se ha cargado el archivo.")
   else:
       st.success(
           f"El grafo es bipartito y tiene {num_componentes_conexas} {'componente' if num_componentes_conexas == 1 else 'componentes'} conexas: {componentes_conexas}")
   return
