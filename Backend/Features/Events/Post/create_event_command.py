"""aqui esta lo q se recibe del front"""

import datetime

from Domain.resources import Resource, Employee

class CreateEventComand:
   def __init__(self, date: datetime.date, owns_name: str,
                employee: Employee, urgency: bool, necesary_resources: list[Resource], 
                appointment_name: str =None):
        """Inicializa la clase CreateEventComand"""

        self.date = date
        # self.appointment_name = appointment_name        #todo ver q hacer con esto a futuro
        self.owns_name = owns_name
        self.employee = employee
        self.especiality = employee.especiality
        self.urgency = urgency
        self.duration = employee.productivity()  #todo ver si hay que ponerlo aquí 
        self.necesary_resources = necesary_resources        #todo ver si aquí CreateEventComand hay que poner los recursos necesarios?