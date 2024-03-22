import streamlit as st
from streamlit_react_flow import react_flow
from frontend.components.menu.menu import *

def main():
    st.title("Grafo con React Flow")
    create_menu_bar()


if __name__ == "__main__":
    main()
