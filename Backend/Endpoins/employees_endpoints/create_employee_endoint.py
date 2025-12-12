from Backend.Data_Access.context import Context
from Backend.Domain.employee import Employee


class EmployeeCreator:

    def excecute(self, name: str, experience: int, is_doctor: bool):
        context = Context()
        employee_repo = context.get_repo_employee()
        new_employee = Employee(employee_repo.count + 1, name, experience, is_doctor)
        employee_repo[new_employee.key] = new_employee
        context.save(employee_repo)
        print("Se ha creado el empleado")