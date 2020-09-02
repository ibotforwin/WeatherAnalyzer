from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import UploadedDocumentForm
import csv
import os

def index(request):
    # We always want to show a form in case a user wants to upload a different file to work with.
    form = UploadedDocumentForm(request.POST, request.FILES)
    is_active_file=False
    if request.method=='POST' and "uploading_file" in request.POST:
        csv_as_list=[]
        if form.is_valid():
            document_object = form.save()
        else:
            form = UploadedDocumentForm()
        reader = csv.reader(open(document_object.document.path,'r'))

        #TODO Check if excel file is valid, maybe check column titles, value existence, and file extension. Return meaningful error to user in the form of a message.

        #Iterating through reader and appending relevant data to a list
        for i, row in enumerate(reader):
            if i>0:
                csv_as_list.append([row[4], row[11], row[9], row[13], row[15], row[19], row[21], row[29]])

        print(csv_as_list)
        is_active_file=True

        data={
            'form': form,
            'is_active_file':is_active_file,
            'csv_as_list':csv_as_list
        }

        return render(request, 'weather/index.html', {'form': form, 'data':data})
    return render(request, 'weather/index.html', {'form': form})



