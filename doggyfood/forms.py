from django import forms

from . import models


class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = (
            'title',
            'content',
        )


class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    content = forms.CharField(
        required=True,
        widget=forms.Textarea
    )
