import streamlit as st
import string
import random
from backend.models.graph import Elements

counter = random.randint(100000,999999)

def random_graph(num_nodes, directed=False, weighted=False, connected=False, complete=False):
    # Crear nodos
    nodes = []
    for i in range(num_nodes):
        node_id = i + 1
        node_label = ''.join(random.choices(string.ascii_uppercase, k=3))  # Etiqueta aleatoria de 3 letras
        nodes.append({
            "id": node_id,
            "type": 'default',
            "style": {"background": '#fff', "width": 75, "height": 75, "align-items": "center",
                      "box-shadow": "-2px 10px 100px 3px rgba(255,255,255,0.25)",
                      "text-shadow": "4px 4px 2px rgba(0,0,0,0.3)",
                      "font-size": "30px", "border-radius": "50%"},
            "data": {"label": node_label},
            "position": {"x":random.randint(100,400), "y":random.randint(100,200)},
            "linkedTo": []
        })

    if weighted:
        # Para la opcion conexo
        if connected:
            for i in range(num_nodes):
                for j in range(i + 1, num_nodes):
                    weight = random.randint(1, 100) if weighted else None
                    nodes[i]["linkedTo"].append({"nodeId": nodes[j]["id"], "weight": weight})
                    if not directed and complete:
                        nodes[j]["linkedTo"].append({"nodeId": nodes[i]["id"], "weight": weight})

        if complete:
            for i in range(num_nodes):
                for j in range(i + 1, num_nodes):
                    weight = random.randint(1, 100) if weighted else None
                    nodes[i]["linkedTo"].append({"nodeId": nodes[j]["id"], "weight": weight})
                    if not directed:
                        nodes[j]["linkedTo"].append({"nodeId": nodes[i]["id"], "weight": weight})

    # Para la opcion conexo
    if connected:
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                nodes[i]["linkedTo"].append({"nodeId": nodes[j]["id"], "weight": 0})
                if not directed and complete:
                    nodes[j]["linkedTo"].append({"nodeId": nodes[i]["id"], "weight": 0})

    if complete:
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                nodes[i]["linkedTo"].append({"nodeId": nodes[j]["id"], "weight": 0})
                if not directed:
                    nodes[j]["linkedTo"].append({"nodeId": nodes[i]["id"], "weight": 0})
    return nodes

def custom_graph(elements):
    # Botón para añadir nodo al grafo personalizado
    if st.button("Añadir nodo"):
        global counter
        counter = Elements.generate_numeric_guid(counter)
        nombre = st.text_input("Ingrese el nombre del nodo:")
        if nombre != "":
            repetido = False
            for element in elements:
                if nombre == element["label"]:
                    repetido = True
                    break  # Salir del bucle una vez que se encuentra un nombre repetido
            if not repetido:
                elements.add_node(Elements.get_elements(), counter, nombre)
                counter += 1  # Incrementar el contador para el próximo nodo
            else:
                st.write("Ya existe un nodo con ese nombre")

def manual_conection(elements, tipo_arista):
   # Obtener los nombres de los nodos
   opciones = []
   for element in elements:
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
       for element in elements:
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
           # Verificar si la conexión ya existe
           if "linkedTo" in elemento_origen:
               for link in elemento_origen["linkedTo"]:
                   if int(link["nodeId"]) == int(elemento_destino["id"]):
                       st.warning("La conexión ya existe.")
                       return


           # Agregar la conexión al nodo de origen
           if "linkedTo" not in elemento_origen:
               elemento_origen["linkedTo"] = []


           # Definir el valor de "animated" según el tipo de arista
           animated_value = tipo_arista == "Dirigida"
           elements.append({'id': f'edge-{elemento_origen["id"]}-{elemento_destino["id"]}',
                                           'source': f'{elemento_origen["id"]}', 'target': f'{elemento_destino["id"]}',
                                           'animated': animated_value})
           for element in elements:
               if str(element["id"]) == str(elemento_origen["id"]):
                   element["linkedTo"].append({'nodeId': f'{(elemento_destino["id"])}', 'weight': f'{peso}'})
           Elements.show_node_coordinates(Elements.get_elements())
           # Mostrar la conexión agregada
           st.success(f"Conexión agregada entre '{nodo_origen}' y '{nodo_destino}' con un peso de {peso}.")

