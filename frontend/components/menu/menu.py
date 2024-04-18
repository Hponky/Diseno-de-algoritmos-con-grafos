import streamlit as st
from frontend.components.menu.sub_menu_1.sub_menu_1 import *


def create_menu_bar():
   # Opciones del menú
   menu_options = ["Archivo", "Editar", "Detector de grafos", "Ejecutar", "Herramientas", "Ventana", "Ayuda"]


   # Agregar opciones al sidebar
   choice = st.sidebar.radio("Menú", menu_options, index = 0)


   if choice is not None:
       # Mostrar submenús según la opción seleccionada
       if choice == "Archivo":
           file_menu()
       elif choice == "Editar":
           edit_menu()
       elif choice == "Detector de grafos":
           graph_detector_menu()
       elif choice == "Ejecutar":
           execute_menu(Elements)
       elif choice == "Herramientas":
           tools_menu(Elements)
       elif choice == "Ventana":
           window_menu(Elements)
       elif choice == "Ayuda":
           help_menu(Elements)
