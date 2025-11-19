"""el usario pone el id de un evento y se pone en cancelado o en finalizado si esta activo"""



from Backend.Data_Access.date_manager import DateManager


class ChangeState:
    def __init__(self):
        pass

    @staticmethod
    def change_state(id: int, new_state: str, name_repo: DateManager):
       
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

