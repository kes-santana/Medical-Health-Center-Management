
import sys
import os
# Obtiene la ruta del proyecto (un nivel arriba de Frontend)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)
import streamlit as st
from Frontend.front_utils import clean_resource_list, load_emp_names, load_rec_names, search_id_by_name
from Frontend.bridge import *

ALL_REC = load_rec_names()
ALL_EMPL = load_emp_names()
USER = "" #Usuario Actual
ROL = "" #Roles del UsuarioActual


#   <-- Configuración de la página -->

if "logged_in" not in st.session_state:
     st.session_state.logged_in = False
if "app_user" not in st.session_state:
     st.session_state.app_user = ""
if "app_user_password" not in st.session_state:
     st.session_state.app_user_password = ""
if "app_user_rol" not in st.session_state:
     st.session_state.app_user_rol = ""

st.set_page_config(page_title="Medical Health Center Management", 
                   page_icon="Frontend/icon.jpg", layout="centered")
st.logo("Frontend/icon.jpg")
st.markdown(
    "<h1 style= 'text-align: center; '>Welcome to Medical Health Center Management</h1>",
    unsafe_allow_html=True,
)
st.markdown("---")

if not st.session_state.logged_in:
    # #  Ocultar el sidebar en la pagina de inicio
    css_container = st.empty()
    css_container.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none;}
        section[data-testid="stSidebar"] {display: none;}
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([0.2,0.6,0.2])

    with col2:
            with st.form("login"):
                st.subheader("Login")
                user_input = st.text_input("User")
                password_input = st.text_input("Password", max_chars=30)

                submitted_login = st.form_submit_button("Start", use_container_width=True)

                if submitted_login:
                    accept, user, rol = verify_login(user_input, password_input)
                    if accept:
                        st.session_state.app_user = user
                        st.session_state.app_user_password = password_input
                        st.session_state.app_user_rol = rol
                        print("Credenciales validas")
                        st.session_state.logged_in = True
                        st.rerun()
                    else:
                        st.error("Credenciales no validas. Verifique sus credenciales")
else:
    
    st.sidebar.title("Menu")
    st.sidebar.divider()
    
    event_page = st.Page("events.py", title="Eventos")
    resources_page = st.Page("resources.py", title="Recursos")
    employees_page = st.Page("employees.py", title="Empleados")
    user_config_page = st.Page("user_config.py", title="Usuario")
    system_page = st.Page("system.py", title="System")
    about_page = st.Page("about.py", title="About")

    nav = st.navigation([event_page, resources_page, employees_page,
                          user_config_page, system_page, about_page], position="hidden")
    
    st.sidebar.page_link("events.py", label="Eventos")
    st.sidebar.page_link("resources.py", label="Recursos")
    st.sidebar.page_link("employees.py", label="Empleados")
    st.sidebar.page_link("user_config.py", label="User")
    st.sidebar.page_link("system.py", label="System")
    st.sidebar.page_link("about.py", label="About")

    nav.run()

st.divider()
st.markdown("<p style='text-align: center;" 
            "color: gray;" \
            "'>© 2026 Medical Health Center Management</p>",
            unsafe_allow_html=True)