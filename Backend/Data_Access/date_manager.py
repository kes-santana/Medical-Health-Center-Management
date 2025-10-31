import datetime

from Domain.medical_date import *

# TODO: ver pq no funciona el import


class Cronograma:
    """Representa la clase Cronograma"""
    
    def __init__(self, list_of_events: dict[(datetime.date): dict[str: list[MedicalDate]]]={}):
        """Inicializa la clase Cronograma"""
        self.list_of_events : dict[(datetime.date): dict[str: list[MedicalDate]]]  = list_of_events
       
    # todo ver que hacer co esto a futuro
    actual_datetime: datetime.datetime = datetime.datetime.now()
    actual_date: datetime.date = actual_datetime.date() 
    actual_time: datetime.time =  actual_datetime.time().replace(second=0, microsecond=0)
    
    
# todo meter todo lo que es de validacion en otro script--- listo
    # def add_appointment(self, appointment_date: str, appointment_time: str, owns_name: str, employee: Employee,
    #                     type_classification: str, necesary_resources: list[Resource]) -> MedicalDate:
        
    #     appointment_date, appointment_time = self.is_vald_date(appointment_date, appointment_time)

    #     employee_disponibility = self.employee_disponibility(employee, appointment_date)
    #     if not employee_disponibility:
    #         print("Empleado no disponible")
    #         return #todo lanzar err

    #     date_is_full = self.date_is_full(appointment_date, appointment_time)

    #     if date_is_full and type_classification.lower() != "urgency":
    #         print("No es posible crear la cita por restricciones entre recursos")
    #         return #todo lanzar err
    
    #     resources_valid_to_use = self.validate_necesary_resources(necesary_resources)
       
    #     if not resources_valid_to_use:
    #         print("No es posible crear la cita por restricciones entre recursos")
    #         return #todo lanzar err
        


    #     # TODO
    #     new_appointment=MedicalDate(self.actual_id,appointment_date,appointment_time,owns_name,employee,type_classification,necesary_resources)
    #     self.actual_id+=1

        
    #     # on_vacations =0
    #     # vacations=0
    # def is_vald_date(self, appointment_date: str, appointment_time: str) -> tuple[datetime.date, datetime.time]:
     
    #     #todo hacer un try por si la fecha no es valida
        
    #     appointment_date: datetime.date = datetime.datetime.strptime(appointment_date,"%Y/%b/%d").date()
    #     appointment_time: datetime.time = datetime.datetime.strptime(appointment_time, "%H:%M").time()
        
    #     if appointment_date.weekday() in [5, 6] or appointment_date in holidays.CountryHoliday("US", appointment_date.year):
    #         print("Dia no laborable") #todo lanzar err
    #         return
        
    #     if appointment_time < self.open_hour or appointment_time > self.close_hour:
    #         print("Hora fuera de rango") #todo lanzar err
    #         return
        
    #     if appointment_date >= self.actual_date:
    #         if appointment_date > self.actual_date:
    #             return (appointment_date, appointment_time)

    #         else: 
    #             if appointment_time >= self.actual_time:
    #                return (appointment_date, appointment_time)
    #             else:
    #                 print("No puede agendar cita en una hora pasada") #todo lanzar err
    #                 return

    #     else:
    #         print("No puede agendar cita en una fecha pasada") #todo lanzar err
    #         return
    # def date_is_full(self, appointment_date: datetime.date, appointment_time: datetime.time) -> bool:
    #     pass
    # def validate_necesary_resources(self, necesary_resources: list[Resource]) -> bool:
    #     pass #todo ver si poner lo en la class restriction y q esa clase maneje todas las restricciones
    # def employee_disponibility(self, employee: Employee, appointment_date: datetime.date) -> bool:
    #     pass #todo ver si poner lo en la class restriction y q esa clase maneje todas las restricciones




a= datetime.time(0,0)
print(a)



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
