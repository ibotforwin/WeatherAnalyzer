from ..models import WeatherDataRow
import django_tables2 as tables

class WeatherDataTable(tables.Table):
    export_formats = ['csv', 'xls']
    date = tables.Column(orderable=False)
    min_temp = tables.Column(orderable=False)
    max_temp = tables.Column(orderable=False)
    mean_temp = tables.Column(orderable=False)
    heat_degree_days = tables.Column(orderable=False)
    total_rain = tables.Column(orderable=False)
    total_snow = tables.Column(orderable=False)
    speed_max_gusts = tables.Column(orderable=False)

    class Meta:
        model = WeatherDataRow
        attrs = {"class": "table"}
