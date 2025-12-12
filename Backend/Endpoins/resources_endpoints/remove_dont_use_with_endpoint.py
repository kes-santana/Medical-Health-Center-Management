
from Backend.Data_Access.context import Context
from Backend.Domain.resources import Resource


class RemoveDontUseWithEndpoint:
    
   def excecute(self,resource_id: int, restricted_resource_id: int) -> None:
        
        context = Context()
        resources_repo = context.get_repo_resource()
        resource_id: Resource = resources_repo.get_by_id(resource_id)
    
        for r in range(len(resource_id.dont_use_with)):
            if resource_id.dont_use_with[r] == restricted_resource_id:
                resource_id.dont_use_with.pop(r)
                print(f'El recurso "{resource_id.name}" ahora puede ser usado junto al recurso de ID: {restricted_resource_id}')
                resources_repo.to_dict()
                context.save(resources_repo)
                return
            
        raise Exception(f'El recurso "{resource_id.name}" no tenia restriccion de no uso respecto al recurso de ID: {restricted_resource_id}')
