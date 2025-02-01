from .models import Note, Comment, Account
from accounts.models import CustomUser
from django.contrib.auth import authenticate

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import PrivateNoteModel


class UserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email']

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
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
        fields = ['name']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
      
        if not self.instance.pk: 
            self.instance.regular_user = True


class AuthenticationForm(forms.Form):
    email = forms.CharField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("email")
        password = cleaned_data.get("password")
        
        if email and password:
            user = authenticate(username=email, password=password)
            if user is None:
                raise forms.ValidationError("Invalid email or password.")
            self.user = user 
        return cleaned_data
    

class PrivateNoteForm(forms.ModelForm):
    class Meta:
        model = PrivateNoteModel
        fields = ['content']
