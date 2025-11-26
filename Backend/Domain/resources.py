import datetime

#  todo agregar al validador de recursos que si no es gastable solo debe revisar el estado
class Resource:
    """Representa los recursos"""

    def __init__(self, id: int, name: str, count: int, is_espendable: bool, use_state: str="active",
                use_with: list[int]=[], dont_use_with: list[int]=[]):
        """Inicializa la clase Recursos"""

        self.id: int = id
        self.name: str = name
        self.use_with: list[int] = use_with
        self.dont_use_with: list[int] = dont_use_with
        self.use_state: str = use_state  
        self.count: int = count 
        self.is_espendable: bool = is_espendable

    def to_dict(self) -> dict:
        """Convierte el recurso a un diccionario"""

        return {
            "id": self.id,
            "name": self.name,
            "use_with": self.use_with,
            "dont_use_with": self.dont_use_with,
            "use_state": self.use_state,
            "count": self.count,
            "is_espendable": self.is_espendable
        }
    
    @staticmethod
    def from_dict(data: dict) -> "Resource":
        return Resource(
            id= data["id"],
            name= data["name"],
            use_state= data["use_state"],
            use_with= data["use_with"],
            dont_use_with= data["dont_use_with"],
            count= data["count"],
            is_espendable= data["is_espendable"]
        )

class Employee():
    """Representa los empleados"""
    def __init__(self, id: int, name: str, experience: int, is_doctor: bool=False,
                 on_vacations: bool=False, vacations: list[datetime.datetime]=[]):  
        """Inicializa la clase Employee"""

        self.id: int = id
        self.name: str = name
        self.key = f"{id} {name}"
        self.experience: int = experience       # dict{machine: exp}  dict[str: int] #todo agregar a data_base and todavia no lo uso
        self.is_doctor = is_doctor              # todo ver que hacer con esto a futuro
        self.on_vacations: bool = on_vacations
        self.vacations: list[datetime.datetime] = vacations  

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
            "experience": self.experience,
            "on_vacations": self.on_vacations,
            "vacations": [date.isoformat() for date in self.vacations] if self.vacations else None
        }
    
    @staticmethod
    def from_dict(data: dict) -> "Employee":
        vacations=[datetime.datetime.strptime(v, "%Y-%M-%d") for v in data[vacations]]
        return Employee(
            id=data["id"],
            name=data["name"],
            experience=data["experience"],
            is_doctor=data["is_doctor"],
            on_vacations=data["on_vacations"],
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
