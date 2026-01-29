import datetime

from Backend.Data_Access.context import Context
from Frontend.front_utils import load_emp_names, load_rec_names # Todo: esto esta bien?


class RefreshSystemEndpoint:
    def __init__(self):
        self.actual_day = datetime.datetime.now().date()

    def excecute(self) -> tuple[list[str], list[str]]:
        resources_names = load_rec_names()
        employees_keys = load_emp_names()
        context = Context()
        manager = context.get_repo_date_manager()
        resource_repo = context.get_repo_resource()
        all_events = manager.get_all()

        for event in all_events:
            if event.date_time.date() < self.actual_day and event.state == "active":
                event.state = "finished"
                for r in range(len(event.necesary_resources)):
                    if not event.necesary_resources[r].is_espendable:
                        resource = resource_repo.get_by_id( event.necesary_resources[r].id)
                        resource.count += event.resources_count[r]

        context.save(resource_repo)
        context.save(manager)
        return resources_names, employees_keys