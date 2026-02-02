import streamlit as st

from Frontend.app import ALL_EMPL
from Frontend.bridge import asignar_vacaciones, crear_empleado, listar_empleados

if "create_employee" not in st.session_state:
    st.session_state.create_employee = False
if "list_employees" not in st.session_state:
    st.session_state.list_employees = False
if "set_vacations" not in st.session_state:
    st.session_state.set_vacations = False


st.header("Gestion de Empleados")
tab_add, tab_list, tab_vacations = st.tabs(["Crear", "Listar", "Vacaciones"])

with tab_add:

    st.header("Crear Nuevo Empleado", divider=True, width="content")

    with st.form("create_employee_form"):
        st.subheader("Crear empleado")
        employee_name = st.text_input("Employee Name")
        employee_exp = st.number_input("Experience", min_value=15, max_value=100)
        employee_is_doctor = st.checkbox("Is a Doctor")
        submitted_employee = st.form_submit_button("Crear",width="stretch")
        if submitted_employee:
            try:
                crear_empleado(employee_name, employee_exp, employee_is_doctor)
                st.success("Se ha creado el empleado con exito.")
            except Exception as e:
                st.error(e)

with tab_list:

    st.header("Listar Empleados", divider="blue", width="content")

    try:
        listed_employees = listar_empleados()
        st.dataframe(listed_employees)
    except Exception as e:
        st.error(e)

with tab_vacations:

    st.header("Asignar Vacaciones", divider="blue", width="content")

    with st.form("assign_vacations_form"):
        st.subheader("Asignar Vacaciones")
        
        employee = st.selectbox("Employee", options=ALL_EMPL)
        start_date = st.date_input("Start Date", format= "YYYY-MM-DD")
        end_date = st.date_input("End Date",  format= "YYYY-MM-DD")
        
        submitted_vacations = st.form_submit_button("Assign", use_container_width=True)
        if submitted_vacations:
            try:
                asignar_vacaciones(employee, start_date, end_date)
                st.success("Se asignaron las vacaciones con exito.")
            except Exception as e:
                st.error(e)