import os
import json
import pandas as pd
import streamlit as st


from openpyxl import Workbook
from streamlit_react_flow import react_flow


def create_directory(directory):
   # Crear el directorio si no existe
   if not os.path.exists(directory):
       os.makedirs(directory)


# Función para guardar los datos en un archivo de Excel
def export_graph_to_excel(elementos, nombre_archivo):
   # Crear un nuevo libro de trabajo
   wb = Workbook()
   # Seleccionar la hoja activa (por defecto la primera)
   ws = wb.active
   # Definir los encabezados para las columnas
   encabezados = ['id', 'type', 'style', 'data', 'position', 'linkedTo', 'source', 'target', 'animated']
   # Escribir los encabezados en la primera fila
   ws.append(encabezados)
   # Iterar sobre los datos y escribir cada fila en el archivo de Excel
   for elemento in elementos:
       fila = []
       for encabezado in encabezados:
           if encabezado in elemento:
               if encabezado == 'data':
                   fila.append(elemento['data']['label'])
               else:
                   fila.append(str(elemento[encabezado]))
           else:
               fila.append('')
       ws.append(fila)
   # Guardar el archivo de Excel
   wb.save(nombre_archivo)


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


       create_directory(directory)


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


           create_directory(directory)


           # Guardar los datos en formato JSON en un archivo
           filepath = os.path.join(directory, filename+".json")
           with open(filepath, "w") as file:
               json.dump(graph_data, file)


       # Mostrar el nombre de archivo seleccionado
       st.success(f"Se ha guardado el archivo con el nombre: {filename}.json")

