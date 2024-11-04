from django import forms
from adminpanel.models import Profile, User
from django.contrib.auth.forms import UserCreationForm,SetPasswordForm
import re

from sitevisitor.tasks import send_otp_generation, send_success_email_task
class RegistrationForm(UserCreationForm):
    firstname = forms.CharField(max_length=50, required=True, label='First Name',
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}))
    lastname = forms.CharField(max_length=50, required=True, label='Last Name',
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}))
    email = forms.EmailField(max_length=50, required=True, label='Email',
                             widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))
    username = forms.CharField(max_length=50, required=True, label='Username',
                               widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
    password1 = forms.CharField(max_length=50, required=True, label='Password',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))
    password2 = forms.CharField(max_length=50, required=True, label='Confirm Password',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'email', 'username', 'password1', 'password2']
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            self.add_error('password1', 'Password should have at least 8 characters')
        if not re.search(r'[a-z]', password):
            self.add_error('password1', 'Password should have at least 1 lowercase letter')
        if not re.search(r'[0-9]', password):
            self.add_error('password1', 'Password should have at least 1 number')
        return password
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords do not match.")
        return cleaned_data
    
    def send_email(self):
     send_success_email_task.delay(
        email=self.cleaned_data['email'],
        firstname=self.cleaned_data['firstname'],  # Make sure this is included
        lastname=self.cleaned_data['lastname']     # Include lastname too
    )
class ProfileForm(forms.ModelForm):
    phone = forms.CharField(
        max_length=13,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Phone"
    )
    about_description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Describe yourself'
        }),
        label="About"
    )
    profile_image = forms.ImageField(
        label="Profile Picture",
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control'
        })
    )
    id_proof = forms.ImageField(
        label="ID Proof",
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control'
        })
    )
    class Meta:
        model = Profile
        exclude = ['user']

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        label="Username",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Password"
    )


class OTPForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'style': 'width: 350px; height: 40px;'
    }))
    def send_email(self):
        send_otp_generation.delay(
        email=self.cleaned_data['email'],
     )
       

