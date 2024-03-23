import json
import os
import streamlit as st
from streamlit_react_flow import react_flow
import pandas as pd

def export_graph_to_excel(graph_list, filename):
    # Crear un DataFrame vacío
    df = pd.DataFrame(graph_list)
    df.to_excel(filename, index=False, engine='openpyxl')

def save_elements_to_json(elements, directory):
    if elements != []:
        # Crear una estructura de datos para el grafo
        graph_data = {
            "graph": [
                {
                    "name": "G",
                    "data": elements
                }
            ]
        }
        # Obtener el nombre único para el archivo
        filename = f"grafo_guardado_1.json"

        # Verificar si ya existe un archivo con el mismo nombre
        file_counter = 2
        while os.path.exists(os.path.join(directory, filename)):
            filename = f"grafo_guardado_{file_counter}.json"
            file_counter += 1

        st.write(f"Se ha guardado el archivo con el nombre: {filename}")

        # Crear el directorio si no existe
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Guardar los datos en formato JSON en un archivo
        filepath = os.path.join(directory, filename)
        with open(filepath, "w") as file:
            json.dump(graph_data, file)


def save_elements_to_json_as(elements, directory, filename):
    if elements != []:
        # Crear una estructura de datos para el grafo
        graph_data = {
            "graph": [
                {
                    "name": "G",
                    "data": elements
                }
            ]
        }

        # Si no se proporciona un nombre de archivo, generarlo automáticamente
        if filename is None:
            filename = f"grafo_guardado_1.json"
            file_counter = 2
            while os.path.exists(os.path.join(directory, filename)):
                filename = f"grafo_guardado_{file_counter}.json"
                file_counter += 1
        else:
            # Verificar si ya existe un archivo con el mismo nombre
            if os.path.exists(os.path.join(directory, filename)):
                # Si existe, agregar sufijo de contador para mantener la unicidad
                filename_base, filename_ext = os.path.splitext(filename)
                file_counter = 1
                while os.path.exists(os.path.join(directory, f"{filename_base}_{file_counter}{filename_ext}")):
                    file_counter += 1
                filename = f"{filename_base}_{file_counter}{filename_ext}.json"

            # Crear el directorio si no existe
            if not os.path.exists(directory):
                os.makedirs(directory)

            # Guardar los datos en formato JSON en un archivo
            filepath = os.path.join(directory, filename+".json")
            with open(filepath, "w") as file:
                json.dump(graph_data, file)

        # Mostrar el nombre de archivo seleccionado
        st.success(f"Se ha guardado el archivo con el nombre: {filename}.json")

def cerrar_ventana():
  st.write(f"<script>window.close()</script>")