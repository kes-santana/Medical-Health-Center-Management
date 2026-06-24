from backend.data_access.context import Context
from backend.domain.employee import Employee


class EmployeeCreatorEndpoint:

    def excecute(self, name: str, experience: int, is_doctor: bool):
        context = Context()
        employee_repo = context.get_repo_employee()
        new_employee = Employee(employee_repo.count + 1, name, experience, is_doctor)
        employee_repo.add_employee(new_employee)
        context.save(employee_repo)
        print("Se ha creado el empleado")
        return new_employee