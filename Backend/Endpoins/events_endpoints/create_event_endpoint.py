# crea un command, crea un hadle y llama un handle.execute(command_creado)
# esto devuleve una respuesta y esta se manda al front



from Backend.Data_Access.date_manager import DateManager
from Backend.Features.Events.Post.create_event_command import CreateEventCommand
from Backend.Features.Events.Post.create_event_command_handler import CreateEventHandler
from Backend.Features.Events.Post.create_event_response import CreateEventResponse
from constants import CLOSE_HOUR, OPEN_HOUR

# todo ver que hay q poner en el init
class CreateEventEndpoint:

    def excecute(self, date: str, time:str, owns_name: str, employee_id: int,
                     is_urgency: bool, necesary_resources: list[str], recs_count: list[int], asigned_date_time_auto: bool,
                     appointment_name: str) -> CreateEventResponse:
       
        comand = CreateEventCommand(date, time, owns_name, employee_id, is_urgency, necesary_resources, recs_count,
                                    asigned_date_time_auto, appointment_name)
        handle = CreateEventHandler(comand)
        response = handle.execute()
        return response
        # todo ver si falta algo aqui