import datetime
from dateutil.relativedelta import relativedelta
import plotly.graph_objects as go

from Backend.Data_Access.context import Context
from Backend.Domain.medical_date import MedicalDate


class ResourcePerMonthGraphix:
    def __init__(self, fecha: datetime.date, recursos_id: list[int]):
        self.date: datetime.date = fecha
        self.resources = recursos_id
    
    def excecute(self):
        context = Context()
        resource_repo = context.get_repo_resource()
        all_events: list[MedicalDate] = context.get_repo_date_manager().get_all()
        resources = [resource_repo.get_by_id(e) for e in self.resources]

        filter_act_month = lambda evnt: evnt.date_time.month == self.date.month and evnt.date_time.year == self.date.year
        act_month_evnts: list[MedicalDate] = []
        for e in all_events:
            if filter_act_month(e):
                act_month_evnts.append(e)

        
        act_rec_counts = {}
        for r in resources:
            act_rec_counts[r.name] = 0
            for e in act_month_evnts:
                for nr in e.necesary_resources:
                    if r.id == nr.id:
                        act_rec_counts[r.name] += e.resources_count[e.necesary_resources.index(nr)]


        last_month = self.date - relativedelta(months=1)
        filter_last_month = lambda evnt: evnt.date_time.month == last_month.month and evnt.date_time.year == last_month.year
        last_month_evnts: list[MedicalDate] = []
        for e in all_events:
            if filter_last_month(e):
                last_month_evnts.append(e)

        last_rec_counts = {}
        for r in resources:
            last_rec_counts[r.name] = 0
            for e in last_month_evnts:
                for nr in e.necesary_resources:
                    if r.id == nr.id:
                        last_rec_counts[r.name] += e.resources_count[e.necesary_resources.index(nr)]
            

        # Calcular diferencias
        diferencias = {r.name: act_rec_counts[r.name] - last_rec_counts[r.name] for r in resources }
        
        # Preparar datos para graficar
        recursos = [r.name for r in resources]
        fig = go.Figure() 
        fig.add_trace(go.Bar( x=recursos, y=[act_rec_counts[r.name] for r in resources], name="Mes investigado" ))
        fig.add_trace(go.Bar( x=recursos, y=[last_rec_counts[r.name] for r in resources], name="Mes anterior" ))
        fig.add_trace(go.Bar( x=recursos, y=[diferencias[r.name] for r in resources], name="Diferencia" ))
        
        # Agrupar barras por recurso
        fig.update_layout( barmode='group', title="Uso de recursos por mes", xaxis_title="Recurso", yaxis_title="Cantidad" )
        return fig