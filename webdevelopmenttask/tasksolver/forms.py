from django import forms
from .models import Task
from django.core.files.base import ContentFile
from django.utils.text import slugify
import requests


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['number']

    def clean_number(self):
        number = self.cleaned_data.get('number')
        if number > 1000000000:
            raise forms.ValidationError('The number is too large. Please choose a smaller one.')
        elif number < 1:
            raise forms.ValidationError('The number is too small. Please choose a larger one.')
        return number

    def save(self, force_insert=False, force_update=False, commit=True):
        image = super().save(commit=False)

        if commit:
            image.save()
        return image







# class ImageCreateForm(forms.ModelForm):
#     class Meta:
#         model = Image
#         fields = ['image']
#
#     def clean_image(self):
#         image = self.cleaned_data.get('image')
#         if image:
#             max_size = 2 * 1024 * 1024
#             if image.size > max_size:
#                 raise forms.ValidationError('The image size is too large. Please choose a smaller image.')
#         return image
#
#     def save(self, force_insert=False, force_update=False, commit=True):
#         image = super().save(commit=False)
#         if commit:
#             image.save()
#         return image


# class ProcessParametersForm(forms.ModelForm):
#     class Meta:
#         model = ProcessParameters
#         fields = ['saturation', 'brightness', 'blur']
