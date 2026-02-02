"""aqui esta lo q se recibe del front"""

class CreateEventCommand:
   def __init__(self, date: str, time: str, owns_name: str,
                employee_id: int, is_urgency: bool, necesary_resources: list[int], 
                resources_count: list[int], asigned_date_time_auto: bool,
                appointment_name: str, time_auto: bool):
        """Inicializa la clase CreateEventComand"""

        self.date: str = date
        self.time: str = time
        self.asigned_date_time_auto: bool = asigned_date_time_auto
        self.appointment_name = appointment_name
        self.owns_name: str = owns_name
        self.employee: int = employee_id
        self.is_urgency: bool = is_urgency
        self.time_auto: bool = time_auto
        self.necesary_resources: list[int] = necesary_resources
        self.resources_count: list[int] = resources_count