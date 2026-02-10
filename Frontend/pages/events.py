import streamlit as st

from Frontend.app import ROL, USER_KEY
from Frontend.bridge import cambiar_estado_de_evento, guardar_evento, listar_eventos, obtener_evento

if "rec_form_for_event" not in st.session_state:
    st.session_state.rec_form_for_event = False
if "event" not in st.session_state:
    st.session_state.event = {}
if "event_resources" not in st.session_state:
    st.session_state.event_resources = []

USER_KEY = st.session_state.app_user_key
ROL: str = st.session_state.app_user_rol

st.header("Gestion de Eventos")
tab_add, tab_get, tab_list, tab_estados = st.tabs(["Agregar", "Ver Detalles", "Listar", "Cambiar Estado"])

with tab_add:
    
    # Mostrar formulario si está activo
    with st.form("formulario_paciente"):
        st.subheader("Formulario de Registro")
        
        event_name = st.text_input("Nombre de la Consulta")
        date = st.date_input("Fecha de la Consulta",  format= "YYYY-MM-DD")
        time = st.time_input("Hora del Evento")
        paciente = st.text_input("Nombre del Paciente")
        empleado = st.selectbox(label= "Doctor", options= st.session_state.all_empl if ROL.title() in ['Admin', 'Secretario'] else [USER_KEY])
        urgencia = st.checkbox("Es urgencia")
        time_auto = st.checkbox("Seleccionar hora automática")
        date_time_auto = st.checkbox("Seleccionar Hora y Fecha automática")

        # Botón para enviar
        submitted_event = st.form_submit_button("Salvar", use_container_width=True)

        if submitted_event:
            st.session_state.event["nombre"] = event_name
            st.session_state.event["date"] = date
            st.session_state.event["time"] = time
            st.session_state.event["paciente"] = paciente
            st.session_state.event["empleado"] = empleado
            st.session_state.event["urgencia"] = urgencia
            st.session_state.event["date_time_auto"] = date_time_auto
            st.session_state.event["time_auto"] = time_auto

            print(st.session_state.event["nombre"])
            st.session_state.rec_form_for_event = True

    if st.session_state.rec_form_for_event:
        try:
            with st.form("Recurso que usara"):
                st.subheader("Formulario de Recurso")
                nombre_rec_event = st.selectbox(label="Nombre Recurso", options=st.session_state.all_rec)
                count_rec_event = st.number_input(label="Cantidad", min_value=1)
                
                submitted_rec = st.form_submit_button("Agregar", use_container_width=True)
                
                if submitted_rec:
                    change_count = False
                    for r in st.session_state.event_resources:
                        if nombre_rec_event == r[0]:
                            r[1] += count_rec_event
                            change_count = True
                            break
                    if not change_count:
                        st.session_state.event_resources.append([nombre_rec_event, count_rec_event])
        
        except Exception as e:
            st.error(e)

    if st.button("Show Info"):
        with st.container(border=True):
            try:
                st.write(f"Nombre de Consulta: {st.session_state.event["nombre"]}")
                st.write("Recursos usados:")
                for rec in st.session_state.event_resources:
                    st.write(f"{rec[0]}: {rec[1]}")
            except:
                st.error("No hay info disponible. Debe salvar la info del formulario.")


    if st.button("Guardar Evento"):
        try:
            recs = [item[0] for item in st.session_state.event_resources]
            recs_count = [item[1] for item in st.session_state.event_resources]
            event = st.session_state.event
            response = guardar_evento(event["nombre"], event["date"], event["time"], event["paciente"], event["empleado"],
                        event["urgencia"], recs, recs_count, event["date_time_auto"], event["time_auto"])
            
            st.session_state.rec_form_for_event = False
            st.session_state.event = {}
            st.session_state.event_resources = []

            st.write("Se creo la Consulta con Exito!!!!")
            st.write(f"Fecha: {response.date}")
            st.write(f"Paciente: {response.owns_name}")
            st.write(f"Doctor: {response.employee}")
            st.success("Guardado correctamente")
        except Exception as e:
            st.error(e)
            
with tab_list:
    # Mostrar formulario si está activo
    with st.form("listar eventos form"):
        st.subheader("Listar Eventos")
        query = st.text_input("Query")
        print(f"query = {query}")
    
        submitted_list = st.form_submit_button("Listar")
        
        if submitted_list:
            try:
                filas = listar_eventos(query)
                # Mostrar tabla
                st.dataframe(filas, height=300)

            except Exception as e:
                st.error(e)

with tab_get:
      
    with st.form("get_event_form"):
        st.subheader("Obtener Evento")
        id = st.number_input("ID del evento", min_value=1)
        print(f"Id = {id}")
    
        submitted_get_event = st.form_submit_button("Buscar")
        
        if submitted_get_event:
            try:
                evento = obtener_evento(id)
                st.dataframe(evento, height=80)
            except Exception as e:
                st.error(e)

with tab_estados:

    with st.form("change_state_event_form"):
        st.subheader("Cambiar Estado de Eventos")
        event_id = st.number_input("ID del evento", min_value=1)
        new_state = st.selectbox("Nuevo Estado", ["Finished", "Canceled"])

        if st.form_submit_button("Cambiar", use_container_width=True):
            try:
                cambiar_estado_de_evento(event_id, new_state.lower())
                st.success("Se cambio el estado del evento con exito")
            except Exception as e:
                st.error(e)
            


