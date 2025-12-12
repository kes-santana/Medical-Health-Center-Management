from datetime import datetime

# from Backend.Data_Access.context import Context
from Backend.Domain.medical_date import MedicalDate





class DateManager:
    """Representa la clase Cronograma"""
    
    def __init__(self, list_of_events: dict[(datetime.date): dict[str: list[MedicalDate]]]={},
                 actual_id: int=1):
        """Inicializa la clase Cronograma"""
        self.list_of_events : dict[(datetime.date): dict[str: list[MedicalDate]]]  = list_of_events
        self.actual_id : int = actual_id

    def add_event(self, date_time: datetime, doctor_id: str, evento: MedicalDate):
        event_date: datetime.date= date_time.date()
        if event_date in self.list_of_events.keys():
            date_events: dict[str, list[MedicalDate]] = self.list_of_events[event_date]
            if doctor_id in date_events.keys():
                date_events[doctor_id].append(evento)
            else:
                date_events[doctor_id] = [evento]
        else: 
            self.list_of_events[event_date]={}
            self.list_of_events[event_date][doctor_id]=[evento]

        self.actual_id += 1

    def get_all(self, filter=None) -> list[MedicalDate]:
        events: list[MedicalDate] = []
        for date in self.list_of_events.values():
            for doctor_dates in date.values():
                events.extend(doctor_dates)
        if filter is not None:
            for e in events:
                if not filter(e):
                    events.remove(e)
        return events

    def get_by_id(self, id: int): 
        events: list[MedicalDate] = self.get_all()
        for event in events:
            if event.id == id:
                return event
            
        raise Exception(f"El evento de ID: {id} no se encuentra en la base de datos")
        
    def change_state(self, id: int, new_state: str): 
        event = self.get_by_id(id)
        if event.state == new_state:
            raise Exception(f"La cita ya estaba en el estado {new_state}")
                
        if event.state != "active":
            raise Exception(f"No puede actualizar a {new_state} un evento {event.state}")
                
        event.state = new_state
        return 
    
    @staticmethod
    def from_dict(data: list, context) -> "DateManager":
        # Cargar del JSON

        actual_id= data[0]

        # Reconstruir estructura
        list_of_events: dict[datetime.date, dict[str, list[MedicalDate]]] = {}

        for fecha_str, doctor in data[1].items():
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            eventos_por_doctor = {}

            for doctor, eventos in doctor.items():
                eventos_por_doctor[doctor] = [MedicalDate.from_dict(e, context) for e in eventos]

            list_of_events[fecha] = eventos_por_doctor
        
        return DateManager(list_of_events, actual_id)

    def to_dict(self) -> dict: 
    # Convertir a JSON serializable

        data = [self.actual_id,
            {
            fecha.isoformat(): {
                doctor: [evento.to_dict() for evento in eventos]
                for doctor, eventos in doctores.items()
            }
            for fecha, doctores in self.list_of_events.items()
        }]
        return data










# a= datetime.time(0,0)
# print(a)

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
