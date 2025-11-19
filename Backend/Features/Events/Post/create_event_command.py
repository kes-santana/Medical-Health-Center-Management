"""aqui esta lo q se recibe del front"""

class CreateEventComand:
   def __init__(self, date: str, owns_name: str,
                employee_name: str, is_urgency: bool, necesary_resources: list[str], 
                appointment_name: str =None):
        """Inicializa la clase CreateEventComand"""

        self.date: str = date
        # self.appointment_name = appointment_name        #todo ver q hacer con esto a futuro
        self.owns_name: str = owns_name
        self.employee: str = employee_name
        self.is_urgency: bool = is_urgency
        self.necesary_resources: list[str] = necesary_resources        #todo ver si aquí CreateEventComand hay que poner los recursos necesarios? 