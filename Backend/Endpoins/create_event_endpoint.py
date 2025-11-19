# crea un command, crea un hadle y llama un handle.execute(command_creado)
# esto devuleve una respuesta y esta se manda al front



from Backend.Data_Access.date_manager import DateManager
from Backend.Features.Events.Post.create_event_command import CreateEventComand
from Backend.Features.Events.Post.create_event_command_handler import CreateEventHandler
from constants import CloseHour, OpenHour


class CreateEvent:
    def __init__(self):
        pass

    @staticmethod
    def create_event(date_manager: DateManager, date: str, owns_name: str, employee_name: str, is_urgency: bool,
                     necesary_resources: list[str], appointment_name: str =None):
       
        comand = CreateEventComand(date, owns_name, employee_name, is_urgency, necesary_resources)
        handle = CreateEventHandler(comand, date_manager, OpenHour, CloseHour)
        response = handle.execute()
        # todo ver si falta algo aqui