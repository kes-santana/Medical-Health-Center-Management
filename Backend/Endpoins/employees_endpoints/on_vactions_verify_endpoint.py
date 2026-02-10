from datetime import datetime

from Backend.Data_Access.context import Context
from Backend.Domain.employee import Employee


class VerifyVacations:
    
    def excecute(self):
        context = Context()
        repo = context.get_repo_employee()
        employees: list[Employee]= repo.get_all()
        today = datetime.now().date() 
        for e in employees:
            if e.vacations:
                if e.vacations[0] <= today <= e.vacations[1]:
                    e.on_vacations = True
                if today < e.vacations[0] or e.vacations[1] < today:
                    e.on_vacations = False
        context.save(repo)
        