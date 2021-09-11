from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadImageForm
import logging

def homepage(request):
    return render(request, 'upload.html', {'form': UploadImageForm()})

def upload_file(request):
    if request.method == 'POST':
        logging.debug(request.FILES)
        form = UploadImageForm(request.POST, request.FILES)
        # if form.is_valid():
        handle_uploaded_file(request.FILES['file1'])
        return render(request, 'splash.html')
    else:
        form = UploadImageForm()
    return render(request, 'upload.html', {'form': form})

def handle_uploaded_file(f):
    with open('output.png', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def success(request): 
    return render(request, 'splash.html')