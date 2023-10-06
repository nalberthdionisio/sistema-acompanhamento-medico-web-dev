from django import forms
from django.contrib.auth import forms
from django.forms import ChoiceField, Form, MultipleChoiceField

from .models import Procedure, Recommendation, Users


class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = Users


class UserCreationForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = Users
