import streamlit as st
from Frontend.app import ALL_EMPL
from bridge import cambiar_rol_de_usuario

st.header("Gestion de Sistema")
st.divider()
st.subheader("Administrar Cargos del Personal", divider=True, width="content")

with st.form("change_user_rol_form"):
    st.subheader("Formulario de cambio de User Rol")
    
    user_id = st.selectbox("User", options=ALL_EMPL)
    new_rol = st.selectbox("New User Rol", options=["Admin", "Secretario", "Doctor"])
    password = st.text_input("Admin Password")
    
    submitted_user_rol= st.form_submit_button("Cambiar", use_container_width=True)

    if submitted_user_rol:
        cambiar_rol_de_usuario(user_id, password, new_rol)
        st.success("Se cambio correctamente el user rol")

