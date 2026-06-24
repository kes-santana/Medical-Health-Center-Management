import streamlit as st

from frontend.bridge import asignar_vacaciones, crear_empleado, listar_empleados, obtener_empleado



st.header("Gestion de Empleados")
tab_add, tab_get, tab_list, tab_vacations = st.tabs(["Crear", "Ver Detalles", "Listar", "Vacaciones"])

with tab_add:

    st.subheader("Crear Nuevo Empleado", divider=True, width="content")

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

with tab_get:

    st.header("Detalles de Empleado", divider="blue", width="content")
    with st.form("get_employee_form"):
        st.subheader("Obtener Empleado")
        id = st.number_input("ID del empleado", min_value=1)
        print(f"Id = {id}")
    
        submitted_get_employee = st.form_submit_button("Buscar")
        
        if submitted_get_employee:
            try:
                empleado = obtener_empleado(id)
                st.dataframe(empleado, height=80)
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
        
        employee = st.selectbox("Employee", options=st.session_state.all_empl)
        start_date = st.date_input("Start Date", format= "YYYY-MM-DD")
        end_date = st.date_input("End Date",  format= "YYYY-MM-DD")
        
        submitted_vacations = st.form_submit_button("Assign", use_container_width=True)
        if submitted_vacations:
            try:
                asignar_vacaciones(employee, start_date, end_date)
                st.success("Se asignaron las vacaciones con exito.")
            except Exception as e:
                st.error(e)