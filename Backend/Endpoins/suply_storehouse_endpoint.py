from Backend.Data_Access.context import Context
from Backend.Data_Access.resource_repository import ResourceRepository


class SuplyStorehouse:
    def __init__(self, resorces_id: list[int], count_by_id: list[int]):
        self.resorces_id: list[int] = resorces_id
        self.count_by_id: list[int] = count_by_id

    def suply_storehouse(self):
        context = Context()
        resource_repo: ResourceRepository = context.get_repo_resource()
        resource_repo.suply_resources(self.resorces_id, self.count_by_id)
        resource_repo.to_dict()