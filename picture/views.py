# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from .models import Picture
from .forms import PictureForm


# Create your views here.

def pictures(request):
    if request.method=="GET":
        pictures=Picture.objects.all()
        return render(request,'pictures.html',{'pictures':pictures})
    else:
        picture_form = PictureForm(request.POST,request.FILES)
        pictures = Picture.objects.all()
        if  picture_form.is_valid():
            picture_form.save()
            return render(request,'pictures.html',{'pictures':pictures,'msg':u'上传成功'})
        else:
            return render(request,'pictures.html',{'pictures':pictures,'msg':u'请选择图片'})
        return render(request, 'pictures.html', {'pictures':pictures})
