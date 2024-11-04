from django import forms
from adminpanel.models import Blog, Comment, Profile, User
from django.contrib.auth.forms import SetPasswordForm


class EditRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True, label='First Name',
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, required=True, label='Last Name',
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}))
    email = forms.EmailField(max_length=50, required=True, label='Email',
                             widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))
    username = forms.CharField(max_length=50, required=True, label='Username',
                               widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control','readonly':'readonly'}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']
class EditProfileForm(forms.ModelForm):
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

class CommentForm(forms.ModelForm):
        comment = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Enter your comment'}),
        label="Comment"
    )
    
        class Meta:
            model = Comment
            fields = ['comment']

class BlogForm(forms.ModelForm):
    title = forms.CharField(
        label='Title',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'})
    )
    content = forms.CharField(
        label='Description',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Enter content'})
    )
    blog_image = forms.ImageField(
        label='Upload Image',
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )
    status_choices = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    
    status = forms.ChoiceField(
        label='Status',
        choices=status_choices,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = Blog
        fields = ['title', 'content', 'blog_image', 'status']
    
class ResetPassForm(SetPasswordForm):
    old_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old Password'})
    )
    new_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'})
    )
    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        # Ensure new passwords match
        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("New passwords do not match.")

        return cleaned_data