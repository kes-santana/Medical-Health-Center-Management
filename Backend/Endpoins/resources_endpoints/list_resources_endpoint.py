from Backend.Data_Access.context import Context
from Backend.Features.dtos.resource_dto import ResourceDto


class ListResourcesEndpoint:

    def excecute(self):
        context = Context()
        resource_repo = context.get_repo_resource()
        resource_list = resource_repo.get_all()
        recs = []
        for r in resource_list:
            use = [resource_repo.get_by_id(use_r).name for use_r in r.use_with]
            dont_use = [resource_repo.get_by_id(dont_use_r).name for dont_use_r in r.dont_use_with]
            r.use_with = use
            r.dont_use_with = dont_use
            recs.append(ResourceDto.to_resource_dto(r))
        return recs