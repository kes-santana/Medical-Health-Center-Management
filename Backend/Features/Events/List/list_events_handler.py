from Backend.Data_Access.context import Context
from Backend.Features.Events.List.list_events_command import ListEventsCommand
from Backend.Features.dtos.eventdto import EventDto


class ListEventCommandHandler:
    def __init__(self, command: ListEventsCommand):
        self.command = command
        self.context = Context()
        self.manager = self.context.get_repo_date_manager()

    def execute(self) -> list[EventDto]:
        events = self.manager.get_all()
        result = []
        query = self.command.query
        for e in events:
            if query == "" or e.appointment_name.lower() in query.lower() or e.state.lower() in query.lower() or e.employee.name.lower() in query.lower() or e.owns_name.lower() in query.lower() or str(e.date_time.date().isoformat()) in query:
                result.append(EventDto.to_event_dto(e))
                continue
            if query.lower() in e.appointment_name.lower() or query.lower() in e.employee.name.lower() or query.lower() in e.state.lower() or query.lower() in e.owns_name.lower() or query in str(e.date_time.date().isoformat()):
                result.append(EventDto.to_event_dto(e))
        
        return result