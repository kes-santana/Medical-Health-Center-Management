
# from Backend.Endpoins.resources_endpoints.create_resource_endpoint import ResourceCreator
# endppoint= ResourceCreator()
# endppoint.create_resource("tv-led", 2, False, [], [6])
# ---------------------------------------------

# from Backend.Endpoins.resources_endpoints.suply_storehouse_endpoint import SuplyStorehouseEndpoint
# endp = SuplyStorehouseEndpoint()
# endp.suply_storehouse([1,2],[2,3])
# ----------------------------------------------

# from Backend.Endpoins.resources_endpoints.set_new_use_with_endpoint import SetNewUseWithEndpoint
# endp= SetNewUseWithEndpoint()
# endp.excecute(3,1)
# ---------------------------------------------

# from Backend.Endpoins.resources_endpoints.set_new_dont_use_with_endpoint import SetNewDontUseWithEndpoint
# endp = SetNewDontUseWithEndpoint()
# endp.excecute(1,2)
# ----------------------------------------------

# from Backend.Endpoins.resources_endpoints.remove_use_with_endpoint import RemoveUseWithEndpoint
# endp = RemoveUseWithEndpoint()
# endp.excecute(2,1)
# -----------------------------------------------

# from Backend.Endpoins.resources_endpoints.remove_dont_use_with_endpoint import RemoveDontUseWithEndpoint
# endp = RemoveDontUseWithEndpoint()
# endp.excecute(2,3)
# ------------------------------------------------


# from Backend.Endpoins.employees_endpoints.set_employee_vacations_endpoint import EmployeeVacationsSeterEndpoint
# endp= EmployeeVacationsSeterEndpoint()
# endp.excecute(1, "2025/10/8", "2025/12/2")
# -------------------------------------------------

# from Backend.Endpoins.change_state_endpoint import ChangeStateEndpiont
# from constants import RESOURCES
# endp=ChangeStateEndpiont()
# endp.excecute(1, "disponible", RESOURCES)
# --------------------------------------------------

from datetime import datetime
from Backend.Endpoins.employees_endpoints.create_employee_endoint import EmployeeCreatorEndpoint
from Backend.Endpoins.events_endpoints.create_event_endpoint import CreateEventEndpoint
from Backend.Features.Events.Get.get_event_command import GetEventCommand
from Backend.Features.Events.Get.get_event_command_handler import GetEventHandler
from Backend.Features.Events.List.list_events_command import ListEventsCommand
from Backend.Features.Events.List.list_events_handler import ListEventCommandHandler
endpoint = CreateEventEndpoint()
# endpoint.excecute()
# command = GetEventCommand(1)
# handler = GetEventHandler(command)
# response = handler.excecute()

# a =ListEventsCommand("")
# b=ListEventCommandHandler(a)
# c = b.execute()
# d=c

endpoint.excecute(
    date= "2026-2-3",
    time= "17:00:00",
    owns_name= "Lee",
    employee_id= 1,
    is_urgency= False,
    necesary_resources= [1],
    recs_count=[1],
    asigned_date_time_auto= False,
    appointment_name= "Cirugia"
)
                                                                                    
# endp = EmployeeCreatorEndpoint()
# endp.excecute("Alex", 15, True)
# print("se creo el empleado")