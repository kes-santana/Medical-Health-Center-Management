
from Backend.Data_Access.context import Context
from Backend.Domain.resources import Resource

# en el init se puede llamar a un metodo de la misma clase ?
class UseConditionResource:
    def __init__(self, resource_id: int, restricted_resource_id: int):
        self.context = Context()
        self.resources_repo = self.context.get_repo_resource()
        self.resource_id: Resource = self.resources_repo.get_by_id(resource_id)
        self.restricted_resource_id: int = restricted_resource_id
    
    
    # todo hay algun problema si se elimina alguna propiedad del json?
       
    def set_new_use_with(self) -> None:
        
        if self.restricted_resource_id in self.resource_id.use_with:
            print("El recurso ya estaba agregado")
            return
        
        self.resource_id.use_with.append(id)
        print(f"Ahora es necesario usar el recurso {self.resource_id.name} junto al recurso de ID: {self.restricted_resource_id}")
        self.resources_repo.to_dict()
    
    def set_new_dont_use_with(self) -> None:
       
        if self.restricted_resource_id in self.resource_id.use_with:
            print("El recurso ya estaba agregado")
            return
        
        self.resource_id.dont_use_with.append(id)
        print(f"Ahora es necesario que el recurso {self.resource_id.name} no se use junto al recurso de ID: {self.restricted_resource_id}")
        self.resources_repo.to_dict()
    
    def remove_use_with(self) -> None:

        for r in range(len(self.resource_id.use_with)):
            if self.resource_id.use_with[r] == self.restricted_resource_id:
                self.resource_id.use_with.pop(r)
                print(f'Para usar el recurso: "{self.resource_id.name}" ya no es necesario el recurso de ID: {self.restricted_resource_id}')
                return
        
        print(f'El recurso "{self.resource_id.name}" no era necesario usarlo con el recurso de ID: {self.restricted_resource_id}')

    def remove_dont_use_with(self) -> None:
        
        for r in range(len(self.resource_id.dont_use_with)):
            if self.resource_id.dont_use_with[r] == self.restricted_resource_id:
                self.resource_id.dont_use_with.pop(r)
                print(f'El recurso "{self.resource_id.name}" ahora puede ser usado junto al recurso de ID: {self.restricted_resource_id}')
                self.resources_repo.to_dict()
                return
            
        print(f'El recurso "{self.resource_id.name}" no tenia restriccion respecto al recurso de ID: {self.restricted_resource_id}')

