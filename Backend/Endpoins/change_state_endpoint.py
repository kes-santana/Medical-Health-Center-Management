"""el usario pone el id de un evento y se pone en cancelado o en finalizado si esta activo"""



from Backend.Data_Access.date_manager import DateManager
from Backend.Data_Access.resource_repository import ResourceRepository
from Backend.Domain.resources import Resource

# todo cambiar a no estatico
class ChangeState:
    def __init__(self):
        pass

    @staticmethod   #todo creo q el name_repo debe ser un str
    def change_event_state(id: int, new_state: str, name_repo: DateManager):
       
       event = name_repo.get_by_id(id)
       if event is not None:
            actual_state: str = event.state
            if actual_state == new_state:
                print(f"La cita ya estaba en el estado {new_state}")
                return
            
            if actual_state != "active":
                print(f"No puede actualizar a {new_state} un evento {actual_state}")
                return

            event.state = new_state
            print(f"Se ha actualizado el evento a {new_state}")

    # todo revisar y ver si lo puedo reducir todo a un solo metodo
    @staticmethod
    def change_resource_state(id: int, new_state: str, name_repo: ResourceRepository):
        item: Resource = name_repo.get_by_id(id)
        if item is not None:
            actual_state: str = item.state
            if actual_state == new_state:
                print(f"El item ya estaba en el estado {new_state}")
                return
            
            item.use_state = new_state
            print(f"Se ha actualizado el item a {new_state}")
