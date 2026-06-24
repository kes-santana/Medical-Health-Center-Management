from backend.data_access.context import Context
from backend.features.dtos.employee_dto import EmployeeDto


class ListEmployeesEndpoint:

    def excecute(self):
        context = Context()
        employee_repo = context.get_repo_employee()
        employee_list = employee_repo.get_all()
        return [EmployeeDto.to_employee_dto(e) for e in employee_list]