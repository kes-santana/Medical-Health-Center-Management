import streamlit as st

from Frontend.app import USER, ROL, ID
from Frontend.bridge import cambiar_nombre_de_usuario, cambiar_password_de_usuario

st.header("Gestion de Cuenta")

user_container = st.container(border=True)
with user_container:
    
    col1, col2 = st.columns([0.2, 0.8])
    
    with col1:
        st.write("")
        st.write("")
        st.image("Frontend/assets/user_icon1.jpg",)
    
    with col2:
        USER = st.session_state.app_user
        PASSWORD = st.session_state.app_user_password
        ROL = st.session_state.app_user_rol
        ID = st.session_state.app_user_id

        st.subheader("Perfil de Usuario", divider="blue")
        st.write(f"Usuario: {USER}".title())
        st.write(f"Cargo: {ROL}".title())
        st.write(f"ID: {ID}".title())

st.subheader("Configuracion ⚙️")
opcion_expander = st.expander("User Config")
with opcion_expander:

    user_name_expander = st.expander("Cambiar Nombre de Usuario",icon="👤")
    user_password_expander = st.expander("Cambiar Password de Usuario",icon="🔐")

    with user_name_expander:
        
        with st.form("change_user_name_form"):
            st.subheader("Formulario de cambio de User Name")
            
            user_id = st.number_input("User ID", min_value=1)
            new_user_name = st.text_input("New User Name")
            password = st.text_input("User Password", type="password")
        
            submitted_user_name = st.form_submit_button("Cambiar")

            if submitted_user_name:
                try:
                    cambiar_nombre_de_usuario(user_id, password, new_user_name)
                    USER = new_user_name
                    st.session_state.app_user = new_user_name
                    st.success("Se cambio el nombre de usuario correctamente")
                except Exception as e:
                    st.error(e)
        
    with user_password_expander:

        with st.form("change_user_password_form"):
            st.subheader("Formulario de cambio de User Password")
            
            user_id = st.number_input("User ID", min_value=1)
            new_password = st.text_input("New User password", type="password")
            new_password_copy = st.text_input("Confirm New User password", type="password")
            password = st.text_input("User Password", type="password")
            
            submitted_user_password = st.form_submit_button("Cambiar")

            if submitted_user_password:
                try:
                    cambiar_password_de_usuario(user_id, password, new_password, new_password_copy)
                    PASSWORD = new_password
                    st.session_state.app_user_password = new_password
                    st.success("Se cambio correctamente el user password")
                except Exception as e:
                    st.error(e)
