from Backend.Data_Access.context import Context
from Backend.Data_Access.resource_repository import ResourceRepository


class SuplyStorehouseEndpoint:

    def excecute(self, resorces_id: list[int], count_by_id: list[int]): 
        context = Context()
        resource_repo: ResourceRepository = context.get_repo_resource()
        resource_repo.suply_resources(resorces_id, count_by_id)
        resource_repo.to_dict()
        context.save(resource_repo)
        print("Se ha abastecido el almacen")