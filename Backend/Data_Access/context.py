import json
import os

from Backend.Data_Access.date_manager import DateManager
from Backend.Data_Access.employee_repository import EmployeeRepository
from Backend.Data_Access.resource_repository import ResourceRepository
from Backend.Data_Access.users_repository import UsersRepository
from constants import *

# TODO: arreglar rutas y revisar metodos
# PATH = "..\DataBase"

class Context:
    def __init__(self):
        pass
    
    def save(self, repo):
       data = repo.to_dict()
       
       if type(repo) ==  DateManager:
           name_repo = EVENTS
       elif type(repo) ==  EmployeeRepository:
           name_repo = EMPLOYEES
       elif type(repo) ==  ResourceRepository:
            name_repo = SPENDABLE
       else: 
           name_repo = USERS
           
       root, _ = self._validate_json_size(name_repo)
       with open(root, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _validate_json_size(self, name_repo: str):
        root = os.path.join(
            r"C:\Users\Kevin Emilio\Programación\Python\Projects\Medical-Health-Center-Management\Backend\DataBase",
            f"{name_repo}.json"
        )
        return root, os.path.getsize(root) == 0
    
    def _validate_content(self, root: str) -> dict:
        json_data = {} 
        with open(root, "r", encoding="utf-8") as archivo:
            try:
                json_data = json.load(archivo)
                return json_data
            except json.JSONDecodeError:
                raise Exception("El contenido del JSON no es válido.")

    def get_repo_date_manager(self) -> DateManager:
        root, size_equal_zero = self._validate_json_size(EVENTS)
        if size_equal_zero:
            return DateManager({}, 1)
        json_data: list = self._validate_content(root)       
        return DateManager.from_dict(json_data, self)
    
    def get_repo_resource(self) -> ResourceRepository:
        root, size_equal_zero = self._validate_json_size(SPENDABLE)
        if size_equal_zero:
            return ResourceRepository({})
        data = self._validate_content(root)
        return ResourceRepository.from_dict(data)
    
    def get_repo_employee(self) -> EmployeeRepository:
        root, size_equal_zero = self._validate_json_size(EMPLOYEES)
        if size_equal_zero:
            return EmployeeRepository({})
        json_data = self._validate_content(root)
        return EmployeeRepository.from_dict(json_data)
    
    def get_repo_users(self) -> UsersRepository:
        root, size_equal_zero = self._validate_json_size(USERS)
        if size_equal_zero:
            return UsersRepository()
        json_data: list = self._validate_content(root)       
        return UsersRepository.from_dict(json_data)