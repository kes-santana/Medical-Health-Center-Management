from Backend.Data_Access.context import Context
from Backend.Features.Events.List.list_events_command import ListEventsCommand
from Backend.Features.dtos.eventdto import EventDto


class ListEventCommandHandler:
    def __init__(self, command: ListEventsCommand):
        self.command = command

    context = Context()
    manager = context.get_repo_date_manager()

    def execute(self) -> list[EventDto]:
        events = self.manager.get_all()
        result = []
        query = self.command.query
        for e in events:
            if query == "" or e.appointment_name in query or e.employee.name in query or e.owns_name in query:
                result.append(EventDto.to_event_dto(e))
        result.sort(key= lambda x: x.date)
        return result