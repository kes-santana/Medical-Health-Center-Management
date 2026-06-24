
from datetime import datetime

from backend.data_access.context import Context
from backend.data_access.employee_repository import EmployeeRepository
from backend.domain.employee import Employee


class EmployeeVacationsSeterEndpoint:

    def excecute(self, employee_id: int, start_vacation: datetime.date, end_vacation: datetime.date) -> None:
        context = Context()
        employee_repo: EmployeeRepository = context.get_repo_employee() 
        manager = context.get_repo_date_manager()
        print([(x.key, x.id) for x in employee_repo.employee_list.values()])
        employee: Employee = employee_repo.get_by_id(employee_id)
        employee.set_vacations(start_vacation, end_vacation, manager.list_of_events)
        context.save(employee_repo)
        print(f'Se han agregado vacaciones al empleado de ID: "{employee.id}" desde {start_vacation} hasta {end_vacation}')
    