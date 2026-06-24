
from backend.data_access.context import Context
from backend.domain.resources import Resource


class RemoveUseWithEndpoint:

    def excecute(self,resource_id: int, restricted_resource_id: int) -> None:
        
        context = Context()
        resources_repo = context.get_repo_resource()
        resource_id: Resource = resources_repo.get_by_id(resource_id)
    

        for r in range(len(resource_id.use_with)):
            if resource_id.use_with[r] == restricted_resource_id:
                resource_id.use_with.pop(r)
                resources_repo.to_dict()
                context.save(resources_repo)
                print(f'Para usar el recurso: "{resource_id.name}" ya no es necesario el recurso de ID: {restricted_resource_id}')
                return
        
        raise Exception(f'El recurso "{resource_id.name}" no era necesario usarlo con el recurso de ID: {restricted_resource_id}')
