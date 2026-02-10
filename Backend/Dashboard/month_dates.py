from datetime import datetime
from Backend.Data_Access.context import Context


class MonthDates:
    
    def excecute(self):    
        context = Context()
        manager = context.get_repo_date_manager()
        all_events = manager.get_all()
        actual_month = datetime.now().month
        month_events= {}
        filter = lambda month, evnt: evnt.date_time.month == month
        for e in all_events:
            if filter(actual_month, e):

                if not e.date_time.day in month_events.keys():
                    month_events[e.date_time.day] = e.is_urgency
                if e.is_urgency and not month_events[e.date_time.day]:
                    month_events[e.date_time.day] = True
        
        return month_events
  