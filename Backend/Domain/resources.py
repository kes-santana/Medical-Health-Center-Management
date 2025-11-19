import datetime


class Resource:
    """Representa los recursos"""

    def __init__(self, id: int, name: str, use_with: list["Resource"]=[], dont_use_with: list["Resource"]=[]):
        """Inicializa la clase Recursos"""

        self.id: int = id
        self.name: str = name
        self.use_with: list["Resource"] = use_with
        self.dont_use_with: list["Resource"] = dont_use_with
        self.use_state: str = "active"   #todo todavia no lo uso
    
    def to_dict(self) -> dict:
        """Convierte el recurso a un diccionario"""

        return {
            "id": self.id,
            "name": self.name,
            "use_with": [resource.id for resource in self.use_with],
            "dont_use_with": [resource.id for resource in self.dont_use_with],
            "use_state": self.use_state
        }

class Equipment(Resource):
    """Representa los equipos medicos"""

    def __init__(self, id: int, name: str):
        """Inicializa la clase Equipment"""
        super().__init__(id, name) 
    

class Employee():
    """Representa los empleados"""
    def __init__(self, id: int, name: str, especiality: str, experience: int, is_doctor: bool=False):  
        """Inicializa la clase Employee"""

        self.id: int = id
        self.name: str = name
        self.especiality: str = especiality
        self.experience: int = experience       # dict{machine: exp}   #todo agregar a data_base and todavia no lo uso
        # self.is_doctor = is_doctor    # todo ver que hacer con esto a futuro
        self.on_vacations: bool = False
        self.vacations: list[datetime.date] = None          # debe ser una lista con dos datetime.date (inicio y fin)
    def productivity(self) -> datetime.time:
        """returns the duration in minutes of the date"""
        
        if self.experience >=50:
          return datetime.time(minute=15)
      
        elif self.experience >=40 and self.experience < 50:
          return datetime.time(minute=20)
      
        elif self.experience >=20 and self.experience < 40:
            return datetime.time(minute=25)
      
        else: return datetime.time(minute=30)
    
    def to_dict(self) -> dict:
        """Convierte el empleado a un diccionario"""

        return {
            "id": self.id,
            "name": self.name,
            "especiality": self.especiality,
            "experience": self.experience,
            "on_vacations": self.on_vacations,
            "vacations": [date.isoformat() for date in self.vacations] if self.vacations else None
        }
    
class Doctor(Employee):
    """Representa los doctores"""

    def __init__(self, id: int, name: str, especiality: str, experience: dict[str: int], intelligence: int):
        """Inicializa la clase Doctor"""

        super().__init__(id, name, especiality, is_doctor=True)
        self.experience: dict[str: int] = experience
        # self.intelligence = intelligence
        
    def to_dict(self) -> dict:
        s = super().to_dict()
        s.update({
            "experience": self.experience,
            # "intelligence": self.intelligence
        })
        return s
