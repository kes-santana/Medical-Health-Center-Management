
from backend.domain.resources import Resource

class ResourceRepository:
    def __init__(self, resource_list: dict[str, Resource]={}):
        self.resource_list : dict[str, Resource] = resource_list
        self.count: int = len(resource_list)


    def get_all(self, filter=None) -> list[Resource]:
        if filter is None:
            return [r for r in self.resource_list.values()]
        ans = []
        for i in self.resource_list.values():
            if filter(i):
                ans.append(i)
        return ans

    def get_by_id(self, id: int) -> Resource:
        # Esta claro lo que hace
        items_list: list[Resource] = self.get_all()
        for item in items_list:
            if item.id == id:
                return item
        
        raise Exception(f"El recurso de ID: {id} no se encuentra en la base de datos")
  
    def suply_resources(self, resorces_id: list[int], count: list[int]):
        for i in range(len(resorces_id)):
            resource = self.get_by_id(resorces_id[i])
            if resource is not None:
                resource.count += count[i]
                if resource.count < 0:
                    resource.count = 0

    def change_state(self, id: int, new_state: str) -> None:
        item = self.get_by_id(id)
        if item != None:
            if item.use_state == new_state:
                raise Exception(f'El recurso recurso con ID: "{id}" ya estaba en el estado "{new_state}"')
            item.use_state = new_state
            return
        
        raise Exception(f'No se encontro recurso con ID: "{id}"')
        
    def load_resources_names(self):
        resources_names = []
        for r in self.resource_list.values():
            if r.count > 0:
                key_split = r.key.split(" ")
                resources_names.append(f"{key_split[0]} - {key_split[1]}")
        
        return resources_names

    @staticmethod
    def from_dict(data: dict) -> "ResourceRepository":
        # Cargar del JSON

        resource_list: dict[int, Resource] = {}
        for id, r in data.items():
            resource_list[id] = Resource.from_dict(r)
        return ResourceRepository(resource_list)                              

    def to_dict(self) -> dict[int, dict]: 
        # Convertir a JSON serializable
        data = {}
        for id, r in self.resource_list.items():
            data[id] = r.to_dict()

        return data