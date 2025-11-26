from Backend.Data_Access import context
from Backend.Features.Events.Post.create_event_command import CreateEventCommand
from Backend.Features.Events.Post.create_event_command_handler import CreateEventHandler
from constants import Events

#  py -m Backend.Data_Access.test

# command = CreateEventCommand(
#     "2025/11/20",
#     "10:00",
#     "Kevin",
#     "Miguel",
#     False,
#     [],
# )

# handler = CreateEventHandler(command)
# handler.execute()