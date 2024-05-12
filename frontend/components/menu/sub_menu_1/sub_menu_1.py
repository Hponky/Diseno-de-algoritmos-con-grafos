import streamlit as st
from streamlit_react_flow import react_flow
from frontend.components.menu.sub_menu_1.sub_menu_2 import sub_menu_2
from backend.utils import file_json
from backend.models.graph import Grafo
from backend.generators import json_elements
from backend.generators import graph_generator
from backend.generators.graph_detector import *


Elements = Grafo()


def file_menu():
   st.subheader("Seleccionaste el menu de archivo")
   # Opciones del submenú "Archivo"
   file_options = ["Nuevo Grafo", "Abrir", "Cerrar", "Guardar", "Guardar como", "Exportar Datos", "Importar Datos",
                  "Salir"]
   selected_option = st.sidebar.selectbox("Opciones de Archivo", file_options, index=1)


   if selected_option is not None:
       if selected_option == "Nuevo Grafo":
           sub_menu_2.new_grafo_menu()
       elif selected_option == "Exportar Datos":
           st.write(f"Seleccionaste la opción de menu: {selected_option}")
           sub_menu_2.export_data_menu()
       elif selected_option == "Importar Datos":
           st.write(f"Seleccionaste la opción de menu: {selected_option}")
           elements = []
           Elements.set_elements(elements)
           Elements.open_txt()
       elif selected_option == "Abrir":
           st.write(f"Seleccionaste la opción de menu: {selected_option}")
           Elements.open_json()
       elif selected_option == "Guardar":
           if Elements.get_elements() == []:
              st.write("No existen elementos a guardar")
           else:
              st.write(f"Seleccionaste la opción: {selected_option}")
              file_json.save_elements_to_json(Elements.get_elements(), "documents/saved")
       elif selected_option == "Guardar como":
           if Elements.get_elements() == []:
              st.write("No existen elementos a guardar")
           else:
              nombreArchivo = st.text_input("Ingrese el nombre del archivo a guardar:")
              if nombreArchivo != "":
                  file_json.save_elements_to_json_as(Elements.get_elements(), "documents/saved_as", nombreArchivo)
       elif selected_option == "Cerrar":
           st.write("De clic en confirmar para cerrar el espacio de trabajo")
           clic = st.button("Confirmar")
           if clic:
              elements = []
              Elements.set_elements(elements)
              st.warning("Se ha cerrado el espacio de trabajo")
       elif selected_option == "Salir":
           st.write("Cerrando pestaña...")
           # Redirigir a una página inexistente para cerrar la pestaña
           st.markdown("<meta http-equiv='refresh' content='0;URL=about:blank' />", unsafe_allow_html=True)
       else:
           st.write(f"Seleccionaste la opción de archivo: {selected_option}")


   return Elements


def edit_menu():
   graph_generator.custom_elements = []
   if Elements.get_elements():
       st.subheader("Seleccionaste el menu de editar")
       st.sidebar.subheader("Editar")
       # Opciones del submenú "Editar"
       edit_options = ["Deshacer", "Nodo", "Arista"]
       selected_option = st.sidebar.selectbox("Opciones de Editar", edit_options, index=1)
       if selected_option is not None:
           st.write(f"Seleccionaste la opción de editar: {selected_option}")
           if selected_option == "Nodo":
              sub_menu_2.edit_nodo_menu()
           elif selected_option == "Arista":
              sub_menu_2.edit_arco_menu()
           elif selected_option == "Deshacer":
              Elements.set_elements(Elements.undo_last_change(Elements.get_elements()))
   else:
       st.subheader("Selecciona un archivo a editar, o crea un grafo")


def graph_detector_menu():
   st.subheader("Detector de Grafos")


   # Opciones del submenú "Detector de Grafos"
   detector_options = ["Determinar componentes si el grafo es bipartito",
                       "Evaluar combinación con la mínima perdida de peso",
                       "Dividir sistema con menor diferencia de información"]


   selected_option = st.sidebar.selectbox("Opciones del Detector de Grafos", detector_options, index = 0)


   elements = Elements.get_elements()
   conexiones = grafo_formateado(elements)
   if selected_option == "Determinar componentes si el grafo es bipartito":
       componentes_conexas_bipartito(conexiones)
   if selected_option == "Evaluar combinación con la mínima perdida de peso":
       componentes_conexas_bipartito(conexiones)
       min_edge_removal_cost_bipartite_subgraphs(elements)
   if selected_option == "Dividir sistema con menor diferencia de información":
       sistema_original = {
           'A': [0, 1, 0, 1, 0, 1, 0, 1],
           'B': [0, 0, 1, 1, 0, 0, 1, 1],
           'C': [0, 0, 0, 0, 1, 1, 1, 1]
       }


       mejor_division = encontrar_division_optima(sistema_original)
       print("División óptima:", mejor_division)


def execute_menu(elements):
   st.subheader("Seleccionaste el menu de ejecutar")
   st.sidebar.subheader("Ejecutar")
   # Opciones del submenú "Ejecutar"
   execute_options = ["Procesos"]
   selected_option = st.sidebar.selectbox("Opciones de Ejecutar", execute_options)


   if selected_option == "Procesos":
      processes_menu()
   else:
      st.write(f"Seleccionaste la opción de procesos: {selected_option}")


def tools_menu(elements):
  st.subheader("Seleccionaste el menu de herramientas")
  st.sidebar.subheader("Herramientas")
  # Opciones del submenú "Herramientas"
  tools_options = ["Ventana Gráfica", "Tabla"]
  selected_option = st.sidebar.selectbox("Opciones de Herramientas", tools_options)


  # Mostrar mensaje dependiendo de la opción seleccionada
  st.write(f"Seleccionaste la opción de herramientas: {selected_option}")


def window_menu(elements):
  st.subheader("Seleccionaste el menu de ventana")
  st.sidebar.subheader("Ventana")
  # Opciones del submenú "Ventana"
  window_options = ["Gráfica", "Tabla"]
  selected_option = st.sidebar.selectbox("Opciones de Ventana", window_options)


  # Mostrar mensaje dependiendo de la opción seleccionada
  st.write(f"Seleccionaste la opción de ventana: {selected_option}")


def help_menu(elements):
  st.subheader("Seleccionaste el menu de ayuda")
  st.sidebar.subheader("Ayuda")
  # Opciones del submenú "Ayuda"
  help_options = ["Ayuda", "Acerca de Grafos"]
  selected_option = st.sidebar.selectbox("Opciones de Ayuda", help_options)


  # Mostrar mensaje dependiendo de la opción seleccionada
  st.write(f"Seleccionaste la opción de ayuda: {selected_option}")



