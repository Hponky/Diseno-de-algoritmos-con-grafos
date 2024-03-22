import streamlit as st

def redit_nodo_menu():
    options = ["Color", "Etiqueta", "Valor"]
    selected_option = st.sidebar.selectbox("Seleccionar tipo de edicion", options)
    st.write(f"Seleccionaste la opción de edición: {selected_option}")

def redit_arco_menu():
    options = ["Tipo de Línea", "Color", "Peso"]
    selected_option = st.sidebar.selectbox("Seleccionar tipo de edicion", options)
    st.write(f"Seleccionaste la opción de edición: {selected_option}")