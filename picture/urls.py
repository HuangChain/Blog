from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^', views.PictureListView.as_view(), name='pictures'),

]
