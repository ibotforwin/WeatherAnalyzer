from django.shortcuts import render
from .forms import UploadedDocumentForm
import csv
from .models import WeatherDataRow, UploadedDocument
import django_tables2 as tables

class WeatherDataTable(tables.Table):
    class Meta:
        model = WeatherDataRow

def index(request):
    # We always want to show a form in case a user wants to upload a different file to work with.
    form = UploadedDocumentForm(request.POST, request.FILES)
    is_active_file = False
    if request.method == 'POST':
        if "uploading_file" in request.POST:
            csv_as_list = []
            if form.is_valid():
                document_object = form.save()
            else:
                form = UploadedDocumentForm()
            reader = csv.reader(open(document_object.document.path, 'r'))

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

            table=WeatherDataTable(WeatherDataRow.objects.filter(parent_file_id=document_object.id))

            request.session['document_id']=document_object.id

            is_active_file = True

            data = {
                'is_active_file': is_active_file,
                'table':table,
                'dates':None
            }

            return render(request, 'weather/index.html', {'form': form, 'data': data})
        if "date_picker_submit" in request.POST:
            table=WeatherDataTable(WeatherDataRow.objects.filter(parent_file_id=request.session['document_id'], date__range=[request.POST['start_date'], request.POST['end_date']]))
            is_active_file = True
            print(request.POST['start_date'])
            print(request.POST['end_date'])

            data = {
                'is_active_file': is_active_file,
                'table':table,
                'dates':{'start_date':request.POST['start_date'], 'end_date':request.POST['end_date']}
            }
            return render(request, 'weather/index.html', {'form': form, 'data': data})


    return render(request, 'weather/index.html', {'form': form})
