from backend.data_access.context import Context
from backend.domain.resources import Resource


class ResourceCreatorEndpoint:
    
    def excecute(self, name: str, count: int, is_spendable: bool,
                use_with: list[int]=[], dont_use_with: list[int]=[]):
        context = Context()
        resource_repo = context.get_repo_resource()
        new_resource = Resource(resource_repo.count + 1, name, count, 
                                is_spendable, use_with=use_with, dont_use_with=dont_use_with)
        new_resource.verificar_dependencias(resource_repo)
        storehouse_resources = [r.name for r in resource_repo.resource_list.values()]
        
        if new_resource.name in storehouse_resources:
            raise Exception(f"El recurso {new_resource.name} ya se encuentra en el almacen. Tal vez quiso realizar otra accion")
        
        resource_repo.resource_list[new_resource.id] = new_resource
        context.save(resource_repo)
        print("Se ha creado el recurso")

    