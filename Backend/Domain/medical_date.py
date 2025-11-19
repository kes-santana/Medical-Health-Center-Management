import datetime

from Backend.Domain.resources import Employee, Resource



class MedicalDate:
    """Representa cada cita medica"""

    def __init__(self, id: int, date: datetime.date, time: datetime.time, created_at: datetime.datetime,
                owns_name: str, employee: Employee, is_urgency: bool, necesary_resources: list[Resource], 
                appointment_name: str =None):
        """Inicializa la clase MedicalDate"""

        self.id: int = id
        self.date: datetime.date = date
        self.time: datetime.time = time
        self.created_at: datetime.datetime = created_at
        # self.appointment_name = appointment_name        #todo ver q hacer con esto a futuro
        self.owns_name: str = owns_name
        self.employee: Employee = employee
        self.especiality: str = employee.especiality
        self.is_urgency: bool = is_urgency
        self.duration: datetime.time = employee.productivity()
        self.necesary_resources: list[Resource] = necesary_resources
        self.state: str = "active"

    def to_dict(self) -> dict:
        """Convierte la cita medica a un diccionario"""

        return {
            "id": self.id,
            "date": self.date.isoformat(),
            "time": self.time.isoformat(),
            "owns_name": self.owns_name,
            "employee": self.employee.to_dict(),
            "especiality": self.especiality,
            "is_urgency": self.is_urgency,
            "duration": self.duration.isoformat(),
            "necesary_resources": [resource.to_dict() for resource in self.necesary_resources],
            "state": self.state
        }