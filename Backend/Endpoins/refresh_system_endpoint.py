import datetime

from Backend.Data_Access.context import Context

class RefreshSystemEndpoint:
    def __init__(self):
        self.actual_day = datetime.datetime.now()

    def excecute(self):
        context = Context()
        manager = context.get_repo_date_manager()
        all_events = manager.get_all()

        for event in all_events:
            if event.date_time < self.actual_day and event.state == "active":
                event.state = "finished"
                
        context.save(manager)