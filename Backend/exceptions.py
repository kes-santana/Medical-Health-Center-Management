import datetime


import datetime

class ExceptionOcurred(Exception):
    def __init__(self, message):
        super().__init__(message)

class EmployeeUnavailableError(Exception): pass
class ResourceConflictError(Exception): pass

try:
    # Intentamos convertir una fecha inválida
    appointment_date = datetime.datetime.strptime("2025/12/32", "%Y/%m/%d").date()
except ValueError as e:
    # Capturamos el error y lanzamos nuestra excepción personalizada
    raise ExceptionOcurred("fecha no válida")
except Exception as e:
    pass