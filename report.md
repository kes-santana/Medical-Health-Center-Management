# Medical-Health-Center-Management 
	
El gestor de eventos Medical Health Center Management es un sistema desarrollado para clínicas de salud con el objetivo de optimizar el proceso de planificación de citas, reduciendo largos tiempos de espera y mejorando la organización de la información. Asimismo, permite manejar la disponibilidad de recursos sanitarios y el método de empleo de estos, facilitando a doctores la gestión de los mismos.
	
Se ha escogido el sector de la salud dada la problemática que presentan varios de estos centros públicos: la mala organización del tiempo y los recursos, la que afecta directamente a los pacientes creando tiempos de espera más largos y carencias para tratar los padecimientos de los mismos. 
		
	
## Instalación y tecnologías
	
El proyecto está desarrollado en su totalidad  en *Python* (versión 3.13.2) y se recomienda el uso de un *virtual environment*.
	

### Requerimientos

Leer archivo *requirements.txt* adjunto al archivo.
	
Cumplidos estos requerimentos, para ejecutar el programa solo es necesario ejecutar el script *main.py* el cual activará el virtual environment y ejecutará la app.

	
## Diseño
	
Se usa Clean Architecture junto a principios SOLID para obtener mejor mantenimiento, escalabilidad y separar claramente las responsabilidades del código, para obtener de esta forma mayor vida útil del software, asegurando así, mayor facilidad para pruebas unitarias y añadir nuevas funcionalidades. Además se usa un patrón MVVM para separar la lógica del programa de la interfaz gráfica.
	
La experiencia de usuario y el diseño de interfaz de usuario (UX-UI) se centra en dar una experiencia intuitiva del uso de las funciones implementadas  usando un diseño minimalista priorizando la accesibilidad y claridad de navegación junto a consistencia en los botones y retroalimentación visual inmediata. Además, se escoge una paleta de colores asociada a clínicas de salud haciendo un llamado a la limpieza y la higiene.
	
La base del proyecto está dirigida a la planificación de citas y a la gestión de recursos, dado esto, se ha decidido escoger como estructura de datos principal el diccionario debido a su rapidez de indexado y su versatilidad de uso. Para la gestión de citas se utiliza un diccionario que reune fechas como llaves y un nuevo diccionario como valor, el cual contiene a los doctores como llaves y sus respectivas citas como valores. Respecto a la gestión de recursos se utiliza un diccionario que contiene el inventario disponible en la clínica. En ambos diccionarios se utiliza como llave el *ID* de los doctores y de los recursos para minimizar tiempos de búsqueda.
	
Se decide usar programación orientada a objetos para facilitar el desarrollo del programa y tener acceso a particularidades propias de este paradigma tales como la modularización, la reutilización y escalabilidad del código. Como núcleo del sistema se crean clases de más bajo nivel tales como "MedicalDate", "Resources", "Employee", mientras que, a un nivel por encima se crea "DateManager", clase central del proyecto encargada de la organización del sistema de planificación de citas médicas.
	
### Eventos
	
Para mayor optimización del tiempo y dar mayor realismo a la problemática, se decide gestionar citas médicas que abarcan un cierto espacio de tiempo y utilizan los recursos almacenados.
	
### Recursos
	
Los recursos manejados son los que se utilizan en una consulta médica estandar, lo que implica que se cumplan determinadas condiciones para su correcto uso y prevención de riesgos. 
	
### Cantidades
	
Para  que un recurso pueda usarse lo principal es que en el almacén exista la cantidad solicitada de dicho recurso. Además, se manejan los casos particulares de los recursos reutilizables, los cuales se debe verificar para su uso, que para el momento de la cita médica este disponible la cantidad deseada.
	
#### Restricción de Co-requisito o Inclusión
	
Exieten recursos que para ser usados en una cita es necesario usarlos junto con otros específicos debido a la codependencia generada entre estos o simplemente por la protección e higiene requerida en los procedimientos en los que estos son utilizados.
	
#### Restricción de Exclusión Mutua
	
Exieten recursos que para ser usados en una cita es necesario que en la misma no se usen otros recursos específicos por seguridad o incompatbilidad entre estos.
	
    
- En ambas restricciones se contempla el caso en que un recurso A deba usarse con un recurso B y a su vez no deba usarse con un recurso C, pero que el recurso B dependa directamente del recurso C. Estos casos se han restringido por defecto, y, se le da al usuario la oportunidad de cambiar  las restricciones de uso de los anteriores recursos citados para minimizar situaciones de este tipo.
    

## Implementaciones
	
Se pone a disposición del usuario gran variedad de herramientas para facilitar la gestión de eventos, siendo parte fundamental de esto evitar colisiones entre horarios, buscar espacios para citas y el tratado de urgencias, así como la gestión de los recursos disponibles y la disponibilidad de los doctores.
	
    
### Eventos

Se ha implementado un sistema que además de programar nuevas citas médicas es capaz de listar las ya existentes, ver detalles sobre una cita específica y cambiar el estado de estas.
Se ha tenido en cuenta la posibilidad de programar citas para el primer espacio disponible en el día así como la posibilidad de programar una cita en el primer espacio libre en la agenda general de un doctor determinado. Además se manejan conflictos como la ausencia del doctor solicitado para el día de la consulta.
	
El sistema trata de forma diferenciada citas comunes y urgentes, dándole prioridad a las últimas y desplazando hacia horas posteriores las comunes que se solapen en el intervalo de tiempo.
	

### Recursos
Dada la importancia de los recursos para una clínica se implementaron herramientas para crear nuevos recursos, además de listar y ver detalles de los ya existentes. Se agregó la posibilidad de surtir recursos al almacén asi como  la de añadir y eliminar restricciones sobre los mismos. 
	

### Empleados
	
Atendiendo a la importancia de los doctores en el sistema de salud, se implementaron medidas para contratar nuevos doctores, listar a los existentes y ver información detallada sobre cada uno de estos.
	
### Otras funciones
	
Además, se agregaron las siguientes funciones:
	
- El sistema provee a cada empleado de una cuenta personal para tratar sus citas, dando la posibilidad de administrar la información de su perfil de usuario.
	
- Se implementó la posibilidad de asignar a cada empleado un nuevo papel en la clínica, dándole a estos mayores facultades en el sistema de administración.

- El sistema tiene la posibilidad de graficar la cantidad de citas diarias y la cantidad de pacientes que posee un empleado en un transcurso de tiempo determinado.

	
## Aprendizaje durante el desarrollo del proyecto

Durante el desarrollo se tuvo en cuenta el trabajo con librerías externas a *Python* para obtener mejores resultados del programa.

En el backend se priorizó el uso de librerías que trabajan con el tiempo como *Datetime* y *Calendar* demandando el aprendizaje de estas para un mejor resultado, dado que esta es la problemática principal que se debe resolver. De igual forma, se utiliza *plotly-express*, librería para el trabajo con gráficos y datos, siendo un aspecto a estudiar.

Para el frontend se utiliza la librería *streamlit* la cual por su valor y complejidad fue de vital importacia la adaptación a su modo de uso para la obtención de una mejor calidad y una mejor experiencia de trabajo del usario.

## Dificultades encontradas

Dada la problemática planteada respecto a la máxima optimización del tiempo y los     recursos, uno de los problemas encontrados es la organización de las citas médicas y los recursos requeridos por estas. Debido al trato realista del tiempo, donde se establecen hora y minutos determinados para las consultas, y la posible cancelación de las mismas, se toma la decición de organizar las citas mediante un parámetro *active* teniendo al comienzo las citas activas y al final las canceladas o finalizadas.

Se toma la decición de crear citas médicas de carácter urgente las cuales al momento de agregar esta funcionalidad, se decidió, poner al comienzo del día las urgencias y las demás citas a continuación de estas. Por comodidad del trabajo se impuso la normativa de solo planificar urgencias hasta las 12:00 pm, esto se debe a que, por el carácter de estas, se agregaban al comienzo de la lista sin revisar a fondo otros detalles, lo que generaba una lista infinita de urgencias en caso de solo programar citas de este tipo en un día o que no existiera capacidad para citas de carácter común. También debido a la existencia de estas consultas, por el peso que tienen sobre las comunes, surge un alto índice de exitencia de solapamientos. Esta problemática se debe a que al agregar las urgencias al comienzo del día, y la posible existencia de citas comunes en horarios cercano se terminen solapando los mismos. Esto se resolvió reorganizando la lista de citas después de insertar la urgencia médica al final de la lista de urgencias.
 
Cabe destacar que por problemas logísticos de mayor peso se decide solo crear citas con un día o más de antelación y nunca el mismo día. Además las citas planificadas con mayor antelación tienen mayor peso respecto a los productos que utilizan por sobre otras, es decir, por ejemplo, si una cita es programada el lunes para desarrollarse el viernes, y otra se programa el martes para desarrollarse el jueves, y ambas necesitan un recurso específico, solo se planificará la segunda cita del ejemplo si hay disponibilidad de ese recurso, en caso contrario se denegará la creación de la cita.
 
## Modo de uso
 
El uso del programa es en su totalidad intuitivo. A continuación se propone un ejemplo de uso de cada característia del mismo.
 
Al momento de acceder al programa usted se encontrará con una página de inicio de sesión, que le mostrará un resumen de las consultas  de la clínica correspondientes al mes en curso. Para acceder por primera vez se ha creado el super usuario *admin* y su contraseña es *admin*.
 
Después de eso usted tendrá accesso al sistema como administrador y deberá crear su cuenta personal y, por seguridad cambiar la contraseña del administrador. Para esto dirijase a la sección *Empleados* que se encuentra en la barra lateral de opciones y dirijase a la pestaña *Crear*. Aquí deberá rellenar el formulario solicitado, y terminado esto, se creará su nueva cuenta. Se debe precisar que, el proceso es el mismo para agregar a otros empleados y solo lo podrá hacer si tiene acceso como administrador, además los usarios recién creados tendrán como nombre *nuevo_empleado_nombre_del_empleado* en minúsculas y guión bajo, y como contraseña *0123456789*. 
 
Luego para cambiar la información de la cuenta debe dirigirse a la sección *User*, donde verá los detalles de su usuario, junto a las opciones de las que dispone.
 
Después de esto usted podrá comenzar a trabajar en el sistema sin ningún problema.
 
En la sección *Dashboard* encontrará la página principal del programa donde podrá observar variada información.
 
En la  sección *Eventos* podrá agregar, listar, ver detalles y cambiar el estado de los eventos. A continuación un breve ejemplo de uso.
Primero rellenamos el formulario principal y pulsamos el botón *Salvar*. Luego agregamos los recursos que necesitaremos para la cita médica y por cada uno pulsaremos el botón *Agregar* y luego el botón *Show info* para ver los dealles guardados hasta el momento. Para culminar presionaremos el botón *Guardar* Evento y, si los datos son válidos se habrá creado correctamente la consulta médica.
  
Para ver detalles más específicos de algún evento vaya a la pestaña *Ver detalles*, introduzca el  *ID* del evento deseado y presione el botón *Buscar*.
 
Para listar los eventos simplemente se debe ir a la pestaña y presionar el botón correspondiente.
 
Para cambiar el estado de los eventos simplemente vaya a la pestaña requerida, rellene el formulario y presione  *Cambiar*.
 
En las secciones *Empleados* y *Recursos* encontrará un menú de opciones parecido al de *Eventos*. Simplemente debe llenar los formularios requeridos para completar las acciones deseadas.
 
Finalmente, en la sección *System* podrá cambiar el tipo de acceso que tendrán los usuarios. Debe tener en cuenta que los usuarios con acceso de doctor solo podrán programar sus propias citas, los que tengan acceso de secretario podrán programar citas de cualquier doctor y los administradores tendrán acceso global al sistema.	
	