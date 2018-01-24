# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.conf import settings
from django.http import JsonResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
import redis
from django.views.decorators.http import require_POST

from .models import Blog,Message
from manager.models import UserInfo

from blog.forms import BlogForm,MessageForm

# Create your views here.
def home(request):
    blogs=Blog.objects.all()[:3]
    userinfo=UserInfo.objects.get(user_id=1)
    return render(request,'home.html',{
        'blogs':blogs,
        'userinfo':userinfo
    })


def articles(request):
    articles = Blog.objects.all()
    total_articles=articles.count()
    paginator = Paginator(articles, 5)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    articles=Blog.objects.all().order_by("-likes")[:5]
    return render(request, 'articles.html', {
        'contacts': contacts,
        'articles':articles,
        'total_articles':total_articles
    })

def detail(request,id):
    article=Blog.objects.get(id=id)
    likes=range(article.likes)
    r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
    total_views = r.incr("article:{}:views".format(article.id))
    return render(request,'detail.html',{'article':article,'likes':likes,'total_views':total_views})


@csrf_exempt
def publish(request):
    if request.method=="GET":
        article_form = BlogForm()
        return render(request, 'publish.html',{'article_form':article_form})
    else:
        article_form=BlogForm(request.POST)
        if article_form.is_valid():
            cd=article_form.cleaned_data
            Blog.objects.create(title=cd['title'],body=cd['body'])
            return HttpResponse('1')
        else:
            return JsonResponse(article_form.errors)
        return JsonResponse(article_form.errors)


@require_POST
@csrf_exempt
def likes(request,ids):
    article=Blog.objects.get(id=ids)
    article.likes+=1
    article.save()
    # likes = range(article.likes)
    return HttpResponse('1')

@csrf_exempt
def messages(request):
    if request.method=='GET':
        message_form = MessageForm()
        messages=Message.objects.filter(status=1).order_by("-created")
        return render(request, 'messages.html', {'messages':messages,'message_form':message_form})
    else:
        message_form=MessageForm(request.POST)
        if message_form.is_valid():
            cd=message_form.cleaned_data
            Message.objects.create(message=cd['message'])
            return HttpResponse('1')
        else:
            return JsonResponse(message_form.errors)
        return JsonResponse(message_form.errors)

@csrf_exempt
def edit_article(request,ids):
    if request.method == "GET":
        article=Blog.objects.get(id=ids)
        article_form = BlogForm(initial={'title':article.title,'body':article.body})
        return render(request, 'edit.html', {'article_form': article_form,'article':article})
    else:
        article_form = BlogForm(request.POST)
        if article_form.is_valid():
            cd = article_form.cleaned_data
            Blog.objects.filter(id=ids).update(title=cd['title'], body=cd['body'])
            return HttpResponse('1')
        else:
            return JsonResponse(article_form.errors)
        return JsonResponse(article_form.errors)

@require_POST
@csrf_exempt
def delete_article(request,ids):
    Blog.objects.get(id=ids).delete()
    return HttpResponse('1')
