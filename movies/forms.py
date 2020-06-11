from django import forms

from .models import *


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Reviews
        fields = ["name", "email", "text"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control border"}),
            "email": forms.EmailInput(attrs={"class": "form-control border"}),
            "text": forms.Textarea(attrs={"class": "form-control border",
                                          "id": "contactcomment"}),
        }


class RatingForm(forms.ModelForm):
    star = forms.ModelChoiceField(
        queryset = RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating
        fields = ['star', ]
