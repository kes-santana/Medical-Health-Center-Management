### Para que la app quede como un componente view la primera parte de app.py 
## es todo lo que llama al backend, la segunda es las cosas que estan en la ssesion_state
#  y la tercera parte es la logica


import sys
import os
# Obtiene la ruta del proyecto (un nivel arriba de Frontend)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)
import streamlit as st
import calendar
import datetime
from Frontend.front_utils import load_employees_names, load_resources_names
from Frontend.bridge import *

try:
    if not "all_rec" in st.session_state:
        st.session_state.all_rec = load_resources_names()
    if not "all_empl" in st.session_state:
        st.session_state.all_empl = load_employees_names()
    USER = "" #Usuario Actual
    USER_KEY = ""
    ROL = "" #Roles del UsuarioActual
    ID = 0

    #   <-- Configuración de la página -->

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "app_user" not in st.session_state:
        st.session_state.app_user = ""
    if "app_user_password" not in st.session_state:
        st.session_state.app_user_password = ""
    if "app_user_rol" not in st.session_state:
        st.session_state.app_user_rol = ""
    if "app_user_key" not in st.session_state:
        st.session_state.app_user_key = ""
    if "app_user_id" not in st.session_state:
        st.session_state.app_user_id = 0


    st.set_page_config(page_title="Medical Health Center Management", 
                    page_icon="Frontend/assets/icon.jpg", layout="centered")
    st.logo("Frontend/assets/icon.jpg")
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

        col1, col2 = st.columns([0.5,0.5])

        with col1:
            with st.container(border=True):

                citas_medicas = month_dates()

                # --- ESTILOS CSS PARA UN LOOK "EXTRA-COMPACTO" ---
                css_code = """
                /* Encabezados de los días de la semana - más pequeños y juntos */
                .day-header {
                    text-align: center;
                    font-weight: bold;
                    color: #6c757d;
                    font-size: 11px; /* Aún más pequeño */
                    padding-bottom: 5px;
                }

                /* Círculos de los días - MUY PEQUEÑOS */
                .day-circle {
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    width: 28px;  /* Reducido de 35px */
                    height: 28px; /* Reducido de 35px */
                    border-radius: 50%;
                    font-weight: 500;
                    font-size: 12px; /* Reducido de 14px */
                    transition: all 0.2s ease-in-out;
                    margin: 0 auto;
                }

                /* Colores de fondo (sin cambios) */
                .no-appointment { background-color: #e9ecef; color: #495057; }
                .normal { background-color: #a3d5ff; color: #004085; }
                .urgent { background-color: #ffc9c9; color: #721c24; }

                /* Resaltado para el día actual - borde muy fino */
                .today {
                    border: 2px solid #007bff;
                    /* Quitamos la sombra para un look más limpio y compacto */
                }
                """

                st.markdown(f'<style>{css_code}</style>', unsafe_allow_html=True)

                # --- LÓGICA DEL CALENDARIO (con columnas más juntas) ---

                now = datetime.datetime.now()
                current_year = now.year
                current_month = now.month

                month_name = now.strftime("%B %Y")
                st.subheader(f" Calendario de Citas: {month_name.capitalize()}")

                month_matrix = calendar.monthcalendar(current_year, current_month)
                days_of_week = ["L", "M", "M", "J", "V", "S", "D"]

                # Usamos gap="small" para reducir el espacio entre columnas
                cols = st.columns(7)
                for i, day_name in enumerate(days_of_week):
                    with cols[i]:
                        st.markdown(f'<div class="day-header">{day_name}</div>', unsafe_allow_html=True)

                st.markdown("<hr style='margin-top: 0; margin-bottom: 0.5rem;'>", unsafe_allow_html=True) 

                for week in month_matrix:
                    cols = st.columns(7, gap="small")
                    for i, day_num in enumerate(week):
                        with cols[i]:
                            if day_num != 0:
                                # Comprobar si el día está en el diccionario de citas
                                if day_num in citas_medicas:
                                    # Si está, comprobar si es True (urgente) o False (normal)
                                    if citas_medicas[day_num] is True:
                                        css_class = "urgent"
                                    else:
                                        css_class = "normal"
                                else:
                                    # Si no está en el diccionario, no hay cita
                                    css_class = "no-appointment"

                                # Comprobar si es el día de hoy para añadir el resaltado
                                if day_num == now.day:
                                    css_class += " today"
                                
                                # Renderizar el HTML
                                st.markdown(
                                    f'<div class="day-circle {css_class}">{day_num}</div>',
                                    unsafe_allow_html=True
                                )

                # --- LEYENDA ---
                st.markdown("---") # Una línea simple es más compacta
                st.write("Leyenda")
                legend_cols = st.columns(3)
                with legend_cols[0]:
                    st.markdown('<div class="day-circle no-appointment"></div>', unsafe_allow_html=True)
                    st.markdown("<p style='text-align: center; font-size: 11px;'>Sin Cita</p>", unsafe_allow_html=True)
                with legend_cols[1]:
                    st.markdown('<div class="day-circle normal"></div>', unsafe_allow_html=True)
                    st.markdown("<p style='text-align: center; font-size: 11px;'>Cita Normal</p>", unsafe_allow_html=True)
                with legend_cols[2]:
                    st.markdown('<div class="day-circle urgent"></div>', unsafe_allow_html=True)
                    st.markdown("<p style='text-align: center; font-size: 11px;'>Cita Urgente</p>", unsafe_allow_html=True)



        with col2:
                with st.form("login"):
                    st.subheader("Login")
                    user_input = st.text_input("User")
                    password_input = st.text_input("Password", max_chars=30, type="password")

                    submitted_login = st.form_submit_button("Start", use_container_width=True)

                    if submitted_login:
                        accept, user, user_rol, user_key = verify_login(user_input, password_input)
                        if accept:
                            st.session_state.app_user = user
                            st.session_state.app_user_password = password_input
                            st.session_state.app_user_rol = user_rol
                            st.session_state.app_user_key = user_key
                            st.session_state.app_user_id = int(user_key.split(" ")[0])
                            print("Credenciales validas")
                            st.session_state.logged_in = True
                            st.rerun()
                        else:
                            st.error("Credenciales no validas. Verifique sus credenciales")
    else:
        
        verify_vacations()

        st.sidebar.title("Menu")
        st.sidebar.divider()
        ROL = st.session_state.app_user_rol

        dashboard_page = st.Page("pages/dashboard.py", title="Dashboard")
        event_page = st.Page("pages/events.py", title="Eventos")
        employees_page = st.Page("pages/employees.py", title="Empleados")
        resources_page = st.Page("pages/resources.py", title="Recursos")
        user_config_page = st.Page("pages/user_config.py", title="Usuario")
        system_page = st.Page("pages/system.py", title="System")
        about_page = st.Page("pages/about.py", title="About")

        nav = st.navigation([dashboard_page, event_page, employees_page, resources_page,
                            user_config_page, system_page, about_page], position="hidden")
        
        st.sidebar.page_link("pages/about.py", label="About")
        st.sidebar.page_link("pages/dashboard.py", label="Dashboard")
        st.sidebar.page_link("pages/events.py", label="Eventos")
        if ROL == "admin":
            st.sidebar.page_link("pages/employees.py", label="Empleados")
            st.sidebar.page_link("pages/resources.py", label="Recursos")
        st.sidebar.page_link("pages/user_config.py", label="User")
        if ROL == "admin":
            st.sidebar.page_link("pages/system.py", label="System")
        
        nav.run()

        
        refresh_action = st.sidebar.button("Refresh")

        if refresh_action:
            st.session_state.all_rec, st.session_state.all_empl = refresh()
            refresh_action = False

    st.divider()
    st.markdown("<p style='text-align: center;" 
                "color: gray;" \
                "'>© 2026 Medical Health Center Management</p>",
                unsafe_allow_html=True)
        
except Exception as e:
    st.error(e)