"""aqui esta lo q se recibe del front"""

class CreateEventCommand:
   def __init__(self, date: str, time: str, owns_name: str,
                employee_id: str, is_urgency: bool, necesary_resources: list[str], 
                asigned_date_time_auto: bool,
                appointment_name: str):
        """Inicializa la clase CreateEventComand"""

        self.date: str = date
        self.time: str = time
        self.asigned_date_time_auto: bool = asigned_date_time_auto
        self.appointment_name = appointment_name
        self.owns_name: str = owns_name
        self.employee: str = employee_id
        self.is_urgency: bool = is_urgency
        self.necesary_resources: list[str] = necesary_resources