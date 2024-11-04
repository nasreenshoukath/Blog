from django import forms


class AdminLoginForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        label="Username",
        widget=forms.TextInput(attrs={'class': 'form-control','style': 'width: 350px; height: 40px;','placeholder': 'Username'})
        
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control','style': 'width: 350px; height: 40px;','placeholder': 'Password'}),
        label="Password"
    )

class AdminResetPassForm(forms.Form):
        old_password = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'old Password'}),
        
    )
        new_password = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'New Password'}),
        
    )
        confirm_password = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Confirm Password'}),
       
    )