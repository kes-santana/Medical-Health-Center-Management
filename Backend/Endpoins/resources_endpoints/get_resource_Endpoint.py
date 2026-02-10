from Backend.Data_Access.context import Context
from Backend.Features.dtos.resource_dto import ResourceDto


class GetResourceEndpoint:

    def excecute(self, resource_id: int):
        context = Context()
        resource_repo = context.get_repo_resource()
        resource = resource_repo.get_by_id(resource_id)
        use = [resource_repo.get_by_id(use_r).name for use_r in resource.use_with]
        dont_use = [resource_repo.get_by_id(dont_use_r).name for dont_use_r in resource.dont_use_with]
        resource.use_with = use
        resource.dont_use_with = dont_use
        return ResourceDto.to_resource_dto(resource)
         