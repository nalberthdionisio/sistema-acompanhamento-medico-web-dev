from dataclasses import field

from django import forms
from django.forms.widgets import PasswordInput
from django.forms.widgets import NumberInput
from .models import *
from crispy_forms.layout import Layout, Field


class formSug(forms.ModelForm):
    password = None

    class Meta:
        model = Recommendation
        fields = '__all__'
        labels = {
            'name': 'Qual seu nome?',
        }
        widget = {
            'name': forms.TextInput(attrs={'class': 'name-input'}),
            'avatar': forms.FileInput(attrs={'class': 'avatar-input'}),
            'phone': forms.NumberInput(attrs={'class': 'phone-input'}),
            'email': forms.EmailInput(attrs={'class': 'email-input'}),
            'street': forms.TextInput(attrs={'class': 'street-input'}),
            'number': forms.NumberInput(attrs={'class': 'number-input'}),
        }

    # def __init__(self, *args, **kwargs):
    #     super(formSug, self).__init__(*args, **kwargs)
    #     self.fields['name'].required = False
    #     self.fields['avatar'].required = False
    #     self.fields['phone'].required = False
    #     self.fields['email'].required = False
    #     self.fields['street'].required = False
    #     self.fields['number'].required = True
    # procedure = forms.ModelMultipleChoiceField(
    #     queryset=Procedure.objects.all(),
    #     widget=forms.CheckboxSelectMultiple
    # )

    # def __init__(self, *args, **kwargs):
    #     super(formSug, self).__init__(*args, **kwargs)
    #     self.fields['procedure'].required = False


class formcadProc(forms.ModelForm):
    class Meta:
        model = Procedure
        fields = '__all__'
       
    recommendation = forms.ModelMultipleChoiceField(
        queryset=Recommendation.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )


class formUser(forms.ModelForm):
    class Meta:
        model = Users
        # fields = '__all__']

        labels = {

            'username': 'Nome Completo',
        }
        fields = ['username', 'email', 'cpf',
                  'birth_date', 'street', 'number', 'district', 'uf', 'phone', 'procedure', 'association','bariatric' ]

        help_texts = {
            'username': None,
        }
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'pass-input'}),
            'cpf': forms.NumberInput(attrs={'class': 'cpf-input'}),
            'email': forms.EmailInput(attrs={'class': 'mail-input'}),
            'street': forms.TextInput(attrs={'class': 'str-input'}),
            # 'birth_date': forms.DateInput(attrs={'class':'birth-input'}),
            'number': forms.NumberInput(attrs={'class': 'num-input'}),
            'username': forms.TextInput(attrs={'class': 'user-input'}),
            'district': forms.TextInput(attrs={'class': 'dstr-input'}),
            'phone': forms.NumberInput(attrs={'class': 'phon-input'}),
            'uf': forms.Select(attrs={'class': 'uf-input'}),
            # 'procedure': forms.CheckboxSelectMultiple(attrs={'class':'proc-input'}),
        }
    birth_date = forms.DateField(
        label='Data de nascimento',
        widget=NumberInput(attrs={'type': 'date', 'class': 'birth-input'}))
    procedure = forms.ModelMultipleChoiceField(
        label='',
        queryset=Procedure.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'proc-input'})

    )

    def __init__(self, *args, **kwargs):
        super(formUser, self).__init__(*args, **kwargs)
        self.fields['procedure'].required = False


class FormUserProcedure(forms.ModelForm):
    class Meta:
        model = UserProcedure
        fields = '__all__'
        exclude = ['user','procedure']



