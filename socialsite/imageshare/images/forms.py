# -*- coding:UTF-8 -*-

from urllib2 import urlopen
from django.core.files.base import ContentFile
from django.utils.text import slugify
from django import forms

from .models import Image

class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description',)
        widgets = {
            'url': forms.HiddenInput,  #我可以通过别的方式提供
        }

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg']
        extension = url.rsplit('.',1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('给定的url不能匹配有效的文件名扩展')
        return url

    # 覆盖form本身的方法,提供文件下载功能
    def save(self, force_insert=False, force_update=False, commit=True):
        image = super(ImageCreateForm, self).save(commit=False)  
        image_url = self.cleaned_data['url']
        image_name = '{}.{}'.format(slugify(image.title),
                                    image_url.rsplit('.',1)[1].lower())
        response = urlopen(image_url)
        image.image.save(image_name, ContentFile(response.read()), save=False)
        if commit:
            image.save()
        return image
