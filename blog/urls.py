from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^home/', views.home,name='home'),
    url(r'^articles/$', views.articles,name='articles'),
    url(r'^article_detail/(?P<id>\d+)$', views.detail,name='detail'),
    url(r'^publish/$', views.publish,name='publish'),
    url(r'^messages/', views.messages,name='messages'),
    url(r'^article-likes/(?P<ids>\d+)/$', views.likes,name='article_likes'),
    url(r'^edit/(?P<ids>\d+)/$', views.edit_article,name='edit'),
    url(r'^delete_article/(?P<ids>\d+)/$', views.delete_article,name='delete_article'),
]