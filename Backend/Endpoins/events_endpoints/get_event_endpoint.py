
from backend.features.events.get.get_event_command import GetEventCommand
from backend.features.events.get.get_event_command_handler import GetEventHandler


class GetEventEndpoint:

    def excecute(self, event_id: int):
        command = GetEventCommand(event_id)
        handler = GetEventHandler(command)
        response = handler.excecute()
        return response