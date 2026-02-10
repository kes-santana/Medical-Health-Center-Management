import streamlit as st

st.header("Acerca de la app", divider="blue")

st.write("El gestor de eventos Mediacal Health Center Management es un sistema " \
        "desarrollado para clínicas de salud con el objetivo de optimizar el proceso " \
        "de agendamiento de citas, reduciendo tiempos de espera y mejorando la organización " \
        "de la información. Asimismo, permite manejar la disponiblidad de recursos sanitarios " \
        "y el método de empleo de estos facilitando a doctores la gestion de los mismos.")

st.subheader("Sección Eventos", divider="blue", width="content")
st.write('En esta sección encontrará multiples herramientas. En el apartado "Agregar" podrá ' \
        'agendar nuevas citas a su cronograma de consultas. tenga en cuenta que solo puede agendar ' \
        'citas con fechas posteriores a la fecha del día en que se crea la misma. En "Ver Detalles" podrá ' \
        'ver información de una cita agendada según el ID de la misma. En "Listar" podrá buscar todas las ' \
        'citas que tengan en su información alguna coincidencia con el aspecto de su búsqueda. Finalmente ' \
        'en "Cambiar Estado" puede cambiar el estado de una cita "activa" a "finalizada" o "cancelada".')

st.subheader("Sección Empleados", divider="blue", width="content")
st.write('En la sección encontrará opciones como "Crear Empleados", "Ver Detalles" y "Listar" todas ' \
        'con funciones parecidas a las de la "Sección Eventos". Además encontrará una funcionalidad ' \
        'llamada "Vacaciones" con la cual podrá asignar vacaciones a los empleados.')

st.subheader("Sección Recursos", divider="blue", width="content")
st.write('En esta sección al igual que en las anteriores encontrará las funciones de "Agregar", ' \
        '"Ver Detalles" y "Listar". Se agregan dos nuevas funcionalidades: "Almacén" y "Opciones". ' \
        'Con la primera podrá surtir el almacén con recursos ya existentes y eliminar recursos ' \
        'defectuosos, mientras que con la segunda podrá cambiar las opciones de uso de cada recurso ' \
        'respecto a otros tanto para hacer que dos recursos tengan que usarse juntos, como ' \
        'para hacer que estos no puedan hacerlo.')


st.subheader("Sección User", divider="blue", width="content")
st.write('En esta sección encontrará todo lo relacionado con su cueta, dándole la posibilidad ' \
        'de hacer los cambios que desee tanto en su nombre de usuario como en su contraseña.')


st.subheader("Sección System", divider="blue", width="content")
st.write('En este apartado podrá asignar nuevos cargos a los empleados de la clínica.')

st.subheader("Observaciones", divider="blue")
st.write('- Tenga en cuenta que solo podrá acceder a las secciones de recursos, empleados y ' \
        'sistema si es administrador de la clínica.')

st.write('- Se recomienda que al crear un nuevo empleado o recurso se actualice la sesión mediante ' \
        'el botón "Refresh".')