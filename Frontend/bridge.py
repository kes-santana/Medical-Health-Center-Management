
import datetime

from Backend.Dashboard.employee_rank import EmployeeRankingGraphix
from Backend.Dashboard.events_per_day import EventPerDayGraphix
from Backend.Dashboard.month_dates import MonthDates

from Backend.Dashboard.resource_per_month import ResourcePerMonthGraphix
from Backend.Domain.resources import Resource
from Backend.Endpoins.user_endpoints.login_endpoint import LoginEndpoint
from Backend.Endpoins.user_endpoints.create_user_endpoint import CreateUserEndpoint
from Backend.Endpoins.user_endpoints.change_user_name_endpoint import ChangeUserNameEndpoint
from Backend.Endpoins.user_endpoints.change_user_password_endpoint import ChangeUserPasswordEndpoint
from Backend.Endpoins.user_endpoints.change_user_rol_endpoint import ChangeUserRolEndpoint

from Backend.Endpoins.events_endpoints.create_event_endpoint import CreateEventEndpoint
from Backend.Features.Events.Get.get_event_response import GetEventResponse
from Backend.Features.Events.Post.create_event_response import CreateEventResponse
from Backend.Features.dtos.eventdto import EventDto
from Backend.Endpoins.events_endpoints.get_event_endpoint import GetEventEndpoint
from Backend.Endpoins.events_endpoints.list_events_endpoint import ListEventEndpoint
from Backend.Endpoins.events_endpoints.change_event_state_endpoint import ChangeEventStateEndpiont

from Backend.Domain.employee import Employee
from Backend.Endpoins.employees_endpoints.get_employee_endpoint import GetEmployeeEndpoint
from Backend.Endpoins.employees_endpoints.on_vactions_verify_endpoint import VerifyVacations
from Backend.Endpoins.employees_endpoints.create_employee_endoint import EmployeeCreatorEndpoint
from Backend.Endpoins.employees_endpoints.list_employees_endpoint import ListEmployeesEndpoint
from Backend.Endpoins.employees_endpoints.set_employee_vacations_endpoint import EmployeeVacationsSeterEndpoint
from Backend.Features.dtos.employee_dto import EmployeeDto

from Backend.Endpoins.resources_endpoints.get_resource_Endpoint import GetResourceEndpoint
from Backend.Endpoins.resources_endpoints.create_resource_endpoint import ResourceCreatorEndpoint
from Backend.Endpoins.resources_endpoints.list_resources_endpoint import ListResourcesEndpoint
from Backend.Endpoins.resources_endpoints.remove_dont_use_with_endpoint import RemoveDontUseWithEndpoint
from Backend.Endpoins.resources_endpoints.remove_use_with_endpoint import RemoveUseWithEndpoint
from Backend.Endpoins.resources_endpoints.set_new_dont_use_with_endpoint import SetNewDontUseWithEndpoint
from Backend.Endpoins.resources_endpoints.set_new_use_with_endpoint import SetNewUseWithEndpoint
from Backend.Endpoins.resources_endpoints.suply_storehouse_endpoint import SuplyStorehouseEndpoint
from Backend.Features.dtos.resource_dto import ResourceDto
from Backend.Endpoins.refresh_system_endpoint import RefreshSystemEndpoint
from Frontend.front_utils import load_employees_names, load_resources_names, search_id_by_name

# Función que recibe los datos del formulario
def verify_login(user_input, password_input) -> tuple[bool, str, str, str]:
   endpoint = LoginEndpoint()
   return endpoint.excecute(user_input, password_input)

def refresh() -> tuple[list[str], list[str]]:
    endpoint = RefreshSystemEndpoint()   
    endpoint.excecute() 
    all_resources = load_resources_names()
    all_employees = load_employees_names()
    return all_resources, all_employees

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
        {"ID": event.id, "State": event.state, "Doctor": event.doctor, "Paciente": event.patient, "Consulta": event.name, "Fecha": event.date,
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

def cambiar_estado_de_evento(event_id: int, new_state: str):
    endpoint = ChangeEventStateEndpiont()
    endpoint.excecute(event_id, new_state)

def crear_empleado(name: str, experience: int, is_doctor: bool):
    endpoint = EmployeeCreatorEndpoint()
    employee = endpoint.excecute(name, experience, is_doctor)
    crear_usario(employee)

def obtener_empleado(employee_id: int):
    endpoint = GetEmployeeEndpoint()
    employee_dto = endpoint.excecute(employee_id)
    employee =[ {"ID": employee_dto.id, "Nombre": employee_dto.name, "Experiencia": employee_dto.experience,
                 "Is Doctor": employee_dto.is_doctor, "On Vacations": employee_dto.on_vacations}]
    return employee

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

def verify_vacations():
    endpoint = VerifyVacations()
    endpoint.excecute()

def crear_recurso(name: str, count: int, is_spendable: bool,
                use_with: list[int]=[], dont_use_with: list[int]=[]):
    endpoint = ResourceCreatorEndpoint()  
    endpoint.excecute(name, count, is_spendable, use_with, dont_use_with)

def obtener_recurso(resource_id: int):
    endpoint = GetResourceEndpoint()
    resource_dto = endpoint.excecute(resource_id)
    resource =[{"ID": resource_dto.id, "Nombre": resource_dto.name, "Count": resource_dto.count,
                 "Is Spendable": resource_dto.is_espendable, "Usar Con": resource_dto.use_with,
                 "No Usar Con": resource_dto.dont_use_with}]
    return resource

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

def crear_usario(employee: Employee):
    endpoint = CreateUserEndpoint()
    endpoint.excecute(employee)

def cambiar_nombre_de_usuario(user_id, password, new_user_name):
    endpoint = ChangeUserNameEndpoint()
    endpoint.excecute(user_id, password, new_user_name)

def cambiar_password_de_usuario(user_id, password, new_password, new_password_copy):
    endpoint = ChangeUserPasswordEndpoint()
    endpoint.excecute(user_id, password, new_password, new_password_copy)

def cambiar_rol_de_usuario(admin_id: int, user: str, password: str, new_rol: str):
    endpoint = ChangeUserRolEndpoint()
    endpoint.excecute(admin_id, int(user.split(" ")[0]), password, new_rol)

#--------------------------CALENDARIO-------------------------------------#

def month_dates() -> dict:
    endpoint = MonthDates()
    return endpoint.excecute()

#---------------------------GRAFICOS--------------------------------------#

def events_per_day(start_date: datetime.date, end_data: datetime.date, graph_type: str):
    endpoint = EventPerDayGraphix(start_date, end_data, graph_type)
    return endpoint.execute()

def employee_ranking(rank_type: str):
    endpoint = EmployeeRankingGraphix(rank_type)
    return endpoint.excecute()

def resource_per_month(fecha: datetime.date, recursos: list[str]):
    recursos = search_id_by_name(recursos)
    endpoint = ResourcePerMonthGraphix(fecha, recursos)
    return endpoint.excecute()