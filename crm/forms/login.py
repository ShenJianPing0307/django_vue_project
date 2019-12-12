from django import forms
from django.forms import widgets
from crm import models


class LoginForm(forms.Form):
    username = forms.CharField(min_length=6, max_length=12, required=True,
                                error_messages={
                                    'required': '用户不能为空',
                                    'min_length': '输入的太短了',
                                    'max_length': '太长了',
                                },
                                )
    password = forms.CharField(max_length=6, required=True)


