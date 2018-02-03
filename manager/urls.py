from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt


from . import views

urlpatterns = [
    url(r'^login/', views.LoginView.as_view(), name="login"),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^verify/', csrf_exempt(views.VerifyView.as_view()), name="verify"),
]
