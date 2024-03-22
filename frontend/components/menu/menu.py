import streamlit as st
from .sub_menu_1.sub_menu_1 import *

def create_menu_bar():
    # Opciones del menú
    menu_options = ["Archivo", "Editar", "Ejecutar", "Herramientas", "Ventana", "Ayuda"]

    # Agregar opciones al sidebar
    choice = st.sidebar.radio("Menú", menu_options, index = 0)

    if choice is not None:
        # Mostrar submenús según la opción seleccionada
        if choice == "Archivo":
            file_menu()
        elif choice == "Editar":
            edit_menu()
        elif choice == "Ejecutar":
            execute_menu(Elements)
        elif choice == "Herramientas":
            tools_menu(Elements)
        elif choice == "Ventana":
            window_menu(Elements)
        elif choice == "Ayuda":
            help_menu(Elements)

    else:
        st.title("Bienvenido a Graph Editor")

        st.subheader("""
                Graph Editor es una herramienta interactiva que te permite crear, visualizar y manipular grafos de manera intuitiva. 
                Con nuestra aplicación, puedes diseñar redes complejas, realizar análisis de grafos y compartir tus resultados fácilmente.
                """)

        st.subheader("""
                Conveniencias:\n
                - **Facilidad de Uso:** Nuestra interfaz de usuario intuitiva hace que sea fácil
                 para cualquier persona crear y editar grafos.
                - **Interactividad:** Puedes agregar, eliminar y editar nodos y aristas con unos
                 pocos clics.
                - **Análisis de Grafos:** Realiza análisis avanzados como búsqueda de caminos
                 mínimos, detección de ciclos y cálculo de centralidad.
                - **Exportación e Importación:** Exporta tus grafos en varios formatos 
                (JSON, Excel, imagen) y también importa grafos existentes.
                """)