from django import forms
from django.utils.translation import gettext as _

from .models import Status


class StatusCreationForm(forms.ModelForm):
    name = forms.CharField(label=_('Name'))

    class Meta():
        model = Status
        fields = ['name']
