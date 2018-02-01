# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic.base import View
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# Create your views here.

from manager.forms import LoginForm
from blog.models import Message

# def user_login(request):
#     if request.method=="GET":
#         login_form = LoginForm()
#         return render(request, 'login.html', {'login_form': login_form})


class LoginView(View):

    def get(self,request):
        login_form=LoginForm()
        return render(request,'login.html',{'login_form':login_form})

    def post(self,request):
        login_form=LoginForm(request.POST)
        if login_form.is_valid():
            user_name = login_form.cleaned_data['username']
            pass_word = login_form.cleaned_data["password"]
            user = authenticate(username=user_name, password=pass_word)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return render(request, "login.html",{'msg':u'用户名或密码错误','login_form':login_form})
        else:
            return render(request,'login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


class VerifyView(View):
    def get(self,request):
        messages = Message.objects.filter(status=2)
        return render(request, 'verify.html', {'messages': messages})

    def post(self, request):
        id = request.POST.get('id')
        status = request.POST.get('status')
        message=Message.objects.get(id=id)
        if status == "1":
            message.status = status
            message.save()
            return HttpResponse('1')
        elif status == "3":
            message.status = status
            message.save()
            return HttpResponse('1')
        return HttpResponse('2')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(VerifyView, self).dispatch(*args, **kwargs)




# @csrf_exempt
# def verify(request,id):
#     if request.method=="POST":
#         message = Message.objects.get(id=id)
#         status = request.POST.get('status')
#         if status == "1":
#             message.status = status
#
#         elif status == "3":
#             message.status = status
#             message.save()
#         messages = Message.objects.filter(status=2)
#         return render(request, 'verify.html', {'messages': messages})



# class VerifyView(View):
#     def post(self, request,id):
#         message = Message.objects.get(id=id)
#         status = request.POST.get('status')
#         if status == "1":
#             message.status = status
#
#         elif status == "3":
#             message.status = status
#             message.save()
#         messages = Message.objects.filter(status=2)
#         return render(request, 'verify.html', {'messages': messages})
#
#     @csrf_exempt
#     def dispatch(self, *args, **kwargs):
#         return super(VerifyView, self).dispatch(*args, **kwargs)
#
