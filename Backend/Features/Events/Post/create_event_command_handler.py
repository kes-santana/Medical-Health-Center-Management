"""aqui se decide si se puede o no"""
#   TODO ver si se me ocurren mas  restricciones

import datetime

from Backend.Data_Access.context import Context
from Backend.Data_Access.date_manager import DateManager
from Backend.Data_Access.resource_repository import ResourceRepository
from Backend.Domain.medical_date import MedicalDate
from Backend.Domain.resources import Resource
from Backend.Domain.employee import Employee
from Backend.Features.Events.Post.create_event_command import CreateEventCommand
from Backend.Features.Events.Post.create_event_response import CreateEventResponse
from constants import OPEN_HOUR, CLOSE_HOUR, MID_DAY



class CreateEventHandler:
    def __init__(self, comand: CreateEventCommand):
        self.command = comand
        self.actual_datetime = datetime.datetime.now()
        self.actual_date = self.actual_datetime.date() 
        self.actual_time = self.actual_datetime.time().replace(second=0, microsecond=0)
        self.context = Context()
    
    def execute(self) -> CreateEventResponse:
       
        print("Creating event")
        manager: DateManager = self.context.get_repo_date_manager()
        resource_repo: ResourceRepository = self.context.get_repo_resource()
        necesary_resources: list[Resource] = self.get_necesary_resources(
                                                self.command.necesary_resources, resource_repo.resource_list)
        employee_repo = self.context.get_repo_employee()
        employee = employee_repo.get_by_id(self.command.employee)
        if employee == None:
            raise Exception("No existe ningun empleado con ese ID")

        event: MedicalDate = self.create_appointment(manager, self.command.date, self.command.time, self.command.asigned_date_time_auto,
                        self.command.owns_name, employee, self.command.is_urgency, 
                        necesary_resources, self.command.resources_count, self.command.time_auto)
        
        manager.add_event(event.date_time,str(event.employee.id),event)
        self.context.save(manager)
        self.context.save(resource_repo)
        print("Event created")
        return CreateEventResponse(event.id, event.date_time, event.owns_name, event.employee.name)
   
    def create_appointment(self, manager: DateManager, appointment_date: datetime.date, appointment_time: datetime.time,
                           asigned_date_time_auto: bool, owns_name: str, employee: Employee,
                           is_urgency: bool, necesary_resources: list[Resource], resources_count: list[int], time_auto: bool) -> MedicalDate:
            if asigned_date_time_auto:
                appointment_date_time = self.asigned_date_time_auto_to_event(manager, employee)

            else:   
                appointment_date_time = self.is_valid_date(manager, appointment_date,
                                                           appointment_time, is_urgency, employee, time_auto)
            
            self.employee_disponibility(employee, appointment_date)
            # self.convert_resources(necesary_resources)
            self.validate_necesary_resources(necesary_resources, resources_count)
            self.find_who_use_a_spendable_resource(necesary_resources, appointment_date_time, (appointment_date_time + datetime.timedelta(hours=employee.productivity().hour, minutes=employee.productivity().minute)).time(), manager)
            self.validate_reusable_resources(manager, appointment_date_time, necesary_resources, resources_count, employee)
            self.descontar_recursos(necesary_resources, self.command.resources_count)
            
            return MedicalDate(manager.actual_id, appointment_date_time, owns_name, employee,
                               is_urgency, necesary_resources, self.command.resources_count, self.command.appointment_name) 

    def employee_disponibility(self, employee: Employee, appointment_date: datetime.date) -> None:
        if employee.vacations:
            if employee.vacations[0] < appointment_date < employee.vacations[1]:
                raise Exception("Empleado no disponible")

    def get_necesary_resources(self, necesary_resources: list[int],
                               resource_list: dict[str, Resource]) -> list[Resource]:
        
        resources: list[Resource] = []

        if len(necesary_resources)==0:
            return resources
        
        for recurso in necesary_resources:
            for r in resource_list.keys():
                if int(r) == recurso:
                    resources.append(resource_list[r])
                    break
            if len(resources)==0 or resources[-1].id != recurso:
                raise Exception(f'El recurso de ID: "{recurso}" no esta en almacen')
        
        return resources
    
    def validate_necesary_resources(self, necesary_resources: list[Resource], resources_count: list[int]) -> None:
        for resource in range(len(necesary_resources)):
            r = necesary_resources[resource]

            if r.count == 0 or r.count - resources_count[resource] < 0:
                raise Exception(f'No hay disponibilidad del producto "{r.name}" en el almacen')
                
            for u_w in r.use_with:
                if not any(x.id == u_w for x in necesary_resources):
                    raise Exception(f'El recurso "{necesary_resources[resource].id}" nesecita usarse con el recurso de ID: "{u_w}" y este ultimo no esta en la lista de recursos')
            
            for d_u_w in r.dont_use_with:
                if any(x.id == d_u_w for x in necesary_resources):
                    raise Exception(f'El recurso "{r.name}" no puede usarse con el recurso con ID: "{d_u_w}" y este ultimo esta en la lista de recursos')
     
    def validate_reusable_resources(self, manager: DateManager, appointment_date_time: datetime.datetime, 
                                    necesary_resources: list[Resource], resources_count: list[int], employee: Employee) -> None:
        events = manager.get_all()
        events_filtred = [e for e in events if e.date_time.date() == appointment_date_time.date()]

        for resource in range(len(necesary_resources)):
            r = necesary_resources[resource]
            c = resources_count[resource]
            if r.is_espendable:
                continue

            r_events = self.find_resource_event(r, events_filtred, appointment_date_time, employee.productivity().minute)
            if r.count - r_events >= c:
                continue
            else:
                raise Exception(f'El recurso "{r.name}" no esta disponible en este momento')

    def find_resource_event(self, resource: Resource, events_filtred: list[MedicalDate],
                            appointment_date_time: datetime.datetime, duration_min: int):
        count = 0
        ap_time = appointment_date_time.time()
        ap_tdelta = datetime.timedelta(hours=ap_time.hour, minutes=ap_time.minute)
        duration_tdelta = datetime.timedelta(minutes=duration_min)
        ap_end =  ap_tdelta + duration_tdelta

        for e in events_filtred:
            nr = e.necesary_resources
            is_on_event = False
            index =0
            for r in range(len(nr)):
                if nr[r].id == resource.id:
                  is_on_event = True
                  index = r
                  break  
            
            if not is_on_event:
                continue

            e_time = e.date_time.time()
            e_tdelta = datetime.timedelta(hours=e_time.hour, minutes=e_time.minute)
            e_duration_tdelta = datetime.timedelta(minutes=e.duration.minute)
            event_end = e_tdelta + e_duration_tdelta
            

            if (e_tdelta <= ap_tdelta <= event_end) or (e_tdelta <= ap_end <= event_end):
                count += e.resources_count[index]
        
        return count

    def descontar_recursos(self, necesary_resources: list[Resource], resources_count: list[int]) -> None:
        for r in range(len(necesary_resources)):
            if necesary_resources[r].is_espendable:
                necesary_resources[r].count -= resources_count[r]
       
    def find_who_use_a_spendable_resource(self, resource_list_event: list[Resource], day_time: datetime.datetime, end_time:datetime.time, manager: DateManager):
        day_filter = lambda day, event: event.date_time.date == day
        events = manager.get_all()
        events = [e for e in events if day_filter(day_time.date(), e)]
        hour_events: list[MedicalDate] = []
        
        for e in events:
            min_start_e = e.date_time.time() if e.date_time.time() < day_time.time() else day_time
            if min_start_e == e.date_time.time():
                end_min = e.end_time
                max_start_e = day_time.time()
            else:
                end_min = end_time
                max_start_e = e.date_time.time()
            if max_start_e <= end_min:
                hour_events.append(e)
        
        for rec in resource_list_event:
            if rec.is_espendable:
                continue
            count_rec = 0
            for e in hour_events:
                if rec.id in [r.id for r in e.necesary_resources]:
                    count_rec += e.resources_count[e.necesary_resources.index(rec)]
            if count_rec == rec.count:
                raise Exception(f"No hay {rec.name}s disponibles a esa hora")

                
    def is_valid_date(self, manager: DateManager, appointment_date: datetime.date, appointment_time: str, is_urgency: bool, employee: Employee, time_auto: bool) -> datetime.datetime:
     
        self.validate_day(appointment_date)
        if not is_urgency:
           appointment_time = self.validate_time(manager, appointment_date, appointment_time, time_auto, employee)
        
        else:
            print([str(d) for d in manager.list_of_events.keys()])
            appointment_time: datetime.time = self.proces_urgency(manager.list_of_events[appointment_date][str(employee.id)])

        return datetime.datetime.combine(appointment_date, appointment_time)
    
    def validate_day(self, appointment_date: datetime.date):
        
        if appointment_date == self.actual_date:
                raise Exception("No se pueden agendar citas para el mismo dia que se crean")
        
        if appointment_date.weekday() in [5, 6]: # or appointment_date in holidays.CountryHoliday("US", appointment_date.year):
            # 5 o 6 == saturday or sunday
            raise Exception("Dia no laborable")
        
        if appointment_date < self.actual_date:
            raise Exception("No puede agendar cita en una fecha pasada") 
         
    def validate_time(self, manager: DateManager, apointment_day: datetime.date, apointment_time: datetime.time, time_auto: bool, event_employee: Employee) -> datetime.time:
       
        employee_events: list[MedicalDate] = self.doctor_is_working(manager, apointment_day, event_employee)
        
        if not time_auto:
            self.is_on_time(apointment_time, employee_events)
            return apointment_time
            
        else:
            time = self.buscar_hora(employee_events)
            return time

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
            if str(event_employee.id) in day_events.keys():
                return day_events[str(event_employee.id)]

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
            new_date_time = datetime.datetime.combine(eventos[0].date_time, OPEN_HOUR)
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
# todo revisar
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

            


