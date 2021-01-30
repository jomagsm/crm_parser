from django import forms
from webapp.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['login',
                  'password']