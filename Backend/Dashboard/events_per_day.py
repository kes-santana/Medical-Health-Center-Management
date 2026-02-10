import plotly.express as px
from datetime import datetime
from Backend.Data_Access.context import Context

class EventPerDayGraphix:
    def __init__(self, start_date: datetime.date, end_date: datetime.date, graph_type: str):
        self.start_date = start_date
        self.end_date = end_date
        self.graph_type = graph_type
    
    def execute(self):
        context = Context()
        repo = context.get_repo_date_manager()
        events = repo.get_all()
        filter = lambda start_date, end_date, evnt: start_date <= evnt.date_time.date() <= end_date
        range_events = {}
        for e in events:
            if filter(self.start_date, self.end_date, e):
                fecha = e.date_time.date()
                if fecha not in range_events:
                    range_events[fecha] = 1
                else:
                    range_events[fecha] += 1
        
        # Convertimos a listas ordenadas por fecha
        dates = sorted(range_events.keys())
        counts = [range_events[d] for d in dates]

        # Creamos el gráfico moderno con Plotly

        if self.graph_type == "barras":

            # ----Grafico de barras----#

            # --- Manejo de caso sin datos --- #
            if not dates or not counts: 
                # Devuelve un gráfico vacío con mensaje
                fig = px.bar(
                    x=[0],
                    y=["No hay evntos"], 
                    labels={"x": "Fecha", "y": "Cantidad de eventos"},
                    title="No hay eventos en el rango seleccionado" ) 
                fig.update_layout(template="plotly_dark")
                return fig

            fig = px.bar(
                x=dates,
                y=counts,
                labels={"x": "Fecha", "y": "Cantidad de eventos"},
                title="Eventos por día",
                color=counts,
                color_continuous_scale="Viridis"
            )
            fig.update_layout(
                template="plotly_dark",
                xaxis_tickangle=-45,
                xaxis=dict(type="category")  # fuerza a tratar las fechas como categorías
            )
            return fig

        else:
            #----Grafico de Linea----#

            if not dates or not counts: 
                # Devuelve un gráfico vacío con mensaje
                fig = px.bar(
                    x=[0],
                    y=["No hay evntos"], 
                    labels={"x": "Fecha", "y": "Cantidad de eventos"},
                    title="No hay eventos en el rango seleccionado"
                    ) 
                fig.update_layout(template="plotly_dark")
                return fig
            
            fig = px.line(
            x=dates,
            y=counts,
            labels={"x": "Fecha", "y": "Cantidad de eventos"},
            title="Eventos por día"
            )
            return fig
