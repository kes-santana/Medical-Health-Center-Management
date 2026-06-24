from backend.features.events.post.create_event_command import CreateEventCommand
from backend.features.events.post.create_event_command_handler import CreateEventHandler
from backend.features.events.post.create_event_response import CreateEventResponse


# crea un command, crea un hadle y llama un handle.execute(command_creado)
# esto devuleve una respuesta y esta se manda al front

class CreateEventEndpoint:

    def excecute(self, date: str, time:str, owns_name: str, employee_id: int, is_urgency: bool,
                necesary_resources: list[str], recs_count: list[int], asigned_date_time_auto: bool,
                appointment_name: str, time_auto: bool) -> CreateEventResponse:
       
        comand = CreateEventCommand(date, time, owns_name, employee_id, is_urgency, necesary_resources, recs_count,
                                    asigned_date_time_auto, appointment_name, time_auto)
        handle = CreateEventHandler(comand)
        response = handle.execute()
        return response