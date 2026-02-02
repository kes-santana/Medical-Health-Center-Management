
from datetime import datetime, date

from Backend.Data_Access.context import Context
from Backend.Data_Access.employee_repository import EmployeeRepository
from Backend.Domain.employee import Employee


class EmployeeVacationsSeterEndpoint:

    def excecute(self, employee_id: int, start_vacation: datetime.date, end_vacation: datetime.date) -> None:
        context = Context()
        employee_repo = context.get_repo_employee() 
        print([(x.key, x.id) for x in employee_repo.employee_list.values()])
        employee: Employee = employee_repo.get_by_id(employee_id)
        employee.set_vacations(start_vacation, end_vacation)
        context.save(employee_repo)
        print(f'Se han agregado vacaciones al empleado de ID: "{employee.id}" desde {start_vacation} hasta {end_vacation}')
    