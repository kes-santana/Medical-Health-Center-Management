
from backend.features.events.list.list_events_command import ListEventsCommand
from backend.features.events.list.list_events_handler import ListEventCommandHandler


class ListEventEndpoint:
    
    def excecute(self ,query: str):
        command = ListEventsCommand(query)
        handler = ListEventCommandHandler(command)
        events = handler.execute()
        return events