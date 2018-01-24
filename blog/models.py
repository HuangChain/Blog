# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Blog(models.Model):
    title=models.CharField(max_length=15,blank=False)
    body=models.TextField(blank=False)
    publish=models.DateTimeField(auto_now_add=True)
    likes=models.IntegerField(default=0)

    class Meta:
        ordering=('-publish',)

    def __unicode__(self):
        return self.title

class Message(models.Model):
    status_choice = (
        ('1', u"通过"),
        ('2', u"未查看"),
        ('3', u"不通过")
    )
    message = models.CharField(max_length=300,blank=False)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=status_choice, max_length=10,default=2)

    class Meta:
        ordering=('-created',)

