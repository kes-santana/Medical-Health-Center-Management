"""aqui se crea y mosdela lo que se envia a la app"""

import datetime


class CreateEventResponse:
    def __init__(self, id: int, date: datetime.datetime, owns_name: str, employee: str):
        self.date = date
        self.owns_name = owns_name
        self.employee = employee
        self.id = id
        