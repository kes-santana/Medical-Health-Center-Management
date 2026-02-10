import plotly.express as px
from Backend.Data_Access.context import Context
from datetime import datetime

class EmployeeRankingGraphix:
    def __init__(self, rank_type: str):
        self.rank_type = rank_type
    
    def excecute(self):
        context = Context()
        repo = context.get_repo_date_manager()
        events = repo.get_all()
        data_process = {}
        today = datetime.now().date()
        if self.rank_type == "día":
            filter = lambda today, evnt: evnt.date_time.date() == today

        elif self.rank_type == "mes":
            filter = lambda today, evnt: evnt.date_time.date().month == today.month and evnt.date_time.date().year == today.year

        else:
            filter = lambda today, evnt: evnt.date_time.date().year == today.year
        
        for e in events:
           if filter(today, e):
                if e.employee.name not in data_process:
                    data_process[e.employee.name] = 1
                else:
                    data_process[e.employee.name] += 1
        
        ranking: list[tuple] = []
        for e, count in data_process.items():
            ranking.append((e, count))
        ranking.sort(key=lambda x: x[1])
        empleados = []
        counts = []
        for e in ranking:
            empleados.append(e[0])
            counts.append(e[1])

        # ----Grafico de barras----#

        if not empleados or not counts: 
                # Devuelve un gráfico vacío con mensaje
                fig = px.bar(
                    x=[0],
                    y=["No hay evntos"], 
                    labels={"x": "Cantidad de eventos", "y": "Empleados"},
                    title="No hay eventos en el rango seleccionado" ) 
                fig.update_layout(
                    template="plotly_dark",
                    xaxis=dict(range=[-1, 1]),
                    yaxis=dict(range=[0,0])
                    )
                return fig


        fig = px.bar(
            x=counts,
            y=empleados,
            labels={"x": "Cantidad de eventos", "y": "Empleado"},
            title="Ranking de Empleados",
            color=counts,
            color_continuous_scale="Viridis",
            orientation="h"

        )
        fig.update_layout(
            template="plotly_dark",
            xaxis_tickangle=-45,
            xaxis=dict(type="log")  # fuerza a tratar los eventos como categorías
        )
        return fig
