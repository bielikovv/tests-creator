from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class':'form-control form-control-sm'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class':'form-control form-control-sm'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm'}))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control form-control-sm'}))

    class Meta:
        model = User
        fields = ['username', 'password']



class CreateQuestionForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), disabled=True, label='', widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))
    test = forms.ModelChoiceField(queryset=Test.objects.all(), disabled=True, label='', widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))
    content = forms.CharField(label='Question', widget=forms.Textarea(attrs={'class': 'form-control form-control-sm'}))
    value = forms.IntegerField(label='Value', widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))

    class Meta:
        model = Question
        fields = ['user', 'test', 'content', 'value']
