"""aqui se decide si se puede o no"""
#   TODO ver si se me ocurren mas  restricciones

import datetime

from Backend.Data_Access.context import Context
from Backend.Data_Access.date_manager import DateManager
from Backend.Data_Access.resource_repository import ResourceRepository
from Backend.Domain.medical_date import MedicalDate
from Backend.Domain.resources import Employee, Resource
from Backend.Features.Events.Post.create_event_command import CreateEventCommand
from Backend.Features.Events.Post.create_event_response import CreateEventResponse
from constants import OPEN_HOUR, CLOSE_HOUR, MID_DAY



class CreateEventHandler:
    def __init__(self, comand: CreateEventCommand):
        
        self.command = comand

    actual_datetime = datetime.datetime.now()
    actual_date = actual_datetime.date() 
    actual_time =  actual_datetime.time().replace(second=0, microsecond=0)
    context = Context()
    
    def execute(self) -> CreateEventResponse: #TODO: revisar
       
        print("Creating event")
        manager: DateManager = self.context.get_repo_date_manager()
        resource_repo: ResourceRepository = self.context.get_repo_resource()
        necesary_resources: list[Resource] = self.get_necesary_resources(
                                                self.command.necesary_resources, resource_repo)
        employee_repo = self.context.get_repo_employee()
        employee = employee_repo.get_by_id(self.command.employee)
        if employee == None:
            raise Exception("No existe ningun empleado con ese ID")

        # todo ver si puedo cambiar para q solo lleve el manager pq el command esta en self
        event: MedicalDate = self.create_appointment(manager, self.command.date, self.command.time,
                        self.command.owns_name, employee, 
                        self.command.is_urgency, necesary_resources)
        
        manager.actual_id += 1
        manager.save()      #todo el save en todos los repos
        print("Event created")
        
        # TODO: Devolver un objeto de tipo response con la info del evento
        return CreateEventResponse()

    def create_appointment(self, manager: DateManager, appointment_date: str, appointment_time: str,
                           asigned_date_time_auto: bool, owns_name: str, employee: Employee,
                           is_urgency: bool, necesary_resources: list[Resource]) -> MedicalDate:
            if asigned_date_time_auto:
                appointment_date_time= self.asigned_date_time_auto_to_event(employee)

            else:   
                appointment_date_time = self.is_valid_date(manager, appointment_date,
                                                           appointment_time, is_urgency, employee)
            
            self.employee_disponibility(employee, appointment_date)
            self.validate_necesary_resources(necesary_resources)
            self.descontar_recursos(necesary_resources)

            return MedicalDate(manager.actual_id, appointment_date_time, owns_name, employee,
                               is_urgency, necesary_resources, self.command.appointment_name) 
  
  
    def employee_disponibility(self, employee: Employee, appointment_date: datetime.date) -> None:
        if employee.on_vacations and employee.vacations[0].date() < appointment_date < employee.vacations[1].date():
            raise Exception("Empleado no disponible")

    def get_necesary_resources(self, necesary_resources: list[str],
                               resource_list: dict[int, Resource]) -> list[Resource]:
        
        resources: list[Resource] = []

        if len(necesary_resources)==0:
            return resources
        
        for recurso in necesary_resources:
            for r in resource_list.values():
                if r.name == recurso:
                    resources.append(r)
                    break
            if len(resources)==0 or resources[-1].name != recurso:
                raise Exception(f"El recurso {recurso} no esta en almacen")
        
        return resources
    
    def validate_necesary_resources(self, necesary_resources: list[Resource], count_of_resource: list[int]) -> None:
        for resource in range(len(necesary_resources)):
            r = necesary_resources[resource]

            if r.count == 0 or r.count - count_of_resource[resource] < 0:
                raise Exception(f'No hay disponibilidad del producto "{r.name}" en el almacen')
                
            for u_w in r.use_with:
                if not any(x.id == u_w for x in necesary_resources):
                    raise Exception(f'El recurso "{resource}" nesecita usarse con el recurso de ID: "{u_w}" y este ultimo no esta en la lista de recursos')
            
            for d_u_w in r.dont_use_with:
                if any(x.id == d_u_w for x in necesary_resources):
                    raise Exception(f'El recurso "{r.name}" no puede usarse con el recurso con ID: "{d_u_w}" y este ultimo esta en la lista de recursos')
     
    def descontar_recursos(self, necesary_resources: list[Resource], count_of_resource: list[int]) -> None:
        for r in range(len(necesary_resources)):
            necesary_resources[r].count -= count_of_resource[r]
       
    
    # todo: revisar con calma de aqui para abajo 
    def is_valid_date(self, manager: DateManager, appointment_date: str, appointment_time: str, is_urgency: bool, employee: Employee) -> datetime.datetime:
     
        self.validate_day(appointment_date)
        if not is_urgency:
           appointment_time = self.validate_time(manager, appointment_date, appointment_time, employee)
        
        else: 
            appointment_time: datetime.time = self.proces_urgency()
            appointment_time = appointment_time.isoformat()

        return datetime.datetime.strptime(f"{appointment_date} {appointment_time}", "%Y/%m/%d %H:%M")
    
    def validate_day(self, day: str):
        try:
            appointment_date: datetime.date = datetime.datetime.strptime(day,"%Y/%m/%d").date()         
        except Exception():
            raise Exception("Dia no valido")
        else:
            if appointment_date == self.actual_date:
                 raise Exception("No se pueden agendar citas para el mismo dia que se crean")
            
            if appointment_date.weekday() in [5, 6]: # or appointment_date in holidays.CountryHoliday("US", appointment_date.year):
                # 5 o 6 == saturday or sunday
                raise Exception("Dia no laborable")
            
            if appointment_date < self.actual_date:
                raise Exception("No puede agendar cita en una fecha pasada") 
         
    def validate_time(self, manager: DateManager, apointment_day: str, apointment_time: str, event_employee: Employee) -> str:
       
        day: datetime.date = datetime.datetime.strptime(apointment_day,"%Y/%m/%d").date()
        employee_events: list[MedicalDate] = self.doctor_is_working(manager, day, event_employee)
        
        if apointment_time != None:
            try:
                time: datetime.time = datetime.datetime.strptime(apointment_time, "%H:%M").time()
            except:
                raise Exception("Hora no valida")
            else: 
                self.is_on_time(time, employee_events)
                return apointment_time
            
        else:
            time = self.buscar_hora(employee_events)
            return time.isoformat()

    def buscar_hora(self, employee_events: list[MedicalDate]) -> datetime.time:
        """Es como buscar espacio pero teniendo el dia"""
        eventos = [e for e in employee_events if e.state == "active"]

        if not eventos:
            return OPEN_HOUR

        # Ordenar eventos por hora
        eventos.sort(key=lambda e: e.date_time)

        try:
            self.is_on_time(OPEN_HOUR, employee_events)
            return OPEN_HOUR
        except:
            pass

        for e in eventos:
            try:
                time = (e.date_time + datetime.timedelta(hours=e.duration.hour, minutes=e.duration.minute)).time()
                self.is_on_time(time, employee_events)
                return time
            except:
                continue
        raise Exception("No hay espacio disponible este dia")
                
    def doctor_is_working(self, manager: DateManager, day: datetime.date, event_employee: Employee) -> list[MedicalDate]:
        if day in manager.list_of_events:      
            day_events: dict[str: list[MedicalDate]] = manager.list_of_events[day]
            
            # si el doc esta en el dict
            if event_employee.key in day_events:
                return day_events[event_employee.key]

        return []

    def is_on_time(self, time: datetime.time, employee_events: list[MedicalDate]) -> None:
        
        if not self.verificar_espacio_de_tiempo(employee_events, time):
            raise Exception("No hay espacio a esa hora intente con buscar hueco o con otra hora")
                
        # la hora es antes de abrir o pasa del cierre 
        if OPEN_HOUR > time or time >= CLOSE_HOUR:
            raise Exception("Horario no laboral")

    def verificar_espacio_de_tiempo(self, employee_events: list[MedicalDate], time: datetime.time) -> bool:
        """Verifica q el evento no se solape con otro y que haya tiempo para su realizacion"""
        
        eventos = [e for e in employee_events if e.state == "active"]

        if not eventos:
            return True

        # Ordenar eventos por hora
        eventos.sort(key=lambda e: e.date_time)

        # Convertir la hora de entrada a datetime para poder operar
        date = eventos[0].date_time.date()
        new_date_time = datetime.datetime.combine(date, time)

        # Verificar si la hora está dentro de algún intervalo
        for e in eventos:
            inicio = e.date_time
            fin = inicio + datetime.timedelta(hours=e.duration.hour, minutes=e.duration.minute)
            if inicio <= new_date_time < fin:
                return False

        # Buscar el próximo evento que empieza después de la hora
        for e in eventos:
            if e.date_time > new_date_time:
                tiempo_disponible = e.date_time - new_date_time
                duracion_nueva_cita = datetime.timedelta(hours=e.duration.hour, minutes=e.duration.minute)
                if tiempo_disponible < duracion_nueva_cita:
                    return False
                break

        return True

    def proces_urgency(self, employee_events: list[MedicalDate]) -> datetime.time:
        eventos = [e for e in employee_events if e.state == "active"]

        if not eventos:
            return OPEN_HOUR

        # Ordenar eventos por hora
        eventos.sort(key=lambda e: e.date_time)
        if eventos[0].date_time.time() > OPEN_HOUR:
            new_date_time = datetime.datetime.combine(eventos[0], OPEN_HOUR)
            end_new_date = new_date_time + datetime.timedelta(hours=eventos[0].duration.hour,
                                                        minutes=eventos[0].duration.minute)
            self.arreglar_solapamientos(0, new_date_time, end_new_date, eventos)
            return new_date_time.time()

        # Convertir la hora de entrada a datetime para poder operar
        new_date_time = eventos[0].date_time
        end_new_date = new_date_time + datetime.timedelta(hours=eventos[0].duration.hour,
                                                        minutes=eventos[0].duration.minute)
        index = 0
        for e in eventos:
            if e.is_urgency:
                new_date_time = e.date_time + datetime.timedelta(hours=e.duration.hour, minutes=e.duration.minute)
                end_new_date = new_date_time + datetime.timedelta(hours=eventos[0].duration.hour,
                                                        minutes=eventos[0].duration.minute)
                continue
            else:
                index = eventos.index(e)
                break

        if new_date_time.time() > MID_DAY:
            raise Exception("No hay cupos para urgencias en este dia")
        
        self.arreglar_solapamientos(index, new_date_time, end_new_date, eventos)
        return new_date_time.time()

    def arreglar_solapamientos(self, index: int, new_date_time: datetime.datetime,
                                end_new_date: datetime.datetime, eventos: list[MedicalDate]):
       
        for e in range(index, len(eventos)):
            if new_date_time <= eventos[e].date_time < end_new_date:
                eventos[e].date_time = end_new_date
                new_date_time = end_new_date
                end_new_date = end_new_date + datetime.timedelta(hours=eventos[e].duration.hour,
                                                        minutes=eventos[e].duration.minute)
            break

    def asigned_date_time_auto_to_event(self, manager: DateManager, employee: Employee) -> datetime.datetime:
        tomorrow = self.actual_date + datetime.timedelta(days=1)
        while True:
            
            events = self.doctor_is_working(manager, tomorrow, employee)
            if not events:
                return datetime.datetime.combine(tomorrow, OPEN_HOUR)
           
            try:
                time = self.buscar_hora(events)
            except:
                tomorrow += datetime.timedelta(days=1)
                continue
            else:
                return datetime.datetime.combine(tomorrow, time)

            


