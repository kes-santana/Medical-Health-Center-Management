
from Backend.Data_Access.context import Context
from Backend.Features.Events.Get.get_event_command import GetEventCommand
from Backend.Features.Events.Get.get_event_response import GetEventResponse


class GetEventHandler:
    def __init__(self, command: GetEventCommand):
        self.command = command
    
    # todo donde debe ir esto aqui o dentro del innit
    context = Context()
    manager = context.get_repo_date_manager()

    def get_event(self) -> GetEventResponse:
       
        event = self.manager.get_by_id(self.command.event_id)
        necesary_resources = [r.name for r in event.necesary_resources]
        
        return GetEventResponse(event.state, event.id, event.date_time, event.duration, 
                                event.employee.name, event.appointment_name, event.is_urgency,
                                necesary_resources, event.owns_name)
    