
from Backend.Data_Access.context import Context
from Backend.Features.dtos.employee_dto import EmployeeDto


class GetEmployeeEndpoint:

    def excecute(self, employee_id: int):
        context = Context()
        employee_repo = context.get_repo_employee()
        employee = employee_repo.get_by_id(employee_id)
        return EmployeeDto.to_employee_dto(employee)