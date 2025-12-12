"""el usario pone el id de un evento y se pone en cancelado o en finalizado si esta activo"""



from Backend.Data_Access.context import Context
from Backend.Data_Access.date_manager import DateManager
from Backend.Data_Access.resource_repository import ResourceRepository
from constants import *

class ChangeStateEndpiont:
    
    def excecute(self, id: int, new_state: str, name_repo: str):
        context: Context = Context()
        if name_repo == EVENTS:
            repo: DateManager = context.get_repo_date_manager()
            objeto = "evento"
        else:
            repo: ResourceRepository = context.get_repo_resource()
            objeto = "recurso"

        repo.change_state(id, new_state)
        context.save(repo)
        print(f'Se ha actualizado el estado del {objeto} de ID: "{id}" a "{new_state}"')