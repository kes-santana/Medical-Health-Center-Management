"""El usario pone el id de un evento y se pone en cancelado o en finalizado si esta activo"""


from Backend.Data_Access.context import Context
from Backend.Data_Access.date_manager import DateManager
from Backend.Data_Access.resource_repository import ResourceRepository
from constants import *

class ChangeEventStateEndpiont:
    
    def excecute(self, id: int, new_state: str):
        context: Context = Context()
        manager: DateManager = context.get_repo_date_manager()
        if new_state == "canceled":
            resource_repo: ResourceRepository = context.get_repo_resource()
            event = manager.get_by_id(id)
            for r in range(len(event.necesary_resources)):
                if event.necesary_resources[r].is_espendable:
                   rec = resource_repo.get_by_id(event.necesary_resources[r].id)
                   rec.count += event.resources_count[r]
            context.save(resource_repo)

        manager.change_state(id, new_state)
        context.save(manager)
        print(f'Se ha actualizado el estado del evento de ID: "{id}" a "{new_state}"')