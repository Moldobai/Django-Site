from django import  forms
from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import CaptchaField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from .models import *


class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label  = 'Выберите!'
    class Meta:
        model = Women
        fields =  ['title', 'slug','content', 'photo' , 'is_published','cat']
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'slug':forms.TextInput(attrs={'class':'form-control'}),
            'content':forms.Textarea(attrs={'class':'form-control', 'cols':60, 'rows':8}),
            'photo':forms.ClearableFileInput(attrs={'class':'form-control-file'}),
            'cat':forms.Select(attrs={'class':'custom-select my-1 mr-sm-2'}),
        }


    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 150:
            raise ValidationError('Длина больше 150 символов')

        return title

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ('username', 'email','password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class':'form-control'}))



class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class':"form-control"}))
    content =forms.CharField(label='Кантент',widget=forms.Textarea(attrs={'cols':40, 'rows':7,'class':'form-control'}))
    capatcha = CaptchaField(label='Are you an human? ')