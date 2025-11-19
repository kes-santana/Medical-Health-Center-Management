"""aqui se decide si se puede o no"""
#   TODO aqui es donde van las restricciones

import datetime
import holidays

from Backend.Data_Access.context import Context
from Backend.Data_Access.date_manager import DateManager
from Backend.Domain.medical_date import MedicalDate
from Backend.Domain.resources import Employee, Resource
from Backend.Features.Events.Post.create_event_command import CreateEventComand
from Backend.Features.Events.Post.create_event_response import CreateEventResponse
from constants import Events



class CreateEventHandler:
    def __init__(self, comand: CreateEventComand, open_hour: str,
                 close_hour: str):
        
        self.command = comand
        self.open_hour = datetime.datetime.strptime(open_hour, "%H:%M").time()
        self.close_hour = datetime.datetime.strptime(close_hour, "%H:%M").time()

    actual_datetime = datetime.datetime.now()
    actual_date = actual_datetime.date() 
    actual_time =  actual_datetime.time().replace(second=0, microsecond=0)
    
    def execute(self) -> CreateEventResponse: #TODO: terminar y revisar
       
        print("Creating event")
        manager: DateManager = Context.get_repo(Events)

        event: MedicalDate = self.create_appointment(manager, self.command.date,
                        self.command.owns_name, self.command.employee, 
                        self.command.is_urgency, self.command.necesary_resources)
        
        manager.actual_id += 1
        manager.save(event, self.actual_time)  #todo como el manager guarda el actual id? 
        print("Event created")
        
        # TODO: Devolver un objeto de tipo response con la info del evento
        return CreateEventResponse()

    def create_appointment(self, manager: DateManager, 
                           appointment_date: str, owns_name: str, employee: str, is_urgency: bool,
                           necesary_resources: list[str]) -> MedicalDate:
        
            # todo crear el empleado por su nombre
        
            appointment_date, appointment_hour = self.is_valid_date(manager, appointment_date, employee)
            
            self.employee_disponibility(employee, appointment_date)
        
            # todo crear los recursos por su nombre y agg a la lista (la lista debe llamarse igual)
            self.validate_necesary_resources(necesary_resources)

            # TODO ver si hay q agg mas cosas
            return MedicalDate(manager.actual_id, appointment_date, appointment_hour, self.actual_time,
                               owns_name, employee, is_urgency, necesary_resources) 
  
    def employee_disponibility(self, employee: Employee, appointment_date: datetime.date) -> None:
        if employee.on_vacations and employee.vacations[0] < appointment_date < employee.vacations[1]:
            raise Exception("Empleado no disponible")

    def validate_necesary_resources(self, necesary_resources: list[Resource]) -> None:
        for resource in necesary_resources:
            for use_with in resource.use_with:
                if not any(x.name == use_with.name for x in necesary_resources):
                    raise Exception(f'El recurso "{resource}" nesecita usarse con el recurso "{use_with}" y este ultimo no esta en la lista de recursos')
            
            for dont_use_with in resource.dont_use_with:
                if any(x.name == dont_use_with for x in necesary_resources):
                    raise Exception(f'El recurso "{resource}" no puede usarse con el recurso "{dont_use_with}" y este ultimo esta en la lista de recursos')
    
    def is_valid_date(self, manager: DateManager, appointment_date: str, employee: Employee) -> tuple[datetime.date, datetime.time]:
     
        appointment_date: datetime.date = self.is_valid_day(appointment_date)
        appointment_hour = self.is_on_time(manager, appointment_date, employee)
        return (appointment_date, appointment_hour)
    
    def is_valid_day(self, day: str) -> datetime.date:
        try:
            appointment_date: datetime.date = datetime.datetime.strptime(appointment_date,"%Y/%b/%d").date()         
        except Exception():
            raise Exception("Dia no valido")
        else:
            if appointment_date.weekday() in [5, 6] or appointment_date in holidays.CountryHoliday("US", appointment_date.year):
                # 5 o 6 == saturday or sunday
                is_valid = False
                raise Exception("Dia no laborable")
            
            if day < self.actual_date:
                is_valid = False
                raise Exception("No puede agendar cita en una fecha pasada") 
            
            return appointment_date

    # todo: revisar con calma de aqui para abajo
    def is_on_time(self, manager: DateManager, day: datetime.date, event_employee: Employee) -> datetime.time:

        appointment_time = self.open_hour
        
        # si el dia esta en el dict
        if day in manager.list_of_events:      
            day_events: dict[str: list[MedicalDate]] = manager.list_of_events[day]
            
            # si el doc esta en el dict
            if event_employee.name in day_events:
                employee_events: list[MedicalDate] = day_events[event_employee.name]
               
                # el doctor esta entonces ya tiene pacientes
                last_event = self.find_last_event(employee_events)
                
                #  si hay algun paciente activo
                if last_event is not None:
                    last_event_concluyed: datetime.time = last_event.time + last_event.duration
                    
                    if last_event_concluyed >= self.close_hour:
                        raise Exception("No hay capacidad en este dia")
                
                    # si es el dia actual la hora del event es el max entre la hora actual y la hora 
                    # en que finaliza el evento anterior
                    if day == self.actual_date:
                        if not self.command.is_urgency:
                            appointment_time = max(self.actual_time, last_event_concluyed)
                        else:
                            appointment_time = self.find_hour_for_urgency_actual_date(employee_events, self.actual_time)
                
                    # no es el dia actual
                    else:
                        if not self.command.is_urgency:
                            appointment_time = last_event_concluyed
                        else:      
                            appointment_time = self.find_best_hour_for_urgency(employee_events)          
                else: # el doc no tiene pacientes (tiene pero no estan activos)
                    if day == self.actual_date: 
                        appointment_time = self.actual_time
                    
            # si el doc no esta en el dict no tiene pasientes
            else: 
                # si es el dia actual entonces la hora es la actual sino es el primer 
                # paciente (no hay q hacer nada pues esta seteado arriba)
                if day == self.actual_date: 
                    appointment_time = self.actual_time
                         
        # el dia no esta en el dict por tanto el doct no tiene pacienetes  
        else:
            # si es el dia actual la hora es la actual sino es la de apertura (ya esta puesto arriba)
            if day == self.actual_date: 
                    appointment_time = self.actual_time

        # la hora pasa de la hora del cierre
        if appointment_time >= self.close_hour:
            raise Exception("No hay capacidad en este dia")
            
        return appointment_time

    # asumimos q la lista esta organizada, que los finalizados y cancelados esten para atras 
    # y que el evento es una urgencia; las urgencias siempre estan alante
    def find_best_hour_for_urgency(self, employee_events: list[MedicalDate]) -> datetime.time:
        best = self.open_hour 
        for event in employee_events:
            if event.state == "finished" or  event.state == "canceled" or not event.is_urgency:
                return best
            else:
                best = event.time + event.duration   
        return best
 
    def find_hour_for_urgency_actual_date(self, employee_events: list[MedicalDate], after_time: datetime.time) -> datetime.time: 
        best = None
        for event in employee_events:
            if event.state == "finished" or  event.state == "canceled":
                if best == None:
                    return after_time
                return best
            if event.time < after_time:
                best = event.time + event.duration
            else:
                break

        return max(best, after_time)
    
    def find_last_event(self, employee_events: list[MedicalDate]):
        last = None      
        for event in employee_events:
            if event.state == "finished" or event.state == "canceled":
               return last
            last = event
        
