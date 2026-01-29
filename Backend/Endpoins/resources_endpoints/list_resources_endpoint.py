from Backend.Data_Access.context import Context
from Backend.Features.dtos.resource_dto import ResourceDto


class ListResourcesEndpoint:

    def excecute(self):
        context = Context()
        resource_repo = context.get_repo_resource()
        resource_list = resource_repo.get_all()
        return [ResourceDto.to_resource_dto(e) for e in resource_list]