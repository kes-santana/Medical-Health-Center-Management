from Backend.Domain.employee import Employee

class EmployeeRepository:
    def __init__(self, employee_list: dict[str, Employee]):
        self.employee_list : dict[str, Employee] = employee_list
        self.count: int = len(employee_list)

    def add_employee(self, employee: Employee) -> None:
        self.employee_list[employee.key] = employee

    def get_all(self, filter=None) -> list:
        if filter is None:
            return [e for e in self.employee_list.values()]
        ans = []
        for e in self.employee_list.values():
            if filter(e):
                ans.append(e)
        return ans

    def get_by_id(self, id: int):
        # Esta claro lo que hace
        items_list: list[Employee] = self.get_all()
        for item in items_list:
            if item.id == id:
                return item
        
        raise Exception(f'El empleado de ID: "{id}" no se encuentra en la base de datos')

    def load_employees_names(self):
        employees_names = []
        for e in self.employee_list.values():
            employees_names.append(e.key)
        return employees_names

    @staticmethod
    def from_dict(data: dict) -> "EmployeeRepository":
        # Cargar del JSON

        employee_list: dict[str, Employee] = {}
        for key, e in data.items():
            employee_list[key] = Employee.from_dict(e)
        return EmployeeRepository(employee_list)                              

    def to_dict(self) -> dict[str, dict]: 
        # Convertir a JSON serializable
        data = {}
        for key, e in self.employee_list.items():
            data[key] = e.to_dict()

        return data
