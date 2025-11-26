# crea un command, crea un hadle y llama un handle.execute(command_creado)
# esto devuleve una respuesta y esta se manda al front



from Backend.Data_Access.date_manager import DateManager
from Backend.Features.Events.Post.create_event_command import CreateEventCommand
from Backend.Features.Events.Post.create_event_command_handler import CreateEventHandler
from constants import CLOSE_HOUR, OPEN_HOUR

# todo cambiar a no estatico
class CreateEvent:
    def __init__(self):
        pass

    @staticmethod
    def create_event(date_manager: DateManager, date: str, time:str, owns_name: str, employee_name: str,
                     is_urgency: bool, necesary_resources: list[str], asigned_date_time_auto: bool,
                     appointment_name: str):
       
        comand = CreateEventCommand(date, time, owns_name, employee_name, is_urgency, necesary_resources,
                                    asigned_date_time_auto, appointment_name)
        handle = CreateEventHandler(comand, date_manager, OPEN_HOUR, CLOSE_HOUR)
        response = handle.execute()
        # todo ver si falta algo aqui