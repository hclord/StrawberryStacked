from django.http import HttpResponse
from django.shortcuts import render
from .forms import UploadImageForm
from .models import Images
from .connector import compute_bad_colors
import logging

def homepage(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            for image in Images.objects.all():
                image.delete() # a weird way of ensuring that the number of images is always 0 or 1
            form.save()
            return display_image(request)
    else:
        form = UploadImageForm()
    return render(request, 'index.html', {'form': form})


def display_image(request):
    # getting all the objects of hotel.
    images = Images.objects.all() 
    default_path = "/Users/hlord/Desktop/StrawberryStacked/webapp/mysite"
    bad_colors = compute_bad_colors(default_path + images[0].image.url)
    bad_color_list = []
    for color in bad_colors:
        bad_color_list.append({'color1': color[0]['hex'], 'color2': color[1]['hex'], 'color1b': color[0]['blindHex'], 'color2b': color[1]['blindHex']})
    return render(request, 'final.html',
                    {'images' : images, 'bad_colors': bad_color_list[:4]})