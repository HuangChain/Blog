# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from django.views.generic import View, ListView, DeleteView, DetailView, UpdateView, CreateView
from django.contrib.auth.decorators import login_required
import redis

from manager.models import UserInfo
from blog.models import Blog, Message
from blog.forms import BlogForm, MessageForm

# Create your views here.


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class CsrfExemptMixin(object):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CsrfExemptMixin, self).dispatch(*args, **kwargs)


class HomeView(ListView):
    template_name = 'home.html'
    context_object_name = 'recent_articles'
    model = Blog
    queryset = Blog.objects.all().order_by('-publish')[:3]

    def get_context_data(self, **kwargs):
        kwargs['userinfo'] = UserInfo.objects.get(id=1)
        return super(HomeView, self).get_context_data(**kwargs)


class ArticleView(ListView):
    template_name = 'articles.html'
    context_object_name = 'articles'
    model = Blog
    paginate_by = 5

    def get_context_data(self, **kwargs):
        kwargs['hot_articles'] = self.model.objects.all().order_by("-likes")[:5]
        kwargs['total_articles'] = self.model.objects.all().count()
        return super(ArticleView, self).get_context_data(**kwargs)


class DetailView(DetailView):
    template_name = 'detail.html'
    context_object_name = 'article'
    model = Blog

    def get_context_data(self, **kwargs):
        article = self.model.objects.get(id=self.object.pk)
        kwargs['likes'] = range(article.likes)
        r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
        kwargs['total_views'] = r.incr("article:{}:views".format(self.object.id))
        return super(DetailView, self).get_context_data(**kwargs)


class PublishView(CsrfExemptMixin, CreateView):
    template_name = 'publish.html'
    context_object_name = 'article'
    model = Blog
    form_class = BlogForm

    def form_valid(self, form):
        form.save()
        return JsonResponse({'state': 1})

    def form_invalid(self, form):
        error = form.errors
        return JsonResponse(error)


class LikeView(CsrfExemptMixin, View):
    def post(self, request, ids):
        article = Blog.objects.get(id=ids)
        article.likes += 1
        article.save()
        return HttpResponse('1')


class MessageView(CsrfExemptMixin, CreateView):
    template_name = 'messages.html'
    context_object_name = 'messages'
    model = Message
    form_class = MessageForm

    def get_context_data(self, **kwargs):
        kwargs['messages'] = self.model.objects.filter(status=1).order_by("-created")
        return super(MessageView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        form.save()
        return JsonResponse({'state': 1})

    def form_invalid(self, form):
        error = form.errors
        return JsonResponse(error)


class EditArticleView(CsrfExemptMixin, UpdateView):
    template_name = 'edit.html'
    context_object_name = 'article'
    model = Blog
    form_class = BlogForm

    def form_valid(self, form):
        form.save()
        return JsonResponse({'state': 1})

    def form_invalid(self, form):
        error = form.errors
        return JsonResponse(error)


class DeleteArticleView(CsrfExemptMixin, DeleteView):
    template_name = 'detail.html'
    model = Blog

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'state': 1})
