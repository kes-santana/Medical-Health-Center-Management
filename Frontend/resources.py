import streamlit as st

from Frontend.app import ALL_REC
from Frontend.bridge import agregar_no_uso, agregar_uso, crear_recurso, listar_recursos, remover_no_uso, remover_uso, surtir_alamcen
from Frontend.front_utils import clean_resource_list, search_id_by_name

if "create_resource" not in st.session_state:
    st.session_state.create_resource = False
if "list_resources" not in st.session_state:
    st.session_state.list_resources = False
if "remove_use_with" not in st.session_state:
    st.session_state.remove_use_with = False
if "remove_dont_use_with" not in st.session_state:
    st.session_state.remove_dont_use_with = False
if "set_use_with" not in st.session_state:
    st.session_state.set_use_with = False
if "set_dont_use_with" not in st.session_state:
    st.session_state.set_dont_use_with = False

if "suply_storehouse" not in st.session_state:
    st.session_state.suply_storehouse = False
if "suplayed_resources" not in st.session_state:
    st.session_state.suplayed_resources = []
if "suplayed_resources_id" not in st.session_state:
    st.session_state.suplayed_resources_id = []
if "suplayed_resources_count" not in st.session_state:
    st.session_state.suplayed_resources_count = []


st.header("Gestion de Recursos")
tab_add, tab_list, tab_almacen, tab_options = st.tabs(["Agregar", "Listar", "Almacen", "Opciones"])

with tab_add:
    st.header("Crear Nuevo Recurso", divider="blue", width="content")

#Todo: en los "dont_use" lo dejo asi o quito de las opciones los que ya esten en los "use" 

    with st.form("create_resource_form"):
        st.subheader("Crear Recurso")
       
        resource_name = st.text_input("Resource Name")
        resource_count = st.number_input("Count", min_value=1)
        resource_is_spendable =st.checkbox("Is Spendable")
        resource_use_with = st.multiselect("Recursos con los que se debe usar", options=ALL_REC)
        resource_dont_use_with = st.multiselect("Recursos con los que no se debe usar", options=ALL_REC)
        
        submitted_create_rec = st.form_submit_button("Crear", use_container_width=True)
        
        if submitted_create_rec:
            try:
                resource_use_with = search_id_by_name(resource_use_with)
                resource_dont_use_with = search_id_by_name(resource_dont_use_with)
                crear_recurso(resource_name, resource_count, resource_is_spendable, 
                            resource_use_with, resource_dont_use_with)
                st.success("Recurso creado con exito")
            except Exception as e:
                st.error(e)

with tab_list:
    st.header("Listado de Recursos", divider=True, width="content")
    try:
        listed_resources = listar_recursos()
        st.dataframe(listed_resources)
    except Exception as e:
        st.error(e)

with tab_options:

    st.header("Opciones de Recurso", divider="blue", width="content")

    col1, col2 = st.columns([0.5, 0.5])
    with col1:
        st.subheader("Agrear Restricciones", divider="gray")
        contenedor1 = st.container(border=True)
        with contenedor1:
            if st.button("Agregar uso de un recurso respecto a otro"):
                st.session_state.set_use_with = True
        
            if st.session_state.set_use_with:
                with st.form("set_use_with_form"):
                    st.subheader("Agregar uso de un recurso respecto a otro")

                    recurso_dependiente = st.selectbox("Recurso dependiente", options=ALL_REC)
                    recurso_restringido = st.selectbox("Recurso a restringir", options=clean_resource_list(ALL_REC,[recurso_dependiente]))

                    submitted_set_u_w = st.form_submit_button("Aceptar")
                
                    if submitted_set_u_w:
                        recurso_dependiente_id, recurso_restringido_id = search_id_by_name(
                                                                     [recurso_dependiente, recurso_restringido])
                        try:    
                            agregar_uso(recurso_dependiente_id, recurso_restringido_id)
                            st.success("Se ha agregado la restriccion con exito")
                        except Exception as e:
                            st.error(e)

            if st.button("Agregar restriccion de un recurso respecto a otro"):
                st.session_state.set_dont_use_with = True
                
            if st.session_state.set_dont_use_with:
                with st.form("set_dont_use_with_form"):
                    st.subheader("Agregar restriccion de un recurso respecto a otro")

                    recurso_dependiente = st.selectbox("Recurso dependiente", options=ALL_REC)
                    recurso_restringido = st.selectbox("Recurso a restringir", options=clean_resource_list(ALL_REC,[recurso_dependiente]))

                    submitted_set_d_u_w = st.form_submit_button("Aceptar")
                    
                    if submitted_set_d_u_w:
                        recurso_dependiente_id, recurso_restringido_id = search_id_by_name(
                                                                        [recurso_dependiente, recurso_restringido])
                        try:
                            agregar_no_uso(recurso_dependiente_id, recurso_restringido_id)
                            st.success("Se ha agregado la restriccion con exito")
                        except Exception as e:
                            st.error(e)
   
    with col2:
        st.subheader("Eliminar Restricciones", divider="gray")
        contenedor2 = st.container(border=True)
        with contenedor2:

            if st.button("Remover uso de un recurso respecto a otro"):
                st.session_state.remove_use_with = True

            if st.session_state.remove_use_with:
                with st.form("remove_use_with_form"):
                    st.subheader("Remover uso de un recurso respecto a otro")

                    recurso_dependiente = st.selectbox("Recurso dependiente", options=ALL_REC)
                    recurso_restringido = st.selectbox("Recurso restringido", options=clean_resource_list(ALL_REC,[recurso_dependiente]))

                    submitted_remove_u_w = st.form_submit_button("Aceptar")
                    
                    if submitted_remove_u_w:
                        recurso_dependiente_id, recurso_restringido_id = search_id_by_name(
                                                                        [recurso_dependiente, recurso_restringido])
                        try:
                            remover_uso(recurso_dependiente_id, recurso_restringido_id)
                            st.success("Se ha removido la restriccion con exito")
                        except Exception as e:
                            st.error(e)

            if st.button("Remover restriccion de un recurso respecto a otro"):
                st.session_state.remove_dont_use_with = True

            if st.session_state.remove_dont_use_with:
                with st.form("remove_dont_use_with_form"):
                    st.subheader("Remover restriccion de un recurso respecto a otro")

                    recurso_dependiente = st.selectbox("Recurso dependiente", options=ALL_REC)
                    recurso_restringido = st.selectbox("Recurso restringido", options=clean_resource_list(ALL_REC,[recurso_dependiente]))

                    submitted_remove_d_u_w = st.form_submit_button("Aceptar")
                
                    if submitted_remove_d_u_w:
                        recurso_dependiente_id, recurso_restringido_id = search_id_by_name(
                                                                        [recurso_dependiente, recurso_restringido])
                        try:
                            remover_no_uso(recurso_dependiente_id, recurso_restringido_id)
                            st.success("Se ha removido la restriccion con exito")
                        except Exception as e:
                            st.error(e)

with tab_almacen:
    st.header("Almacenamiento de Recursos", divider="blue", width="content")

    with st.form("suply_storehouse_form"):
        st.subheader("Formulario de Recursos a Surtir")

        suplayed_rec = st.selectbox("Recurso a Surtir", options=clean_resource_list(ALL_REC, st.session_state.suplayed_resources))
        suplayed_rec_count = st.number_input("Count", value=0)
    
        submitted_suply = st.form_submit_button("Agregar Otro", use_container_width=True)
        print(suplayed_rec)

        if submitted_suply:
            if suplayed_rec not in st.session_state.suplayed_resources:
                st.session_state.suplayed_resources.append(suplayed_rec)
                st.session_state.suplayed_resources_count.append(suplayed_rec_count)
                st.write(st.session_state.suplayed_resources)
                st.write(st.session_state.suplayed_resources_count)
                
    if st.button("Surtir", use_container_width=True):
        st.session_state.suplayed_resources_id = search_id_by_name(st.session_state.suplayed_resources)
        try:
            surtir_alamcen(st.session_state.suplayed_resources_id, st.session_state.suplayed_resources_count)
            
            st.session_state.suplayed_resources.clear()
            st.session_state.suplayed_resources_count.clear()
            st.session_state.suplayed_resources_id.clear()

            st.success("Se ha surtido el almacen con exito")
        except Exception as e:
            st.error(e)
