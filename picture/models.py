# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Picture(models.Model):
    image=models.ImageField(upload_to='images/%Y/%m',max_length=500)
    created=models.DateTimeField(auto_now_add=True)
