from Backend.Data_Access.context import Context
from Backend.Features.Events.List.list_events_command import ListEventsCommand
from Backend.Features.dtos.eventdto import EventDto


class ListEventCommandHandler:
    def __init__(self, command: ListEventsCommand):
        self.command = command

    context = Context()
    manager = context.get_repo_date_manager()

    def execute(self):
        events = self.manager.get_all()
        result = []
        query = self.command.query
        for e in events:
            if query in e.appointment_name or query in e.employee.name or query in e.owns_name:
                result.append(EventDto.to_event_dto(e))
        return result.sort(key= lambda x: x.date)