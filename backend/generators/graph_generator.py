import streamlit as st
import string
import random

from backend.models.graph import Grafo

Elements = Grafo()
custom_elements = []

def complete_graph(directed, weighted):
    if directed:
        for o in Elements.get_elements():
            for d in Elements.get_elements():
                weight = random.randint(1, 100) if weighted else 0
                if not o["id"].startswith('edge') and not d["id"].startswith('edge'):
                    if o["id"] != d["id"]:
                        Elements.set_elements(Elements.add_edge(Elements.get_elements(), o, d, directed, weight))
    else:
        for o in Elements.get_elements():
            for d in Elements.get_elements():
                weight = random.randint(1, 100) if weighted else 0
                if not o["id"].startswith('edge') and not d["id"].startswith('edge'):
                    if int(o["id"]) < int(d["id"]):
                        Elements.set_elements(
                            Elements.add_edge(Elements.get_elements(), o, d, directed, weight))

def connected_graph(num_nodes, directed, weighted):
    for o in Elements.get_elements():
        if not o["id"].startswith('edge'):
            id = int(o["id"]) + 1 if int(o["id"]) <= num_nodes - 2 else 0
            for d in Elements.get_elements():
                weight = random.randint(1, 100) if weighted else 0
                if not d["id"].startswith('edge'):
                    if int(d["id"]) == id:
                        Elements.set_elements(Elements.add_edge(Elements.get_elements(), o, d, directed, weight))


def random_graph(num_nodes, directed=False, weighted=False, connected=False, complete=False):
    # Crear nodos random
    Elements.add_nodes_random(num_nodes)

    # Para la opcion conexo
    if connected:
        if complete:
            complete_graph(directed, weighted)
        else:
            connected_graph(num_nodes,directed,weighted)

    # Para la opcion completo
    elif complete:
        complete_graph(directed, weighted)

def add_custom_node():
    nombre = st.text_input("Ingrese el nombre del nodo: ")
    x = st.number_input("Ingrese las coordenadas para X: ")
    y = st.number_input("Ingrese las coordenadas para Y: ")
    if nombre != "":
        repetido = False
        for element in Elements.get_elements():
            if 'data' in element and 'label' in element['data'] and nombre == element['data']["label"]:
                repetido = True
        if not repetido:
            change = Elements.add_node(Elements.get_elements(), random.randint(100000,999999), nombre,x,y)
            Elements.set_elements(change)
            st.success(f"Nodo '{nombre}' agregado correctamente")
        else:
            st.warning("Ya existe un nodo con ese nombre")

def custom_graph():
    global custom_elements
    if Elements.get_elements() != custom_elements:
        Elements.set_elements(custom_elements)
    options_1 = ["Agregar Nodo", "Agregar Arista"]
    selected_option_1 = st.selectbox(f"Seleccione la opción que desea", options_1, index=0)
    if selected_option_1 is not None:
        if selected_option_1 == "Agregar Nodo":
            add_custom_node()
        elif selected_option_1 == "Agregar Arista":
            tipo_arista = st.selectbox("Tipo de arista", ["Dirigida", "No dirigida"])
            st.write(f"Tipo de arista seleccionada: {tipo_arista}")
            manual_conection(tipo_arista)
        custom_elements = Elements.get_elements()

def añadir_conexion(elemento_origen,elemento_destino, tipo_arista, peso):
    # Verificar si la conexión ya existe
    if "linkedTo" in elemento_origen:
        for link in elemento_origen["linkedTo"]:
            if str(link["nodeId"]) == str(elemento_destino["id"]):
                st.warning("La conexión ya existe.")
                return

    # Agregar la conexión al nodo de origen
    if "linkedTo" not in elemento_origen:
        elemento_origen["linkedTo"] = []

    # Definir el valor de "animated" según el tipo de arista
    animated_value = tipo_arista == "Dirigida"

    Elements.set_elements(Elements.add_edge(Elements.get_elements(), elemento_origen, elemento_destino, animated_value, peso))


def manual_conection(tipo_arista):
   # Obtener los nombres de los nodos
   opciones = []
   for element in Elements.get_elements():
       if "label" in element:
           opciones.append(element["label"])
       elif "data" in element and "label" in element["data"]:
           opciones.append(element["data"]["label"])


   # Crear los selectores de opción para el nodo de origen y el nodo de destino
   nodo_origen = st.selectbox("Selecciona el nodo de origen:", opciones)
   nodo_destino = st.selectbox("Selecciona el nodo de destino:", opciones)


   # Obtener el peso de la conexión
   peso = st.number_input("Ingrese el peso de la conexión:", min_value=0)


   # Encontrar los elementos correspondientes a los nodos de origen y destino
   elemento_origen = None
   elemento_destino = None


   # Botón para confirmar los cambios y guardar
   if st.button("Confirmar cambios y guardar"):
       for element in Elements.get_elements():
           if ("label" in element and nodo_origen == element["label"]) or \
              ("data" in element and "label" in element["data"] and nodo_origen == element["data"]["label"]):
               elemento_origen = element
           if ("label" in element and nodo_destino == element["label"]) or \
              ("data" in element and "label" in element["data"] and nodo_destino == element["data"]["label"]):
               elemento_destino = element

       # Verificar si los nodos de origen y destino son diferentes
       if nodo_origen == nodo_destino:
           st.warning("Los nodos de origen y destino deben ser diferentes.")
       elif elemento_origen is None or elemento_destino is None:
           st.warning("Los nodos de origen y destino deben estar presentes en el grafo.")
       else:
           añadir_conexion(elemento_origen,elemento_destino,tipo_arista,peso)
           if tipo_arista:
               st.success(f"Conexión no dirigida agregada entre '{nodo_origen}' y '{nodo_destino}' con un peso de {peso}.")
           else:
               st.success(f"Conexión dirigida agregada entre '{nodo_origen}' y '{nodo_destino}' con un peso de {peso}.")

