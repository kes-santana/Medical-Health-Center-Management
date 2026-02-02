import streamlit as st

from Frontend.app import ALL_REC, ROL, USER, ALL_EMPL
from Frontend.bridge import guardar_evento, listar_eventos, obtener_evento
from Frontend.front_utils import clean_resource_list

if "event_form" not in st.session_state:
    st.session_state.event_form = False
if "rec_form_for_event" not in st.session_state:
    st.session_state.rec_form_for_event = False
if "event" not in st.session_state:
    st.session_state.event = {}
if "event_resources" not in st.session_state:
    st.session_state.event_resources = []
if "listar_eventos_form" not in st.session_state:
    st.session_state.listar_eventos_form = False
if "obtener_evento" not in st.session_state:
    st.session_state.obtener_evento = False

st.header("Gestion de Eventos")
tab_add, tab_get, tab_list = st.tabs(["Agregar", "Ver Detalles", "Listar"])

with tab_add:
    
    # Mostrar formulario si está activo
    with st.form("formulario_paciente"):
        st.subheader("Formulario de Registro")
        
        event_name = st.text_input("Nombre de la Consulta")
        date = st.date_input("Fecha de la Consulta",  format= "YYYY-MM-DD")
        time = st.time_input("Hora del Evento")
        paciente = st.text_input("Nombre del Paciente")
        empleado = st.selectbox(label= "Doctor", options= ALL_EMPL) #if ROL in ['admin', 'secretary'] else [USER])
        urgencia = st.checkbox("Es urgencia")
        time_auto = st.checkbox("Seleccionar Fecha automática")
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
        with st.form("Recurso que usara"):
            st.subheader("Formulario de Recurso")
            nombre_rec_event = st.selectbox(label="Nomre Recurso", options=clean_resource_list(ALL_REC, st.session_state.event_resources))
            count_rec_event = st.number_input(label="Cantidad", min_value=1)
            
            submitted_rec = st.form_submit_button("Agregar Otro", use_container_width=True)
            
            if submitted_rec:
                st.session_state.event_resources.append((nombre_rec_event, count_rec_event))
                # st.session_state.mostrar_rec_form = True

    if st.button("Show Info"):
        try:
            st.write(f"Nombre de Consulta: {st.session_state.event["nombre"]}")
            st.write("Recursos usados:")
            for rec in st.session_state.event_resources:
                st.write(rec[0])
        except:
            st.error("No hay info disponible. Debe salvar la info del formulario.")
            st.exception()


    if st.button("Guardar Evento"):
        recs = [item[0] for item in st.session_state.event_resources]
        recs_count = [item[1] for item in st.session_state.event_resources]
        event = st.session_state.event
        response = guardar_evento(event["nombre"], event["date"], event["time"], event["paciente"], event["empleado"],
                    event["urgencia"], recs, recs_count, event["date_time_auto"], event["time_auto"])
        
        st.write("Se creo la Consulta con Exito!!!!")
        st.write(f"Fecha: {response.date}")
        st.write(f"Paciente: {response.owns_name}")
        st.write(f"Doctor: {response.employee}")
        st.success("Guardado correctamente")

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
        st.subheader("Obtener evento")
        id = st.number_input("ID del evento", min_value=0)
        print(f"Id = {id}")
    
        submitted_get_event = st.form_submit_button("Buscar")
        
        if submitted_get_event:
            try:
                evento = obtener_evento(id)
                st.dataframe(evento, height=80)
            except Exception as e:
                st.error(e)