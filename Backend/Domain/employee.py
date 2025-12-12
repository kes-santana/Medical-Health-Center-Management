from datetime import datetime, date, time


class Employee():
    """Representa los empleados"""
    def __init__(self, id: int, name: str, experience: int, is_doctor: bool=False,
                 on_vacations: bool=False, vacations: list[date]=[]):  
        """Inicializa la clase Employee"""

        self.id: int = id
        self.name: str = name
        self.key = f"{id} {name}"
        self.experience: int = experience       # dict{machine: exp}  dict[str: int] #todo todavia no lo uso
        self.is_doctor = is_doctor              # todo ver que hacer con esto a futuro
        self.on_vacations: bool = on_vacations
        self.vacations: list[date] = vacations  

    def productivity(self) -> time:
        """returns the duration in minutes of the date"""
        
        if self.experience >= 50:
          return datetime.strptime("15", "%M").time()
      
        elif self.experience >=40 and self.experience < 50:
          return datetime.strptime("20", "%M").time()
      
        elif self.experience >=20 and self.experience < 40:
            return datetime.strptime("25", "%M").time()
      
        else: return datetime.strptime("30", "%M").time()
    
    def set_vacations(self, start_vacation: date, end_vacation: date) -> None:
        if start_vacation <= end_vacation:
            if self.vacations:
                actual_start = self.vacations[0]
                actual_end = self.vacations[1]
                if (start_vacation >= actual_start and end_vacation >= actual_end):
                    self.vacations[0]= start_vacation
                    self.vacations[1]= end_vacation
                    return
                
                raise Exception("Rango de vacaciones no valido, revise las vacaciones ya existentes")
            
            else: 
                self.vacations.append(start_vacation)
                self.vacations.append(end_vacation)
                return
        
        raise Exception("Rango de vacaciones no valido")
        

    def to_dict(self) -> dict:
        """Convierte el empleado a un diccionario"""

        return {
            "id": self.id,
            "name": self.name,
            "key": self.key,
            "experience": self.experience,
            "is_doctor": self.is_doctor,
            "on_vacations": self.on_vacations,
            "vacations": [date.isoformat() for date in self.vacations] if self.vacations else None
        }
    
    @staticmethod
    def from_dict(data: dict) -> "Employee":
        vacations=[datetime.strptime(v, "%Y-%m-%d").date() for v in data["vacations"]]
        return Employee(
            id=data["id"],
            name=data["name"],
            experience=data["experience"],
            #is_doctor=data["is_doctor"],
            #on_vacations=data["on_vacations"],
            vacations=vacations
            )
    
    
class Doctor(Employee):
    """Representa los doctores"""

    def __init__(self, id: int, name: str, experience: dict[str: int], especiality: str,
                on_vacations: bool=False, vacations: list[datetime.date]=None):
        """Inicializa la clase Doctor"""

        super().__init__(id, name, experience, is_doctor=True, on_vacations=on_vacations, vacations=vacations)
        self.especiality = especiality
        # self.intelligence = intelligence
        
    def to_dict(self) -> dict:
        s = super().to_dict()
        s.update({
            "especiality": self.especiality
            # "intelligence": self.intelligence
        })
        return s
    
    @staticmethod
    def from_dict(data: dict) -> "Doctor":
        vacations=[datetime.datetime.strptime(v, "%Y-%M-%d") for v in data[vacations]]
        return Doctor(
            id=data["id"],
            name=data["name"],
            experience=data["experience"],
            is_doctor=data["is_doctor"],
            on_vacations=data["on_vacations"],
            vacations=vacations,
            especiality=data["especiality"],

            )
