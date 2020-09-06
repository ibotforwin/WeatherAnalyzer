from django.shortcuts import render
from .forms import UploadedDocumentForm
import csv
from .components.weather_data_table_class import WeatherDataTable
from .models import WeatherDataRow
from django_tables2.export.export import TableExport
from .components.graph_data import return_plot_div
from .components.email_on_upload import send_email_upload


def index(request):
    # We always want to show a form in case a user wants to upload a different file to work with.
    form = UploadedDocumentForm(request.POST, request.FILES)
    list_of_columns_names = ['date', 'min_temp', 'max_temp', 'mean_temp', 'heat_degree_days', 'total_rain',
                             'total_snow', 'speed_max_gusts']
    if request.method == 'POST':

        # Runs when a new file is uploaded
        if "uploading_file" in request.POST:
            request.session['list_of_excluded'] = ['parent_file', 'id']
            request.session['columns'] = list_of_columns_names
            request.session['date__range'] = None
            csv_as_list = []
            if form.is_valid():
                document_object = form.save()
                is_document_valid = True
            else:
                form = UploadedDocumentForm()
                is_document_valid = False

            # Validating CSV file

            # Checking file validity
            if is_document_valid == False:
                message = 'This is an invalid document upload. Please try again and ensure you are using a .csv file.'
                return render(request, 'weather/index.html', {'form': form, 'message': message})
            # If file valid, read document.
            reader = csv.reader(open(document_object.document.path, 'r'))

            # Assign first row to column_names, check for content and length
            column_names=next(reader)
            if len(column_names) != 31:
                message = 'The CSV file does not contain enough columns. Please check to make sure you are using the correct .csv file.'
                return render(request, 'weather/index.html', {'form': form, 'message': message})
            required_column_names=['Longitude', 'Latitude', 'Station Name', 'Climate ID', 'Date/Time', 'Year', 'Month', 'Day', 'Data Quality', 'Max Temp', 'Max Temp Flag', 'Min Temp', 'Min Temp Flag', 'Mean Temp', 'Mean Temp Flag', 'Heat Deg Days', 'Heat Deg Days Flag', 'Cool Deg Days', 'Cool Deg Days Flag', 'Total Rain', 'Total Rain Flag', 'Total Snow', 'Total Snow Flag', 'Total Precip', 'Total Precip Flag', 'Snow on Grnd', 'Snow on Grnd Flag', 'Dir of Max Gust', 'Dir of Max Gust Flag', 'Spd of Max Gust', 'Spd of Max Gust Flag']
            # Iterating instead of checking required_column_names==column_names. Non-standard characters might cause error otherwise.
            for i, required_content in enumerate(required_column_names):
                if required_content not in column_names[i]:
                    message = 'The names of the columns do not match the required format.'
                    return render(request, 'weather/index.html', {'form': form, 'message': message})

            # Send admin email after validation
            send_email_upload()

            # TODO Check if excel file is valid, maybe check column titles, value existence, and file extension. Return meaningful error to user in the form of a message.
            # Iterating through reader and appending relevant data to a list, reader already starts on second row (first numerical data) due to earlier next function called on reader.
            for i, row in enumerate(reader):
                for j, item in enumerate(row):
                    file_end_date=row[4]
                    if item == '':
                        row[j] = 0
                    if '<' in item:
                        row[j] = int(item.replace('<', ''))
                    if '>' in item:
                        row[j] = int(item.replace('>', ''))
                csv_as_list.append(
                    WeatherDataRow(parent_file=document_object, date=row[4], min_temp=row[11],
                                   max_temp=row[9], mean_temp=row[13], heat_degree_days=row[15], total_rain=row[19],
                                   total_snow=row[21], speed_max_gusts=row[29]))
                if i==0:
                    file_start_date=row[4]
            request.session['date__range'] = [file_start_date, file_end_date]
            WeatherDataRow.objects.bulk_create(csv_as_list)
            table = WeatherDataTable(WeatherDataRow.objects.filter(parent_file_id=document_object.id),
                                     exclude=('parent_file', 'id',))
            request.session['document_id'] = document_object.id

            # return_plot_div is a function from /components/ which returns a plot_div
            plot_div = return_plot_div(parent_file_id=request.session['document_id'])
            is_active_file = True

            data = {
                'is_active_file': is_active_file,
                'table': table,
                'dates': {'start_date': file_start_date, 'end_date': file_end_date},
                'columns': {'date': True, 'min_temp': True, 'max_temp': True,
                            'mean_temp': True, 'heat_degree_days': True, 'total_rain': True, 'total_snow': True,
                            'speed_max_gusts': True},
                'plot_div': plot_div
            }
            return render(request, 'weather/index.html', {'form': form, 'data': data})

        # Runs upon date range submission.
        if "date_picker_submit" in request.POST:
            list_of_excluded = request.session['list_of_excluded']
            if request.POST['start_date'] != '':
                request.session['start_date'] = request.POST['start_date']
                request.session['end_date'] = request.POST['end_date']
                request.session['date__range'] = [request.POST['start_date'], request.POST['end_date']]

            try:
                table = WeatherDataTable(WeatherDataRow.objects.filter(parent_file_id=request.session['document_id'], date__range=request.session['date__range']), exclude=tuple(request.session['list_of_excluded']))
            except:
                list_of_excluded = ['parent_file', 'id']
                table = WeatherDataTable(WeatherDataRow.objects.filter(parent_file_id=request.session['document_id'],
                                                                       date__range=request.session['date__range']),
                                         exclude=('parent_file', 'id',))
            is_active_file = True

            # TODO Check if date is earlier than today's date or not. Maybe we should not be showing 0 value future weather.
            columns = {}
            for item in list_of_columns_names:
                if item not in list_of_excluded:
                    columns[item] = True
            request.session['columns'] = columns

            # return_plot_div is a function from /components/ which returns a plot_div
            plot_div = return_plot_div(parent_file_id=request.session['document_id'],
                                       date__range=request.session['date__range'])

            data = {
                'is_active_file': is_active_file,
                'table': table,
                'dates': {'start_date': request.session['start_date'], 'end_date': request.session['end_date']},
                'columns': columns,
                'plot_div': plot_div
            }

            return render(request, 'weather/index.html', {'form': form, 'data': data})

        # Performs CSV/JSON export download
        if 'export_' in request.POST:
            if request.session['date__range']:
                if request.session['list_of_excluded']:
                    table = WeatherDataTable(
                        WeatherDataRow.objects.filter(parent_file_id=request.session['document_id'],
                                                      date__range=request.session['date__range']),
                        exclude=tuple(request.session['list_of_excluded']))
                else:
                    table = WeatherDataTable(
                        WeatherDataRow.objects.filter(parent_file_id=request.session['document_id'],
                                                      date__range=request.session['date__range']))
            else:
                if request.session['list_of_excluded']:
                    table = WeatherDataTable(
                        WeatherDataRow.objects.filter(parent_file_id=request.session['document_id'],
                                                      ), exclude=tuple(request.session['list_of_excluded']))
                else:
                    table = WeatherDataTable(
                        WeatherDataRow.objects.filter(parent_file_id=request.session['document_id'],
                                                      ))
            if request.POST['export_'] == 'csv':
                export_format = request.GET.get("_export", 'csv')
            if request.POST['export_'] == 'json':
                export_format = request.GET.get("_export", 'json')
            exporter = TableExport(export_format, table)
            return exporter.response('File_Name.{}'.format(export_format))

        # Runs on update column to change displayed and exported columns
        if 'update_columns' in request.POST:
            columns = {'date': True, 'min_temp': True, 'max_temp': True,
                       'mean_temp': True, 'heat_degree_days': True, 'total_rain': True, 'total_snow': True,
                       'speed_max_gusts': True}
            list_of_excluded = ['parent_file', 'id']
            for item in list_of_columns_names:
                if item not in request.POST:
                    list_of_excluded.append(item)
                    columns[item] = False
            request.session['columns'] = columns
            request.session['list_of_excluded'] = list_of_excluded
            try:
                table = WeatherDataTable(WeatherDataRow.objects.filter(parent_file_id=request.session['document_id'],
                                                                       date__range=request.session['date__range']),
                                         exclude=tuple(list_of_excluded))
            except:
                table = WeatherDataTable(WeatherDataRow.objects.filter(parent_file_id=request.session['document_id']),
                                         exclude=tuple(list_of_excluded))

            # return_plot_div is a function from /components/ which returns a plot_div
            plot_div = return_plot_div(parent_file_id=request.session['document_id'],
                                       date__range=request.session['date__range'])

            is_active_file = True
            data = {
                'is_active_file': is_active_file,
                'table': table,
                'dates': {'start_date': request.session['start_date'], 'end_date': request.session['end_date']},
                'columns': columns,
                'plot_div': plot_div
            }
            return render(request, 'weather/index.html', {'form': form, 'data': data})
    return render(request, 'weather/index.html', {'form': form})
