#encoding:utf-8
from blog.models import Blog,Message
from django import forms
from django.forms import widgets

class BlogForm(forms.ModelForm):
    class Meta:
        model=Blog
        fields = ['title','body']
        widgets = {
            'title':widgets.TextInput(attrs={'placeholder': u'标题'}),
            'body':widgets.Textarea(attrs={'placeholder': u'内容'}),
        }
        error_messages = {
            'title':{'required': u'标题不能为空'},
            'body': {'required': u'内容不能为空'},
        }

# class BlogForm(forms.Form):
#     title = forms.CharField(required=True,
#                             max_length=10,
#                             error_messages={'required': u'标题不能为空'},
#                             widget=widgets.TextInput(attrs={'placeholder': u'标题'}),
#
#                             )
#
#     body = forms.CharField(required=True,
#                             error_messages={'required': u'内容不能为空'},
#                             widget=widgets.Textarea(attrs={'placeholder': u'内容'}),
#
#                             )


# class MessageForm(forms.Form):
#     message = forms.CharField(required=True,
#                             error_messages={'required': u'message不能为空'},
#                             widget=widgets.Textarea(attrs={'placeholder': u'message'}),
#
#                             )

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        widgets = {
            'message':widgets.Textarea(attrs={'placeholder': u'message'}),
        }
        error_messages = {
            'message': {'required': u'message不能为空'},
        }