from .models import Note, Comment, Account
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from django import forms
from django.forms import ModelForm


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    

class AccountForm(ModelForm):
    class Meta: 
        model = Account
        fields = ['name', 'regular_user']

        labels = {
            "regular_user": "Do you want to be a regular user?",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
      
        if not self.instance.pk: 
            self.instance.regular_user = True


class AuthenticationForm(forms.Form):
    username = forms.CharField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid username or password.")
            self.user = user 
        return cleaned_data