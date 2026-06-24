from backend.domain.employee import Employee


class EmployeeDto:
    def __init__(self):
        self.id: int
        self.name: str
        self.experience: int
        self.is_doctor: str
        self.on_vacations: bool
    
    @staticmethod
    def to_employee_dto(employee: Employee) -> "EmployeeDto":
        dto = EmployeeDto()
        dto.id = employee.id
        dto.name = employee.name
        dto.experience = employee.experience
        dto.is_doctor =  employee.is_doctor
        dto.on_vacations = employee.on_vacations
        return dto
    
    def __str__(self):
        return f"Employee: \n \
            Name: {self.name} \n \
            Experience: {self.experience} \n \
            Is Doctor: {self.is_doctor} \n \
            On Vacations: {self.on_vacations} \n"
        