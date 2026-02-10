from Backend.Domain.medical_date import MedicalDate


class EventDto():
    def __init__(self):
        self.id : int
        self.state: str
        self.name : str
        self.doctor : str
        self.patient: str
        self.date: str
        self.time: str

    @staticmethod
    def to_event_dto(event: MedicalDate) -> 'EventDto':
        dto = EventDto()
        dto.id = event.id,
        dto.state = event.state
        dto.name = event.appointment_name
        dto.doctor = event.employee.name
        dto.patient = event.owns_name
        dto.date = str(event.date_time.date())
        dto.time = str(event.date_time.time())
        return dto
    
    def __str__(self):
        return f"Event: \n \
            Name: {self.name} \n \
            Doctor: {self.doctor} \n \
            Date: {self.date} \n \
            Time: {self.time} \n \
            Patient {self.patient} \n"
            