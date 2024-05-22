import streamlit as st
import random
import string
import json


from backend.generators.json_elements import *
from streamlit_react_flow import react_flow
from documents.saved import *


elementos = []


class Grafo:


   def __init__(self):
       global elementos
       self.elementos = elementos


   def get_elements(self):
       global elementos
       return elementos


   def set_elements(self, elements):
       global elementos
       elementos = elements
       self.elementos = elements


   def get_element_id(self, element):
       id_value = element.get('id')
       if isinstance(id_value, int):  # Verificar si el ID es un entero
           return str(id_value)
       return id_value


   def get_element_label_by_id(self, id):
       for element in self.get_elements():
           if element['id'] == id:
               return element['data']['label']
       return id


   def get_element_by_label(self, grafo, label):
       for element in grafo:
           if 'data' in element:
               if element['data']['label'] == label:
                   return element


   def get_nodos_no_dirigidos(self):
       nodos = []
       for elemento in self.get_elements():
           if 'source' in elemento and 'target' in elemento:
               if elemento['animated'] == False:
                   cod = (f'{self.get_element_label_by_id(elemento["source"])},'
                          f'{self.get_element_label_by_id(elemento["target"])}')
                   nodos.append(cod)
       return nodos


   def add_nodes_random(self,num_nodes):
       for i in range(num_nodes):
           label = ''.join(random.choices(string.ascii_uppercase, k=3))
           change = self.add_node(self.get_elements(), i, label,random.randint(100,400),random.randint(100,200))
           self.set_elements(change)


   def find_index_node_by_label(self, label, elements):
       create_elements_from_list(elements)
       for i, element in enumerate(elements):  # Utiliza enumerate para obtener tanto el índice como el elemento
           if 'data' in element and 'label' in element['data']:
               if label == element['data']['label']:  # Utiliza == en lugar de 'is' para comparar cadenas
                   node_found = i
                   return node_found
       return -1


   @staticmethod
   def add_node(graph, node_id, node_label, x, y):
       new_node = {
           "id": str(node_id),
           "type": "default",
           "style": {"background": '#fff', "width": 75, "height": 75, "align-items": "center",
                     "box-shadow": "-2px 10px 100px 3px rgba(255,255,255,0.25)",
                     "text-shadow": "4px 4px 2px rgba(0,0,0,0.3)",
                     "font-size": "30px", "border-radius": "50%"},
           "data": {"label": node_label},
           "position": {"x": x, "y": y},
           "linkedTo": []
       }
       graph.append(new_node)


       return graph


   @staticmethod
   def add_edge(graph, elemento_origen, elemento_destino, animated, peso):
       graph.append({'id': f'edge-{elemento_origen["id"]}-{elemento_destino["id"]}',
                        'source': f'{elemento_origen["id"]}', 'target': f'{elemento_destino["id"]}',
                        'animated': animated, 'style': {'stroke': 'white'}})
       if animated:
           for element in graph:
               if str(element["id"]) == str(elemento_origen["id"]):
                   element["linkedTo"].append({'nodeId': f'{(elemento_destino["id"])}', 'weight': f'{peso}'})
       return graph


   def delete_conetion(self, elementos, source_id, target_id, origen, destino):
       for element in elementos:
           if str(element['id']) == f'edge-{source_id}-{target_id}':
               break
           if str(element['id']) == f'edge-{target_id}-{source_id}':
               if not element['animated']:
                   aux = source_id
                   source_id = target_id
                   target_id = aux
                   break


       # Función para eliminar una conexión entre nodos en el grafo
       updated_elements = [element for element in elementos
                           if not ('source' in element and 'target' in element
                                   and str(element.get('source', 0)) == source_id
                                   and str(element.get('target', 0)) == target_id)]
       for element in updated_elements:
           element_id = self.get_element_id(element)
           if not element_id.startswith('edge'):
               if str(element_id) == source_id:
                   element['linkedTo'] = [link for link in element.get('linkedTo', []) if
                                          link.get('nodeId') != target_id]


       if len(updated_elements) < len(elementos):
           st.success(f"Conexión de '{origen}' a '{destino}' eliminada correctamente")
           self.set_elements(updated_elements)
       else:
           st.warning("No se encontró la conexión para eliminar")




   @staticmethod
   def undo_last_change(graph):
       # Función para deshacer el último cambio realizado
       if Elements.cambios_realizados:
           # Obtener el último cambio realizado de la pila
           ultimo_cambio = Elements.cambios_realizados.pop()


           # Deshacer el último cambio
           if ultimo_cambio[0] == "add_node":
               # Si el último cambio fue agregar un nodo, eliminamos el nodo
               _, (node_id, _) = ultimo_cambio
               graph = [node for node in graph if node['id'] != node_id]
           elif ultimo_cambio[0] == "delete_edge":
               # Si el último cambio fue eliminar una conexión entre nodos, volvemos a conectar los nodos
               _, (source_id, target_id) = ultimo_cambio
               for node in graph:
                   if node['id'] == source_id:
                       node['linkedTo'].append({"nodeId": target_id, "weight": None})
                   elif node['id'] == target_id:
                       node['linkedTo'].append({"nodeId": source_id, "weight": None})
           return graph
       else:
           return graph


   def open_txt(self):
       # Cargar archivo
       uploaded_file = st.file_uploader("Cargar archivo", type=["txt"])


       if uploaded_file is not None:
           if uploaded_file.type == 'text/plain':  # Si el archivo es de tipo txt
               txt_content = uploaded_file.getvalue().decode("utf-8")
               st.text_area("Contenido TXT", value=txt_content, height=400)
               Elements.set_elements(create_elements_from_json(uploaded_file))
               flow_styles = {"height": 500, "width": 800}
               react_flow("graph", elements=Elements.get_elements(), flow_styles=flow_styles)


   def open_json(self):
       # Cargar archivo
       uploaded_file = None
       uploaded_file = st.file_uploader("Cargar archivo", type=["json"])


       if uploaded_file is not None:
           # Cargar el archivo JSON
           if uploaded_file.type == 'application/json':
               self.set_elements(create_elements_from_json(uploaded_file))
               flow_styles = {"height": 500, "width": 800}
               react_flow("graph", elements=self.get_elements(), flow_styles=flow_styles)




   def define_styles(self,color):
       style = { f"background": f'{color}', "width": 75, "height": 75, "align-items": "center",
                  "box-shadow": "-2px 10px 100px 3px rgba(255,255,255,0.25)", "text-shadow": "4px 4px 2px rgba(0,0,0,0.6)",
                  "font-size":"30px", "border-radius": "50%"}


   def display_flow(self):
       self.set_elements(create_elements_from_list(self.get_elements()))
       flow_styles = {"height": 500, "width": 800}
       react_flow("graph", elements=self.get_elements(), flow_styles=flow_styles)





