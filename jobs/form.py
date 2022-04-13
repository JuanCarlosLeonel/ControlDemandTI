from django.forms import ModelForm, fields, widgets
from django import forms
from .models import Jobs

class JobForm(forms.ModelForm):
        class Meta:
            model = Jobs
            fields = ['titulo', 'descricao', 'categoria', 'prazo_entrega', 'solicitante']
            widgets = {                         
                'titulo': forms.TextInput(attrs={'class':'form-control'}),
                'descricao': forms.TextInput(attrs={'class':'form-control'}),
                'categoria': forms.Select(attrs={'class':'form-control'}),
                'prazo_entrega': forms.DateInput(attrs={'data-mask':'00/00/0000','class':'form-control datepicker'}),
                'solicitante': forms.TextInput(attrs={'class':'form-control'}),
                }