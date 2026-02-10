# Medical-Health-Center-Management

El gestor de eventos **Mediacal Health Center Management** es un sistema desarrollado para clínicas de salud con el objetivo de optimizar el proceso de agendamiento de citas, reduciendo tiempos de espera y mejorando la organización de la información. Asimismo, permite manejar la disponiblidad de recursos sanitarios y el método de empleo de estos facilitando a doctores la gestión de los mismos, ejemplo de esto el uso de jeringas las cuales por higiene deben usarse con nasobucos y guantes.

## Instalación y tecnologías

El proyecto esta en su totalidad desarrollado en *Python* *version 3.13.2* y se recomienda el uso de un *virtual environment*. 

### Requerimientos:


Usa bibliotecas externas como *streamlit* y *ploty.express* las cuales se pueden intalar mediante los comandos:

 - `pip install streamlit `
 - `pip install ploty.express`

 Cumplidos estos requerimentos, para ejecutar el programa es necesrio abrir una terminal y ejecutar los siguientes comandos:

- `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`
- `.\run.ps1 `

Este último se encargará de ejecutar un script PowerShell `run.ps1` que activará el entorno virtual y ejecutará el sript `app.py` dando inicio al programa.

## Implementaciones

Se ha puesto a disposición del usario gran variedad de herramientas para facilitar la gestión de eventos, siendo parte fundamental de esto evitar colisiones entre horarios, buscar espacios para citas y el tratado de urgencias, así como la gestión de los recursos disponibles y la disponibilidad de los doctores.


