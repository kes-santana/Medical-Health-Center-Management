
import json
from Backend.Domain.resources import Resource


class ResourceRepository:
    def __init__(self, resource_list: dict[int, Resource]):
        self.resource_list : dict[int, Resource] = resource_list
        self.count: int = len(resource_list)

    def get_all_filtered(self, predicate = None) -> list[Resource]:
        if predicate is None:
            return [r for r in self.resource_list.values]
        ans = []
        for i in self.resource_list.values():
            if predicate(i):
                ans.append(i)
        return ans

    def get_by_id(self, id: int) -> Resource:
        # Esta claro lo que hace
        item_finded = None
        items_list: list[Resource] = self.get_all_filtered(predicate=None)
        for item in items_list:
            if item.id == id:
                item_finded = item
                break
        return item_finded
    
    # todo esto va aqui o lo muevo para el endpoint?
    def suply_resources(self, resorces_id: list[int], count: list[int]):
        for i in range(len(resorces_id)):
            resource = self.get_by_id(resorces_id[i])
            if resource is not None:
                resource.count += count[i]

    # todo 
    def save(self, item): 
        pass

    def change_state(self, id: int, new_state: str) -> None:    #todo ajustar params del save
        item = self.get_by_id(id)
        if item != None:
            item.use_state = new_state
            self.save()
        
        else: print(f"No se encontro item con ID: {id}")
        


    @staticmethod
    def from_dict(data: dict) -> "ResourceRepository":
        # Cargar del JSON

        resource_list: dict[int, Resource] = {}
        for id, r in data.items():
            resource_list[id]= Resource.from_dict(r)
        return ResourceRepository(resource_list, len(resource_list))                              

    # todo hacer q se guarde desde el context
    def to_dict(self) -> dict[int, dict]: 
    # Convertir a JSON serializable
        json_ready = {}
        for id, r in self.resource_list.items():
            json_ready[id]= r.to_dict()

        # todo creo q va en context
        with open("eventos.json", "w", encoding="utf-8") as f:
            json.dump(json_ready, f, indent=2, ensure_ascii=False)
