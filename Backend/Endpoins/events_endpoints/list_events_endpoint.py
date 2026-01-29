
from Backend.Features.Events.List.list_events_command import ListEventsCommand
from Backend.Features.Events.List.list_events_handler import ListEventCommandHandler


class ListEventEndpoint:
    
    def excecute(self ,query: str):
        command = ListEventsCommand(query)
        handler = ListEventCommandHandler(command)
        events = handler.execute()
        return events