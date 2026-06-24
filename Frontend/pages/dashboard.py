import datetime
import streamlit as st

from frontend.bridge import employee_ranking, events_per_day, resource_per_month

if "mostrar_graph_1" not in st.session_state:
    st.session_state.mostrar_graph_1 = False
if "mostrar_graph_2" not in st.session_state:
    st.session_state.mostrar_graph_2 = False
if "mostrar_graph_3" not in st.session_state:
    st.session_state.mostrar_graph_3 = False
    
st.header("Start In", divider="blue")
st.write("Bienvenido a su gestor de citas médicas. " \
        "Este panel ha sido diseñado para facilitar su labor diaria. Aquí podrás " \
        "visualizar tus próximas consultas, analizar la demanda de pacientes y acceder " \
        "rápidamente a las herramientas necesarias para organizar tu agenda. " \
        "Nuestro objetivo es dedicar menos tiempo a la gestión y más tiempo a quien en realidad " \
        "lo necesita, el paciente.")

st.divider()

st.header("Tips de Salud", divider="blue")
tip_cont_1 = st.container(border=True)

with tip_cont_1:
    col_1_1, col_1_2, col_1_3 = st.columns([3, 3, 3])
    
    with col_1_1:
        tip_cont_3 = st.container(border=True)
        with tip_cont_3:
            st.subheader("🩺 Promueve chequeos preventivos:")
            st.write("Recordar a los pacientes la importancia de las visitas periódicas ayuda a " \
                    "detectar problemas a tiempo.")
        
    with col_1_2:
        tip_cont_4 = st.container(border=True)
        with tip_cont_4:
            st.subheader("🛏️ Refuerza la importancia del descanso:")
            st.write("Dormir adecuadamente es clave para la recuperacion y la salud mental")

    with col_1_3:
        tip_cont_5 = st.container(border=True)
        with tip_cont_5:
            st.subheader("🚶‍♂️‍➡️ Educa sobre el manejo del estrés:")
            st.write("Técnicas de relajación y mindfulness pueden ser útiles para quienes enfrentan una " \
                "alta carga emocional.")

st.divider()

events_container = st.container(border=True)
with events_container:
    try:  
        st.subheader("Gráfico de Eventos por Día", divider="blue")
        col_1, col_2, col_3 = st.columns([0.2, 0.1, 0.7])
        
        with col_1:
            desde = st.date_input("Fecha desde")
            hasta = st.date_input("Fecha hasta", min_value=desde + datetime.timedelta(days=1))
            graph_type = st.selectbox("Tipo de Gráfico", ["Barras", "Linea"])
            st.session_state.mostrar_graph_1 = st.button("Mostrar")
        
        with col_3:
            with st.container(border=True):
                if st.session_state.mostrar_graph_1:
                    st.plotly_chart(events_per_day(desde, hasta, graph_type.lower()), use_container_width=True)

    except:
        st.error("Hubo un error al graficar")


employee_rank_container = st.container(border=True)
with employee_rank_container:
    try:
        st.subheader("Ranking por Demanda de Doctores", divider="blue")
        col_1, col_2, col_3 = st.columns([0.2, 0.1, 0.7])
        with col_1:
            
            ranking_type = st.selectbox("Tipo de Ranking", ["Día", "Mes", "Año"])
            st.session_state.mostrar_graph_2 = st.button("Mostrar Ranking")
        
        with col_3:
            with st.container(border=True):
                if st.session_state.mostrar_graph_2:
                    st.plotly_chart(employee_ranking(ranking_type.lower()), use_container_width=True, selection_mode="lasso")
   
    except:
        st.error("Hubo un error al graficar")

resource_container = st.container(border=True)
with resource_container:
    try:
        st.subheader("Gráfico de Demanda de Recursos")
        col_1, col_2 = st.columns([0.3, 0.7])
        with col_1:
            fecha = st.date_input("Fecha del mes a a comparar")
            recursos = st.multiselect("Recursos a mostrar", st.session_state.all_rec)
            st.session_state.mostrar_graph_3 = st.button("Mostrar Gráfico")
        
        with col_2:
            with st.container(border=True):
                if st.session_state.mostrar_graph_3:
                    st.plotly_chart(resource_per_month(fecha, recursos), use_container_width=True, selection_mode="lasso")
    
    except Exception as e:
        st.error(e)

st.divider()

st.header("Más Salud", divider="blue")
tip_cont_2 = st.container(border=True)
with tip_cont_2:
    col_2_1, col_2_2, col_2_3 = st.columns([3, 3, 3])
    
    with col_2_1:
        tip_cont_4 = st.container(border=True)
        with tip_cont_4:
            st.subheader("🚵‍♂️ Fomenta hábitos saludables:")
            st.write("Aconsejar sobre sobre la alimentación balanceada y el ejercicio regular mejora " \
                    "la calidad de vida de los pacientes.")
    
    with col_2_2:
        tip_cont_4 = st.container(border=True)
        with tip_cont_4:
            st.subheader("💧 Motiva la hidratación:")
            st.write("Recomendar a los pacientes beber suficiente agua contribuye a su bienestar general")
    
    with col_2_3:
        tip_cont_4 = st.container(border=True)
        with tip_cont_4:
            st.subheader("💉 Incentiva la vacunación:")
            st.write( "Recordar a los pacientes mantener al día sus esquemas de vacunacion foralece la " \
                "prevención de enfermedades y contribuye a la salud pública.")
