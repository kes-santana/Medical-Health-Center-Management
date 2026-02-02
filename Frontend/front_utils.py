from Backend.Data_Access.context import Context
import os
import json

from Backend.Data_Access.resource_repository import ResourceRepository
from constants import SPENDABLE, EMPLOYEES

# todo cambiar el context solo por json
def clean_resource_list(all_rec: list[str], my_rec: list[str]) -> list[str]:
    s_all_rec = set(all_rec)
    if len(my_rec) == 0:
        return all_rec
    if type(my_rec[0]) == str:
        my_rec = set(my_rec)
    else:
        my_rec = set([item[0] for item in my_rec])
    return list(s_all_rec - my_rec)

# TODO: revisr si esta bien y arreglar los otros (ver si hay q hacerlo mas abstracto leyendo directo de json_data)
def load_rec_names() -> list[str]:
    root, size = validate_json_size(SPENDABLE)
    
    if size == 0:
        return []
    
    json_data = validate_content(root)
    resource_repo = ResourceRepository.from_dict(json_data)
    resources_names = []
    for r in resource_repo.resource_list.values():
        if r.count > 0:
            resources_names.append(r.key)
    
    return resources_names

def load_emp_names() -> list[str]:
    context = Context()
    employee_repo = context.get_repo_employee()
    employees_names = [employee.key for employee in employee_repo.employee_list.values()]
    return employees_names

def search_id_by_name(resources_names: list[str]) -> list[int]:
    resources_id = []
    for name in resources_names:
        resources_id.append(int(name.split(" ")[0]))
    return resources_id

def validate_json_size(name_repo: str):
    root = os.path.join(
        r"C:\Users\Kevin Emilio\Programación\Python\Projects\Medical-Health-Center-Management\Backend\DataBase",
        f"{name_repo}.json")
    return root, os.path.getsize(root)

def validate_content(root: str) -> dict:
    json_data = {}
    with open(root, "r", encoding="utf-8") as archivo:
        try:
            json_data = json.load(archivo)
            return json_data
        except json.JSONDecodeError:
            raise Exception("El contenido del JSON no es válido.")