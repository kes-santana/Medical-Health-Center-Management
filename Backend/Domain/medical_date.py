import datetime

from resources import Employee
from resources import Resource

class MedicalDate:
    """Representa cada cita medica"""

    def __init__(self, id: int, date: datetime.date, time: datetime.time, owns_name: str, employee: Employee,
                 urgency: bool, necesary_resources: list[Resource], appointment_name: str =None):
        """Inicializa la clase MedicalDate"""

        self.id: int = id
        self.date: datetime.date = date
        self.time: datetime.time = time
        # self.appointment_name = appointment_name        #todo ver q hacer con esto a futuro
        self.owns_name: str = owns_name
        self.employee: Employee = employee
        self.especiality: str = employee.especiality
        self.urgency: bool = urgency
        self.duration: datetime.time = employee.productivity()
        self.necesary_resources: list[Resource] = necesary_resources
        self.state: str = "active"
