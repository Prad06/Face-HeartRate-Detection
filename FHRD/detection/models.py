import os
from django.db import models

def photo_path(instance, filename):
    basefilename, file_extension= os.path.splitext(filename)
    return 'images/{string}{ext}'.format(string= 'image', ext= file_extension)

# Create your models here.
class Photo(models.Model):
    title = models.CharField(max_length=20, default='Image')
    img = models.ImageField(upload_to=photo_path)

    def __str__(self):
        return self.title
