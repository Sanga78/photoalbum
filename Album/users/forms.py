import re
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile,User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
    )

class UserUpdateForm(forms.ModelForm):
    email =forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'password']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
    )
    
    password_confirm = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
    )

    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Register'))

    def clean_password(self):
        password = self.cleaned_data.get('password')

        # Check if the password contains at least 8 characters
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters.")

        # Check if the password is a mixture of characters
        if not re.match(r'^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$', password):
            raise forms.ValidationError("Password must contain at least one letter, one number, and one special character.")

        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data