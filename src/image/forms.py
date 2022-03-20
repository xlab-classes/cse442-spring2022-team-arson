from calendar import c
from django import forms
from .models import *

class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadImage
        fields = '__all__'