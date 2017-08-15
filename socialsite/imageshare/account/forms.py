# -*- coding:UTF-8 -*-

from django import forms
from django.conf import settings
from django.contrib.auth.models import User

from .models import Profile

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='再一次输入', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('密码不匹配')
        return cd['password2']



class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')

