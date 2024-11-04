from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from adminpanel.models import Profile
from .forms import RegistrationForm,LoginForm, ProfileForm, OTPForm




# Create your views here.


def coverpage(request):
    return render(request, 'sitevisitor/coverpage.html')

def registration(request):
    if request.method =='POST':
        form = RegistrationForm(request.POST)
        form1 = ProfileForm(request.POST,request.FILES)
        if form.is_valid() and form1.is_valid():
            user = form.save()
            form.send_email()

            profile = form1.save(commit = False)
            profile.user = user
            profile.save()
            # profile.send_email()
            messages.success(request,'You have registered successfully please check your email to confirm!!')
            return redirect('signin')
    else:
        form = RegistrationForm()
    form1 = ProfileForm()
    return render(request,'sitevisitor/registration.html',{'form':form,'form1':form1})
  
    # return render(request, 'sitevisitor/registration.html')
    
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)                   
                return redirect('sitehome')    
            else:                
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    
    return render(request, 'sitevisitor/login.html', {'form': form})

  

    
@login_required(login_url='/404/')
def site_home(request):
     profile = get_object_or_404(Profile, user=request.user)
     context = {
        'logged_user': request.user,
        'profile': profile
    }
     return render(request, 'sitevisitor/site_home.html', context)

def otp(request):
        
       
        return render(request, 'sitevisitor/otp.html')
   


   

def reset_password(request):
    return render(request, 'sitevisitor/reset_password.html')

def forgot_password(request):
   
   if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            # Send the OTP via email
            form.send_email()

            # Get the email from the form's cleaned data
            email = form.cleaned_data.get('email')

            # Pass the email to the template context
            context = {
                'email': email
            }

            messages.success(request,'Otp send to your email!!')
            return redirect('otp')
   else:
        form = OTPForm()

    # Render the form in 'otp.html' if the request is GET or if the form is invalid
   return render(request, 'sitevisitor/forgot_password.html', {'form': form})



def unauthorized_access(request):
    return render(request, 'sitevisitor/404.html')