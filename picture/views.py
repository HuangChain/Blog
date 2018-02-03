# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import ListView

from picture.models import Picture
from picture.forms import PictureForm

# Create your views here.


class PictureListView(ListView):
    template_name = 'pictures.html'
    context_object_name = 'pictures'
    model = Picture

    def post(self, request):
        picture_form = PictureForm(request.POST, request.FILES)
        pictures = Picture.objects.all()
        if picture_form.is_valid():
            picture_form.save()
            return render(request, 'pictures.html', {
                'pictures': pictures,
                'msg': u'上传成功'
            })
        else:
            return render(request, 'pictures.html', {
                'pictures': pictures,
                'msg': u'请选择图片'
            })
        return render(request, 'pictures.html', {'pictures': pictures})


