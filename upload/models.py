from django.db import models
from django.core.exceptions import ValidationError, PermissionDenied
from django.core.files import File
import os
import urllib
from urllib.request import urlretrieve
# from PIL import Image
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


class Image(models.Model):
    id = models.IntegerField(primary_key=True)
    image = models.ImageField(upload_to='images', blank=True, verbose_name='Файл')

    def __str__(self):
        return str(self.id)



