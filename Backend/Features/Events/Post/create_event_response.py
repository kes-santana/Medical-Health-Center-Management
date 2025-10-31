"""aqui se crea y mosdela lo que se envia a la app"""

class CreateEventResponse:
    def __init__(self, date, owns_name, employee):
        self.date = date
        self.owns_name = owns_name
        self.employee = employee