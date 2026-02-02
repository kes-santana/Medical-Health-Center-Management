

class Resource:
    """Representa los recursos"""

    def __init__(self, id: int, name: str, count: int, is_espendable: bool, use_state: str="active",
                use_with: list[int]=[], dont_use_with: list[int]=[]):
        """Inicializa la clase Recursos"""

        self.id: int = id
        self.name: str = name
        self.key = f"{id} {name}"
        self.use_with: list[int] = use_with
        self.dont_use_with: list[int] = dont_use_with
        self.use_state: str = use_state  
        self.count: int = count 
        self.is_espendable: bool = is_espendable

    def verificar_dependencias(self, resource_repo):
        for i in self.use_with:
            if i in self.dont_use_with:
                raise Exception("No puede usar y no usar un recurso al mismo tiempo")

        for u in self.use_with:
            r: Resource = resource_repo.resource_list.get(str(u), None)
            if r == None:
                raise Exception(f'El recurso de ID: "{u}" no se encuentra en base de datos')

            for d_u_w in r.dont_use_with:
                if d_u_w in self.use_with:
                    raise Exception(f'El recurso "{r.name}" no puede usarse con el recurso con ID: "{d_u_w}" y este ultimo esta en la lista de recursos a usarse')
     
            for u_w in r.use_with:
                if u_w in self.dont_use_with:
                    raise Exception(f'El recurso "{r.name}" nesecita usarse con el recurso de ID: "{u_w}" y este ultimo esta en la lista de recursos restringidos a no usarse')
                
    def revisar_codependencias(self, resource_repo):
        for u in self.use_with:
            r: Resource = resource_repo.resource_list[str(u)]
            if self.id in r.dont_use_with:
                raise Exception(f'El recurso "{self.name}" no puede usarse con el recurso "{r.name}" porque el primero esta en los restringidos a no usarse con el recurso {r.name}. Si quiere realizar esta accion retire la restriccion de uso de "{r.name}" respecto a "{self.name}"')

        for d in self.dont_use_with:
            r: Resource = resource_repo.resource_list[str(d)]
            if self.id in r.use_with:
                raise Exception(f'El recurso "{self.name}" no puede restringirse a no usarse con el recurso "{r.name}" porque el primero esta en los recursos a usarse con el recurso {r.name}. Si quiere realizar esta accion retire la restriccion de no uso de "{r.name}" respecto a "{self.name}"')


    def to_dict(self) -> dict:
        """Convierte el recurso a un diccionario"""

        return {
            "id": self.id,
            "name": self.name,
            "key": self.key,
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
