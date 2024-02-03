from django import forms
from .models import Photo,Profile,User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
    )
    class Meta:
        model = User
        fields = ['username','password']

class UserUpdateForm(forms.ModelForm):
    email =forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class UserRegisterForm(UserCreationForm):
    fullname = forms.CharField(max_length=255,help_text='Enter your full name')

    class Meta:
        model = User
        fields = ['fullname', 'username', 'email', 'password1','password2']
    
    def save(self,commit=True):
        user = super().save(commit=False)
        user.fullname = self.cleaned_data['fullname']
        if commit:
            user.save()
        return user



class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['photo_title','image']


