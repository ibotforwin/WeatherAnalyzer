import plotly.offline as py
import plotly.graph_objs as go
from ..models import WeatherDataRow
def return_plot_div(parent_file_id, date__range):
    graph_date = []
    graph_min_temp = []
    graph_max_temp = []
    graph_mean_temp = []
    graph_heat_degree_days = []
    graph_total_rain = []
    graph_total_snow = []
    graph_speed_max_gusts = []
    weather_data = WeatherDataRow.objects.filter(parent_file_id=parent_file_id,
                                                 date__range=date__range)
    for data in weather_data:
        graph_date.append(data.date)
        graph_min_temp.append(data.min_temp)
        graph_max_temp.append(data.max_temp)
        graph_mean_temp.append(data.mean_temp)
        graph_heat_degree_days.append(data.heat_degree_days)
        graph_total_rain.append(data.total_rain)
        graph_total_snow.append(data.total_snow)
        graph_speed_max_gusts.append(data.speed_max_gusts)
    graph_data = [
        go.Scatter(
            name='Min Temp',
            x=graph_date,
            y=graph_min_temp,
        ),
        go.Scatter(
            name='Max Temp',
            x=graph_date,
            y=graph_max_temp,
        ),
        go.Scatter(
            name='Mean Temp',
            x=graph_date,
            y=graph_mean_temp,
        ),
        go.Scatter(
            name='Heat Degree Days',
            x=graph_date,
            y=graph_heat_degree_days,
        ),
        go.Scatter(
            name='Total Rain',
            x=graph_date,
            y=graph_total_rain,
        ),
        go.Scatter(
            name='Total Snow',
            x=graph_date,
            y=graph_total_snow,
        ),
        go.Scatter(
            name='Speed Max Gusts',
            x=graph_date,
            y=graph_speed_max_gusts,
        )
    ]
    layout = go.Layout(
        xaxis=dict(
            title='x'
        ),

        yaxis=dict(
            title='Value',
            hoverformat='.2f'
        ),
    )
    fig = go.Figure(data=graph_data, layout=layout)
    plot_div = py.plot(fig, include_plotlyjs=True, output_type='div')
    return plot_div


