import streamlit as st

from bridge import cambiar_rol_de_usuario

st.header("Gestion de Sistema")
st.divider()
st.subheader("Administrar Cargos del Personal", divider=True, width="content")

with st.form("change_user_rol_form"):
    st.subheader("Formulario de cambio de User Rol")
    
    employee_id: str = st.selectbox("User", options=st.session_state.all_empl)
    new_rol = st.selectbox("New User Rol", options=["Admin", "Secretario", "Doctor"])
    password = st.text_input("Admin Password", type="password")
    
    submitted_user_rol= st.form_submit_button("Cambiar", use_container_width=True)

    if submitted_user_rol:
        try:
            cambiar_rol_de_usuario(st.session_state.app_user_id, employee_id, password, new_rol.lower())
            print(st.session_state.app_user_id)
            print(type(st.session_state.app_user_id))
            print(int(employee_id.split(" ")[0]))
            st.success("Se cambio correctamente el user rol")
            if  st.session_state.app_user_id == int(employee_id.split(" ")[0]):
                st.session_state.clear()
                st.rerun()
            
        except Exception as e:
            st.error(e)