"""aqui se deside si se puede o no"""
#   TODO aqui es donde van las restricciones

import datetime
import holidays
import calendar

from Backend.Data_Access.context import Context
from Backend.Data_Access.repository import Repository
from Domain.medical_date import MedicalDate
from Domain.resources import Resource
from Domain.resources import Employee
from Data_Access.date_manager import Cronograma
from constants import Events
from create_event_command import CreateEventComand
from create_event_response import CreateEventResponse


class CreateEventHandler:
    def __init__(self, comand: CreateEventComand, manager: Cronograma, actual_id: int, open_hour: datetime.datetime.time,
                 close_hour: datetime.datetime.time):
        
        self.command = comand
        self.manager = manager
        self.actual_id = actual_id
        self.open_hour = open_hour
        self.close_hour = close_hour

    actual_datetime = datetime.datetime.now()
    actual_date = actual_datetime.date() 
    actual_time =  actual_datetime.time().replace(second=0, microsecond=0)
    
    def execute(self) -> CreateEventResponse: #TODO: terminar
        print("Creating event")
        repo: Repository = Context.get_repo(Events)
        
        evn = MedicalDate() # Informacion pasada en el command
        return CreateEventResponse()


# -------------------------------------------------
    # todo si la fecha se pasa en el comand como pongo el parametro de fecha -- lo quito?
    # todo ver si esta bien
    def add_appointment(self, appointment_date: str, owns_name: str, employee: Employee,
                        type_classification: str, necesary_resources: list[Resource]) -> MedicalDate:
        
        try:
            appointment_date, appointment_time = self.is_valid_date(appointment_date)

            if not self.employee_disponibility(employee, appointment_date):
                raise Exception("Empleado no disponible")  #todo verificar si esta bien asi
        
            resources_valid_to_use = self.validate_necesary_resources(necesary_resources)
        
            if not resources_valid_to_use:      #todo verificar si esta bien
                raise Exception("No es posible crear la cita por restricciones entre recursos")  
        
        except (EmployeeUnavailableError, ResourceConflictError) as e:
            print(f"Error al crear la cita: {e}")
        
        else:
            # TODO
            new_appointment=MedicalDate(self.actual_id,appointment_date,appointment_time,owns_name,employee,type_classification,necesary_resources)
            self.actual_id+=1 # todo esto se hace desde otro lugar despues de creado el evento 
        
        
        # on_vacations =0
        # vacations=0
    
    # TODO: terminar
    def is_valid_date(self, appointment_date: str) -> tuple[datetime.date, datetime.time]:
     
        try:
            appointment_date: datetime.date = datetime.datetime.strptime(appointment_date,"%Y/%b/%d").date()
            # appointment_time: datetime.time = datetime.datetime.strptime(appointment_time, "%H:%M").time()
        except Exception():  #todo revisar si esta bien asi
            pass

        valid_day, day_message = self.is_valid_day(appointment_date)
        if not valid_day:
            raise Exception(day_message)    #todo revisar si esta bien asi
        
        # try:
        #     pass
        # finally:
        #     pass

        appointment_hour, valid_hour, hour_message = self.is_valid_time(appointment_date)
        if not valid_hour:
            raise Exception(hour_message)   #todo revisar si esta bien asi

        return (appointment_date, appointment_hour)
    
    def is_valid_day(self, day: datetime.date) -> tuple[bool,str]:
        
        is_valid = True
        message = ""

        if day.weekday() in [5, 6] or day in holidays.CountryHoliday("US", day.year):\
            # 5 o 6 == saturday or sunday
            is_valid = False
            message = "Dia no laborable"
            return (is_valid, message)
        
        if day < self.actual_date:
            is_valid = False
            message = "No puede agendar cita en una fecha pasada"
            return (is_valid, message)

        return (is_valid, "Dia valido") 
    def is_valid_time(self,day: datetime.date) -> tuple[datetime.time, bool, str]:

        appointment_time = datetime.time(0,0)
        is_valid = True
        message = ""
        event_employee = self.command.employee
        b= list()
        
        # si el dia esta en el dict
        if day in self.manager.list_of_events:      
            day_events: dict[str: list[MedicalDate]] = self.manager.list_of_events[day]
            employee_events: list[MedicalDate] = day_events[event_employee.name]
            if len(employee_events) != 0:
                # el doctor ya tiene pacientes
                last_appointment = employee_events[len(employee_events)-1]
                appointment_time = last_appointment.time + last_appointment.duration    
           
            # el doctor no tiene pacientes 
            else: appointment_time = self.open_hour   
        
        # el dia no esta en el dict por tanto el doct no tiene pacienetes
        else : appointment_time = self.open_hour   
        
        # la hora pasa de la hora del cierre, se contempla si es una urgencia
        if (appointment_time > self.close_hour or appointment_time + event_employee.productivity() >
            self.close_hour) and not self.command.urgency:

            is_valid = False
            message = "No hay capasidad en este dia"
            return (appointment_time, is_valid, message)
            
        # es el dia actual pero la hora ya paso
        if day == self.actual_date:
            if appointment_time < self.actual_time:
                    is_valid = False
                    message = "No puede agendar cita en una hora pasada"
                    return (appointment_time, is_valid, message)
        
        return(appointment_time, is_valid,"Hora valida")

    def employee_disponibility(self, employee: Employee, appointment_date: datetime.date) -> bool:
        if employee.on_vacations and employee.vacations[0] < appointment_date < employee.vacations[1]:
            return False
        return True

# TODO: agg el sistem de poner las urgencias delante de la cola y las demas correrlas

    def validate_necesary_resources(self, necesary_resources: list[Resource]) -> bool:
        pass 


# TODO: Validar las restricciones de recursos
# TODO: Guardar en Base de datos el evento creado
# TODO: Devolver un objeto de tipo response con la info del evento