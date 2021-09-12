from django.db import models
from .connector import create_colorblind_image
from io import BytesIO
from django.core.files import File
from PIL import Image
import logging

class Images(models.Model):
    height = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    image = models.ImageField(upload_to='images/', height_field='height', width_field='width', blank=False, null=False)
    sim_image = models.ImageField(upload_to='images/', default='/Users/hlord/Desktop/StrawberryStacked/webapp/mysite/media/default.jpg')
    def save(self, *args, **kwargs):
        self.sim_image = make_thumbnail(self.image)
        super().save(*args, **kwargs)
    
def make_thumbnail(image, size=(100, 100)):
    """Makes thumbnails of given size from given image"""
    logging.debug(image)

    im = create_colorblind_image(image)

    thumb_io = BytesIO() # create a BytesIO object

    im.save(thumb_io, 'PNG', quality=85) # save image to BytesIO object

    thumbnail = File(thumb_io, name=image.name) # create a django friendly File object

    return thumbnail



