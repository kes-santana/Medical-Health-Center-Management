from datetime import datetime, time

class GetEventResponse:
    def __init__(self, event_state: str, event_id: int, event_date_time: datetime, 
                event_duration: time, event_employee: str, event_appointment_name: str,
                event_is_urgency: bool, necesary_resources: list[str], event_owns_name: str):
        
        self.event_state: str = event_state
        self.event_id: int = event_id
        self.event_date_time: datetime = event_date_time
        self.event_duration: time = event_duration
        self.event_employee: str = event_employee
        self.event_appointment_name: str = event_appointment_name
        self.event_is_urgency: bool = event_is_urgency
        self.necesary_resources: list[str] = necesary_resources
        self.event_owns_name: str = event_owns_name 