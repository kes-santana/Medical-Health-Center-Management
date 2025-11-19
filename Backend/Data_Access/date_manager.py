import datetime

# from Backend.Data_Access.context import Context
from Backend.Domain.medical_date import MedicalDate
from constants import Events



class DateManager:
    """Representa la clase Cronograma"""
    
    def __init__(self, list_of_events: dict[(datetime.date): dict[str: list[MedicalDate]]]={},
                 actual_id: int=0):
        """Inicializa la clase Cronograma"""
        self.list_of_events : dict[(datetime.date): dict[str: list[MedicalDate]]]  = list_of_events
        self.actual_id : int = actual_id

    
    def get_all(self) -> list[MedicalDate]:
        events: list[MedicalDate] = []
        for date in self.list_of_events.values:
            for doctor_dates in date.values:
                events.extend(doctor_dates)     #todo revisar si esto funciona
        return events

    def get_by_id(self, id: int):
        events = self.get_all()
        event_finded = None
        for event in events:
            if event.id == id:
                event_finded = event
        return event_finded
        
    #TODO revisar (creo q no hacen falta los params)
    def save(self, event: MedicalDate, created_at: datetime.time):     
        # Escribe en Base de Datos
        # Context.save_repo(Events, self.list_of_events)

        # TODO meter en otro metodo (va en en handle)
        if event.date in self.list_of_events:
            day_events: dict[str, list[MedicalDate]] = self.list_of_events[event.date]
            if event.employee.name in day_events:
                day_events[event.employee.name].append(event)
                employee_events = day_events[event.employee.name]

                if event.is_urgency:
                    self.order_by_urgency(employee_events,created_at)

            else: 
                day_events[event.employee.name] = [event]
                return
        
        else:
            self.list_of_events[event.date] = {event.employee.name: [event]}
            return

           
    # si se agg una urgencia y hay que organizar #TODO move to handle
    def order_by_urgency(self, employee_events: list[MedicalDate], created_at: datetime.time) -> None:
        event = employee_events.pop()
        index = self.find_index(employee_events, created_at)
    
    def find_index(self, employee_events: list[MedicalDate], created_at: datetime.time) -> int:
        for index in range(len(employee_events)):
            
            if employee_events[index].time < created_at:
                continue

            elif employee_events[index].time == created_at:
                if employee_events[index].is_urgency:
                    continue
                return index
           
            else: return index
        return len(employee_events)   
    
        

    def change_state(self, id: int, state: str): #todo terminar el save y ponerle los params a la ultima linea
        event = self.get_by_id(id)
        event.state = state
        employee_events: list[MedicalDate] = self.list_of_events[event.date][event.employee.name]
        if state == "finished":
            self.order_by_finished(id, employee_events)
        else: self.order_by_canceled
        self.save()
    

    def order_by_finished(self, event_finished_id: int, employee_events: list[MedicalDate]):
        index = self.find_index2(employee_events, event_finished_id)
        event = employee_events.pop(index)
        new_index = self.find_last_event_finished(employee_events)
        # si no encuentro cancelados lo pongo de ultimo
        if new_index == len(employee_events):
            employee_events.append(event)
        else: employee_events.insert(new_index, event)
    def find_last_event_finished(self, employee_events: list[MedicalDate]) -> int:     
        for index in range(len(employee_events)):
            if employee_events[index].state == "canceled":
               return index
        return len(employee_events)
    def order_by_canceled(self, event_canceled_id: int, employee_events: list[MedicalDate]):
        index = self.find_index2(employee_events, event_canceled_id)
        event = employee_events.pop(index)
        employee_events.append(event)
    def find_index2(self, employee_events: list[MedicalDate], event_finished_id: int) -> int:
        for index in range(len(employee_events)):
            if employee_events[index].id == event_finished_id:
                return index
        return None
   














































# a= datetime.time(0,0)
# print(a)



    # todo hacer un for para instanciar los recursos

# print(datetime.datetime.strptime("2025-Oct-11","%Y-%b-%d").date().strftime("%Y-%b-%d"))
# print(calendar.month(2025,10))
# date= datetime.date(2025,10,20)
# print(holidays.country_holidays("FR", years=2025).get_closest_holiday(date))
# print(datetime.datetime.now())
# class A:
#     def __init__(self):
#         pass
    
#     lista=[]
#     a=10

#     def add_to_list(self):
#         x=B(self.a)
#         self.lista.append(x)

# class B: 
#     def __init__(self,num):
#         self.num=num   

# clase1=A()
# clase1.add_to_list()
# clase1.a=5
# clase2=clase1.lista.pop()
# clase1.add_to_list()
# clase3=clase1.lista.pop()
# print(clase2.num)
# print(clase3.num)
# appointment_date: datetime.date = datetime.datetime.strptime("2025/Oct/12","%Y/%b/%d").date()
# actual_datetime = datetime.datetime.now()
# actual_date = actual_datetime.date() 
# print(type(appointment_date)==type(actual_date))
# print(type(appointment_date))
# print(type(actual_date))
