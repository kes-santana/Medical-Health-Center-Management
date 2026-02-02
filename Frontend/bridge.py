
import datetime
from Backend.Domain.employee import Employee
from Backend.Endpoins.acces_endpoints.change_user_name_endpoint import ChangeUserNameEndpoint
from Backend.Endpoins.acces_endpoints.change_user_password_endpoint import ChangeUserPasswordEndpoint
from Backend.Endpoins.acces_endpoints.change_user_rol_endpoint import ChangeUserRolEndpoint
from Backend.Endpoins.acces_endpoints.create_user_endpoint import CreateUserEndpoint
from Backend.Endpoins.acces_endpoints.login_endpoint import LoginEndpoint
from Backend.Endpoins.employees_endpoints.create_employee_endoint import EmployeeCreatorEndpoint
from Backend.Endpoins.employees_endpoints.list_employees_endpoint import ListEmployeesEndpoint
from Backend.Endpoins.employees_endpoints.set_employee_vacations_endpoint import EmployeeVacationsSeterEndpoint
from Backend.Endpoins.events_endpoints.create_event_endpoint import CreateEventEndpoint
from Backend.Endpoins.events_endpoints.get_event_endpoint import GetEventEndpoint
from Backend.Endpoins.events_endpoints.list_events_endpoint import ListEventEndpoint
from Backend.Endpoins.resources_endpoints.create_resource_endpoint import ResourceCreatorEndpoint
from Backend.Endpoins.resources_endpoints.list_resources_endpoint import ListResourcesEndpoint
from Backend.Endpoins.resources_endpoints.remove_dont_use_with_endpoint import RemoveDontUseWithEndpoint
from Backend.Endpoins.resources_endpoints.remove_use_with_endpoint import RemoveUseWithEndpoint
from Backend.Endpoins.resources_endpoints.set_new_dont_use_with_endpoint import SetNewDontUseWithEndpoint
from Backend.Endpoins.resources_endpoints.set_new_use_with_endpoint import SetNewUseWithEndpoint
from Backend.Endpoins.resources_endpoints.suply_storehouse_endpoint import SuplyStorehouseEndpoint
from Backend.Endpoins.refresh_system_endpoint import RefreshSystemEndpoint
from Backend.Features.Events.Get.get_event_response import GetEventResponse
from Backend.Features.Events.Post.create_event_response import CreateEventResponse
from Backend.Features.dtos.employee_dto import EmployeeDto
from Backend.Features.dtos.eventdto import EventDto
from Backend.Features.dtos.resource_dto import ResourceDto
from Frontend.front_utils import search_id_by_name

# Función que recibe los datos del formulario
def verify_login(user_input, password_input) -> tuple[bool, str, str]:
   endpoint = LoginEndpoint()
   return endpoint.excecute(user_input, password_input)

def guardar_evento(nombre, date, time, paciente, empleado: str, urgencia,
                   recursos_nacesarios, recs_count, date_time_auto, time_auto) -> CreateEventResponse:
    
    
    recursos = search_id_by_name(recursos_nacesarios)
    endpoint = CreateEventEndpoint()
    return endpoint.excecute(date, time, paciente, int(empleado.split(' ')[0]), urgencia, 
                                 recursos, recs_count, date_time_auto, nombre, time_auto)
   
def listar_eventos(query: str) -> list[dict]:
    endpoint = ListEventEndpoint()
    listed_events: list[EventDto] = endpoint.excecute(query)
    filas = [ 
        {"ID": event.id, "Doctor": event.doctor, "Paciente": event.patient, "Consulta": event.name, "Fecha": event.date,
         "Hora": event.time} for event in listed_events]
    return filas

def obtener_evento(event_id: str) -> list[dict]:
    endpoint = GetEventEndpoint()
    print(event_id)
    response: GetEventResponse = endpoint.excecute(int(event_id))
    necesary_resources = response.necesary_resources if response.necesary_resources else None
    print(response)
    evento = [
            {"State": response.event_state, "Id": response.event_id,
            "Employee": response.event_employee, "Owns Name": response.event_owns_name,
            "Date": response.event_date_time.date(), "Time": response.event_date_time.time(),
            "Duration": response.event_duration, "Appointment Name": response.event_appointment_name,
            "Is Urgency": f"{response.event_is_urgency}", "Necesary Resources": necesary_resources}]
   
    return evento

def crear_empleado(name: str, experience: int, is_doctor: bool):
    endpoint = EmployeeCreatorEndpoint()
    employee = endpoint.excecute(name, experience, is_doctor)
    crear_usario(employee)

def listar_empleados() -> list[dict]:
    endpoint = ListEmployeesEndpoint()
    listed_employees: list[EmployeeDto] = endpoint.excecute()
    filas = [ 
        {"ID": employee.id, "Nombre": employee.name, "Experiencia": employee.experience,
         "Is Doctor": employee.is_doctor, "On Vacations": employee.on_vacations
        } for employee in listed_employees]
    return filas 
 
def asignar_vacaciones(employee: str, start_vacation: datetime.date, end_vacation: datetime.date):
    endpoint = EmployeeVacationsSeterEndpoint()    
    endpoint.excecute(int(employee.split(" ")[0]), start_vacation, end_vacation)

def crear_recurso(name: str, count: int, is_spendable: bool,
                use_with: list[int]=[], dont_use_with: list[int]=[]):
    endpoint = ResourceCreatorEndpoint()  
    endpoint.excecute(name, count, is_spendable, use_with, dont_use_with)

def listar_recursos() -> list[dict]:
    endpoint = ListResourcesEndpoint()
    listed_resources: list[ResourceDto] = endpoint.excecute()
    filas = [ 
        {"ID": resource.id, "Nombre": resource.name, "Count": resource.count,
         "Is Espendable": resource.is_espendable} for resource in listed_resources]
    return filas 

def remover_uso(recurso_dependiente_id: int, recurso_restringido_id: int):
    endpoint = RemoveUseWithEndpoint()
    endpoint.excecute(recurso_dependiente_id, recurso_restringido_id)

def remover_no_uso(recurso_dependiente_id: int, recurso_restringido_id: int):
    endpoint = RemoveDontUseWithEndpoint()
    endpoint.excecute(recurso_dependiente_id, recurso_restringido_id)

def agregar_uso(recurso_dependiente_id: int, recurso_restringido_id: int):
    endpoint = SetNewUseWithEndpoint()
    endpoint.excecute(recurso_dependiente_id, recurso_restringido_id)
   
def agregar_no_uso(recurso_dependiente_id: int, recurso_restringido_id: int):
    endpoint = SetNewDontUseWithEndpoint()
    endpoint.excecute(recurso_dependiente_id, recurso_restringido_id)

def surtir_alamcen(resources_id: list[int], resoures_count: list[int]):
    endpoint = SuplyStorehouseEndpoint()
    endpoint.excecute(resources_id, resoures_count)

# TODO: ver si esta bien y si tambien se deben limpiar las variabless locales
def refresh() -> tuple[list[str], list[str]]:
    endpoint = RefreshSystemEndpoint()
    return endpoint.excecute()

def crear_usario(employee: Employee):
    endpoint = CreateUserEndpoint()
    endpoint.excecute(employee)

def cambiar_nombre_de_usuario(user_id, password, new_user_name):
    endpoint = ChangeUserNameEndpoint()
    endpoint.excecute(user_id, password, new_user_name)

def cambiar_password_de_usuario(user_id, password, new_password):
    endpoint = ChangeUserPasswordEndpoint()
    endpoint.excecute(user_id, password, new_password)

def cambiar_rol_de_usuario(user: str, password, new_rol):
    endpoint = ChangeUserRolEndpoint()
    endpoint.excecute(int(user.split(" ")[0]), password, new_rol)

