import json
from Backend.Domain.resources import Employee

# todo        ver que hago con el on_vacations (solo tiene sentido si hago una automatizacion que 
# todo        al iniciar revise la fecha y actualice el estado dependiendo del resultado)

class EmployeeRepository:
    def __init__(self, employee_list: dict[str, Employee]):
        self.employee_list : dict[str, Employee] = employee_list
        self.count: int = len(employee_list)

    def get_all_filtered(self, predicate = None) -> list:
        if predicate is None:
            return [e for e in self.employee_list.values]
        ans = []
        for e in self.employee_list.values:
            if predicate(e):
                ans.append(e)
        return ans

    def get_by_id(self, id: int):
        # Esta claro lo que hace
        item_finded = None
        items_list: list[Employee] = self.get_all_filtered(predicate=None)
        for item in items_list:
            if item.id == id:
                item_finded = item
                break
        return item_finded

    # todo 
    def save(self, item): 
        pass

    #  todo que sentido tiene cambiarle el estado a un trabajador
    # def change_state(self, id: int, state: str) -> None:    #todo ajustar params del save
    #     item = self.get_by_id(id)
    #     if item != None:
    #         item.state = state
    #         self.save()
        
    #     else: print(f"No se encontro item con ID: {id}")
        


    @staticmethod
    def from_dict(data: dict) -> "EmployeeRepository":
        # Cargar del JSON

        employee_list: dict[str, Employee] = {}
        for key, e in data.items():
            employee_list[key] = Employee.from_dict(e)
        return EmployeeRepository(employee_list, len(employee_list))                              

    # todo hacer q se guarde desde el context
    def to_dict(self) -> dict[str, dict]: 
    # Convertir a JSON serializable
        json_ready = {}
        for key, e in self.employee_list.items():
            json_ready[key] = e.to_dict()

        # todo creo q va en context
        with open("eventos.json", "w", encoding="utf-8") as f:
            json.dump(json_ready, f, indent=2, ensure_ascii=False)
