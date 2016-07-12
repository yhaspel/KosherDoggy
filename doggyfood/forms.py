from django import forms

from . import models


class CompareForm(forms.ModelForm):
    class Meta:
        model = models.DogFood
        fields = (
            'compare',
        )
