# aqui se definen las tareas

## Endpoint RefreshSystem

0. Rellamar a las funciones de obtener nombres

1. Ve por cada evento que no tenga etiqueta de Finalizado y le cambias la etiqueta si y solo si la fecha actual > que la fecha de finalizacion del evento.

2. Sea E un evento cambiado. Vas por todos los recursos de E y haces lo siguiente:
- Si el recurso es gastable, sigue tu camino
- Si no, repon en base de datos

3. Sea E un empleado. Si en la fecha actual el empleado cae en vacaciones, actualizar la etiqueta de OnVacations

## Implementar Front de Obtener detalles de eventos

## * Implementar Listar con Filtro
1. Frontend: Crea un formulario con string query y dos fechas (desde, hasta) y ejecutar
2. Backend: Obtienes todos los eventos tal que (name in query or doctor in query or paciente in query) and date between desde, hasta
 

### Para que la app quede como un componente view la primera parte de app.py es todo lo que llama al backend, la segunda es las cosas que estan en la ssesion_state y la tercera parte es la logica

### Arreglar en el back la entrada de fecha y hora en crear eventos y donde quiera q haga falta teniendo en cuenta el formato de entrada

### ver si hay que limpiar variables al hacer submit o al hacer refresh, ademas en el refresh debo recoger todos los formularios

### arreglar change_state

### agregar el rango de fechas al list 
### hacer endpoint de cambiar manager y secretario y de crear usuario

## Modularizar los accees_endpoints en command, handler y response
