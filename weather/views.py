from django.shortcuts import render
from .forms import UploadedDocumentForm
import csv
from .models import WeatherDataRow, UploadedDocument
import django_tables2 as tables
from django_tables2.export.views import ExportMixin
from django_tables2.config import RequestConfig
from django_tables2.export.export import TableExport
from datetime import datetime
import plotly.offline as py
import plotly.graph_objs as go
import numpy as np
from .components.graph_data import return_plot_div

def index(request):
    # We always want to show a form in case a user wants to upload a different file to work with.
    form = UploadedDocumentForm(request.POST, request.FILES)
    is_active_file = False
    list_of_columns_names=['date','min_temp','max_temp','mean_temp','heat_degree_days','total_rain','total_snow','speed_max_gusts']
    class WeatherDataTable(tables.Table):
        export_formats = ['csv', 'xls']

        class Meta:
            model = WeatherDataRow
            attrs = {"class": "table"}

    class TableView(ExportMixin, tables.SingleTableView):
        table_class = WeatherDataTable
        model = WeatherDataRow
        template_name = "django_tables2/bootstrap.html"
    if request.method == 'POST':

        #Runs when a new file is uploaded
        if "uploading_file" in request.POST:
            csv_as_list = []
            if form.is_valid():
                document_object = form.save()
            else:
                form = UploadedDocumentForm()
            reader = csv.reader(open(document_object.document.path, 'r'))
            request.session['date__range']=None

            # TODO Check if excel file is valid, maybe check column titles, value existence, and file extension. Return meaningful error to user in the form of a message.
            # Iterating through reader and appending relevant data to a list
            for i, row in enumerate(reader):
                if i > 0:
                    for j, item in enumerate(row):
                        if item=='':
                            row[j]=0
                    csv_as_list.append(
                        WeatherDataRow(parent_file=document_object, date=row[4], min_temp=row[11],
                                       max_temp=row[9], mean_temp=row[13], heat_degree_days=row[15], total_rain=row[19],
                                       total_snow=row[21], speed_max_gusts=row[29]))
            WeatherDataRow.objects.bulk_create(csv_as_list)
            table=WeatherDataTable(WeatherDataRow.objects.filter(parent_file_id=document_object.id), exclude=('parent_file', 'id',))
            request.session['document_id']=document_object.id
            is_active_file = True

            data = {
                'is_active_file': is_active_file,
                'table':table,
                'dates':None,
                'columns':{'date':True,'min_temp':True,'max_temp':True,
                           'mean_temp':True, 'heat_degree_days':True, 'total_rain':True,'total_snow':True,'speed_max_gusts':True},

            }

            return render(request, 'weather/index.html', {'form': form, 'data': data})

        # Runs upon date range submission.
        if "date_picker_submit" in request.POST:
            if request.POST['start_date']!='':
                try:
                    request.session['date__range']=[request.POST['start_date'], request.POST['end_date']]
                except:
                    request.session['date__range'] = ['2020-05-16', '2020-08-16']
            try:
                table = WeatherDataTable(WeatherDataRow.objects.filter(parent_file_id=request.session['document_id'],
                                                                       date__range=request.session['date__range']), exclude=tuple(request.session['list_of_excluded']))
            except:
                list_of_excluded = ['parent_file', 'id']
                table=WeatherDataTable(WeatherDataRow.objects.filter(parent_file_id=request.session['document_id'], date__range=request.session['date__range']), exclude=('parent_file','id',))
            is_active_file = True
            #TODO Check if date is earlier than today's date or not. We should not be showing 0 value future weather.
            try:
                columns=request.session['columns']
                print('try success')
            except:
                columns={'date':True,'min_temp':True,'max_temp':True,
                           'mean_temp':True, 'heat_degree_days':True, 'total_rain':True,'total_snow':True,'speed_max_gusts':True}

            #return_plot_div is a function from /components/ which returns a plot_div
            plot_div=return_plot_div(parent_file_id=request.session['document_id'], date__range=request.session['date__range'])

            data = {
                'is_active_file': is_active_file,
                'table':table,
                'dates':{'start_date':request.POST['start_date'], 'end_date':request.POST['end_date']},
                'columns':columns,
                'plot_div': plot_div
            }
            request.session['start_date']=request.POST['start_date']
            request.session['end_date']=request.POST['end_date']
            return render(request, 'weather/index.html', {'form': form, 'data': data})

        # Performs CSV/JSON export download
        if 'export_' in request.POST:
            if request.session['date__range']:
                if request.session['list_of_excluded']:
                    table = WeatherDataTable(
                        WeatherDataRow.objects.filter(parent_file_id=request.session['document_id'],
                                                      date__range=request.session['date__range']), exclude=tuple(request.session['list_of_excluded']))
                else:
                    table = WeatherDataTable(WeatherDataRow.objects.filter(parent_file_id=request.session['document_id'],
                                                                   date__range=request.session['date__range']))
            else:
                if request.session['list_of_excluded']:
                    table = WeatherDataTable(
                        WeatherDataRow.objects.filter(parent_file_id=request.session['document_id'],
                                                      ), exclude=tuple(request.session['list_of_excluded']))
                else:
                    table = WeatherDataTable(WeatherDataRow.objects.filter(parent_file_id=request.session['document_id'],
                                                                       ))
            if request.POST['export_']=='csv':
                export_format = request.GET.get("_export", 'csv')
            if request.POST['export_'] == 'json':
                export_format = request.GET.get("_export", 'json')
            exporter = TableExport(export_format, table)
            return exporter.response('File_Name.{}'.format(export_format))

        # Runs on update column to change displayed and exported columns
        if 'update_columns' in request.POST:
            columns= {'date': True, 'min_temp': True, 'max_temp': True,
                        'mean_temp': True, 'heat_degree_days': True, 'total_rain': True, 'total_snow': True,
                        'speed_max_gusts': True}
            list_of_excluded=['parent_file','id']
            for item in list_of_columns_names:
                if item not in request.POST:
                    list_of_excluded.append(item)
                    columns[item]=False
            request.session['columns']=columns
            request.session['list_of_excluded']=list_of_excluded
            try:
                table = WeatherDataTable(WeatherDataRow.objects.filter(parent_file_id=request.session['document_id'],
                                                                       date__range=request.session['date__range']), exclude=tuple(list_of_excluded))
            except:
                table = WeatherDataTable(WeatherDataRow.objects.filter(parent_file_id=request.session['document_id']), exclude=tuple(list_of_excluded))
            is_active_file=True
            data = {
                'is_active_file': is_active_file,
                'table':table,
                'dates':{'start_date':request.session['start_date'], 'end_date':request.session['end_date']},
                'columns': columns,
            }
            return render(request, 'weather/index.html', {'form': form, 'data': data})



    return render(request, 'weather/index.html', {'form': form})
