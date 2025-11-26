
from datetime import datetime

from Backend.Data_Access.context import Context
from Backend.Data_Access.employee_repository import EmployeeRepository
from Backend.Domain.resources import Employee


class SetEmployeeVacation:
    def __init__(self, employee_id:str, start_vacation:str, end_vacation: str):
        self.context = Context()
        self.employee_repo: EmployeeRepository = Context.get_repo_employee()
        self.employee: Employee = self.employee_repo.employee_list[employee_id]
        self.start_vacation: datetime = datetime.strptime(start_vacation)
        self.end_vacation: datetime = datetime.strptime(end_vacation)

     # todo ver si va aqui o en employee
    def set_vacations(self) -> None:
        if self.start_vacation<=self.end_vacation:
            self.employee.vacations[0] = self.start_vacation
            self.employee.vacations[1] = self.end_vacation
            self.employee_repo.to_dict()
            print(f'Se han agregado vacaciones al empleado de ID: "{self.employee.id}" desde {self.start_vacation} hasta {self.end_vacation}')
            return
        
        # todo ver si asi o como excepcion
        print("El fin de las vacaciones del empleado debe ser igual o superior al comienzo de las mismas")
        