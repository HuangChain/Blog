#encoding:utf-8
from django import forms
from django.forms import widgets

class LoginForm(forms.Form):

    username=forms.CharField(required=True,
                             max_length=10,
                             widget=widgets.TextInput(attrs={'placeholder':u'用户名'}),
                             )

    password = forms.CharField(required=True,
                               widget=widgets.PasswordInput(attrs={'placeholder': u'密码'}),
                               )