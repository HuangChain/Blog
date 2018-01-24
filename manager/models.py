# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings

# Create your models here.
class UserInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    birthday = models.DateField(default='1995-11-26')
    position = models.CharField(max_length=50)
    hobby = models.CharField(max_length=50)
    address = models.CharField(max_length=10)

    def __unicode__(self):
        return self.user.username
