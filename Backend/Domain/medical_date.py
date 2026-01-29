import datetime

from Backend.Data_Access.employee_repository import EmployeeRepository
from Backend.Data_Access.resource_repository import ResourceRepository
from Backend.Domain.resources import Resource
from Backend.Domain.employee import Employee



class MedicalDate:
    """Representa cada cita medica"""

    def __init__(self, id: int, date_time: datetime.datetime,owns_name: str, employee: Employee,
                 is_urgency: bool, necesary_resources: list[Resource], resources_count: list[int], appointment_name: str):
        """Inicializa la clase MedicalDate"""

        self.id: int = id
        self.date_time: datetime.datetime = date_time
        self.owns_name: str = owns_name
        self.employee: Employee = employee
        # self.especiality: str = employee.especiality
        self.is_urgency: bool = is_urgency
        self.duration: datetime.time = employee.productivity()
        self.necesary_resources: list[Resource] = necesary_resources
        self.resources_count: list[int] = resources_count
        self.state: str = "active"
        self.appointment_name = appointment_name

    def to_dict(self) -> dict:
        """Convierte la cita medica a un diccionario"""

        return {
            "id": self.id,
            "date_time": self.date_time.isoformat(),
            "owns_name": self.owns_name,
            "employee": self.employee.id,
            # "especiality": self.especiality,
            "is_urgency": self.is_urgency,
            "duration": self.duration.isoformat(),
            "necesary_resources": [resource.id for resource in self.necesary_resources],
            "resources_count": self.resources_count,
            "state": self.state,
            "appointment_name": self.appointment_name
        } 

    @staticmethod
    def from_dict(data: dict, context) -> "MedicalDate":
        resource_repo: ResourceRepository = context.get_repo_resource()
        employee_repo: EmployeeRepository = context.get_repo_employee()

        # Convertir fechas
        date_time = datetime.datetime.strptime(data["date_time"], "%Y-%m-%dT%H:%M:%S")
        
        # Reconstruir objetos Employee y Resource
        recursos =[resource_repo.get_by_id(r) for r in data["necesary_resources"]]

        employee = employee_repo.get_by_id(data["employee"])

        return MedicalDate(
            id = data["id"],
            date_time = date_time,
            owns_name = data["owns_name"],
            employee = employee,
            is_urgency = data["is_urgency"],
            necesary_resources = recursos,
            resources_count = data["resources_count"],
            appointment_name = data["appointment_name"]
        )
