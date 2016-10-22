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
    url = forms.CharField(label="Enter URL here", validators=[urlValidator])



