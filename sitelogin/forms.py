from django import forms
from attandance.models import SiteEngineer
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class SiteUserModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name'
        )
    name = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField() 