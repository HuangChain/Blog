#encoding:utf-8
from .models import Blog
from django import forms
from django.forms import widgets

class BlogForm(forms.Form):
    title = forms.CharField(required=True,
                            max_length=10,
                            error_messages={'required': u'标题不能为空'},
                            widget=widgets.TextInput(attrs={'placeholder': u'标题'}),

                            )

    body = forms.CharField(required=True,
                            error_messages={'required': u'内容不能为空'},
                            widget=widgets.Textarea(attrs={'placeholder': u'内容'}),

                            )


class MessageForm(forms.Form):
    message = forms.CharField(required=True,
                            error_messages={'required': u'message不能为空'},
                            widget=widgets.Textarea(attrs={'placeholder': u'message'}),

                            )