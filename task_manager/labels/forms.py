from django import forms
from django.utils.translation import gettext as _

from .models import Label


class LabelCreationForm(forms.ModelForm):
    name = forms.CharField(label=_('Label'))

    class Meta:
        model = Label
        fields = ['name']
