from datetime import datetime

# Simular un enum
EVENTS = "Events"
EMPLOYEES = "Employees"
EQUIPMENT = "Equipment"
SPENDABLE = "Spendable_Resources"
USERS = "Users"

OPEN_HOUR = datetime.strptime("09:00", "%H:%M").time()
CLOSE_HOUR = datetime.strptime("18:00", "%H:%M").time()
MID_DAY = datetime.strptime("12:00", "%H:%M").time()