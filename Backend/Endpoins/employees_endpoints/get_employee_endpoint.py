
from backend.data_access.context import Context
from backend.features.dtos.employee_dto import EmployeeDto


class GetEmployeeEndpoint:

    def excecute(self, employee_id: int):
        context = Context()
        employee_repo = context.get_repo_employee()
        employee = employee_repo.get_by_id(employee_id)
        return EmployeeDto.to_employee_dto(employee)