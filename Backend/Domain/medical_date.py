import datetime

from Backend.Domain.resources import Employee, Resource



class MedicalDate:
    """Representa cada cita medica"""

    def __init__(self, id: int, date_time: datetime.datetime,owns_name: str, employee: Employee,
                 is_urgency: bool, necesary_resources: list[Resource], appointment_name: str):
        """Inicializa la clase MedicalDate"""

        self.id: int = id
        self.date_time: datetime.datetime = date_time
        self.owns_name: str = owns_name
        self.employee: Employee = employee
        # self.especiality: str = employee.especiality
        self.is_urgency: bool = is_urgency
        self.duration: datetime.time = employee.productivity()
        self.necesary_resources: list[Resource] = necesary_resources
        self.state: str = "active"
        self.appointment_name = appointment_name

    def to_dict(self) -> dict:
        """Convierte la cita medica a un diccionario"""

        return {
            "id": self.id,
            "date_time": self.date_time.isoformat(),
            "owns_name": self.owns_name,
            "employee": self.employee.to_dict(),
            # "especiality": self.especiality,
            "is_urgency": self.is_urgency,
            "duration": self.duration.isoformat(),
            "necesary_resources": [resource.to_dict() for resource in self.necesary_resources],
            "state": self.state,
            "appointment_name": self.appointment_name
        } 

    @staticmethod
    def from_dict(data: dict) -> "MedicalDate":
        # Convertir fechas
        date_time = datetime.datetime.strptime(data["date_time"], "%Y-%m-%dT%H:%M")
        
        # Reconstruir objetos Employee y Resource
        empleado = Employee.from_dict(data["employee"])
        recursos = [Resource.from_dict(r) for r in data["necesary_resources"]] 

        return MedicalDate(
            id = data["id"],
            date_time = date_time,
            owns_name = data["owns_name"],
            employee = empleado,
            is_urgency = data["is_urgency"],
            necesary_resources = recursos,
            appointment_name = data["appointment_name"]
        )
