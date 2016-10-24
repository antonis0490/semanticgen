from django import forms
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


def urlValidator(value):
    validator = URLValidator()
    try:
        validator(value)
    except:
        raise ValidationError("URL is not valid")
    return value

class submitURL(forms.Form):
    CHOICES = (('API', 'API'),('Custom', 'Custom'),)
    apiselector = forms.ChoiceField(label="Select generator",choices=CHOICES, widget=forms.Select(attrs={'class':'form-control'}))
    url = forms.CharField(label="Enter URL here", validators=[urlValidator], widget=forms.TextInput(attrs={'class':'form-control'}))



