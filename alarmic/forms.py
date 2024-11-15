from django import forms
from .models import Alarm

class AlarmForm(forms.ModelForm):
    class Meta:
        model = Alarm
        fields = ['time', 'description', 'sound', 'is_active']
        widgets = {
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.TextInput(attrs={'class': 'form-input'}),
            'sound': forms.Select(attrs={'class': 'form-select'}),
        }
