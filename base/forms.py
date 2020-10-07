from django.forms import ModelForm,TextInput
from .models import Twitter_Model

class TwitterForm(ModelForm):
    class Meta:
        model = Twitter_Model 
        fields = '__all__'

# from django import forms


# class TwitterForm(forms.Form):
#     name = forms.CharField(max_length=10000)
#     def __str__(self):
#         return self.name