from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from django.views import View
from .forms import AdminLoginForm, AdminResetPassForm


from .models import Blog, Comment, User, Profile
from django.contrib import messages
from .tasks import send_activate_email_task, send_deactivate_email_task
# from django.contrib.auth.models import User

# Create your views here.


@login_required(login_url='/404/')
def admin_home(request):
    return render(request, 'adminpanel/admin_home.html')

def admin_login(request):
     if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                 if user.is_staff:
                   login(request, user)                   
                 return redirect('adminhome')    
            else:                
                messages.error(request, 'Invalid username or password')
     else:
        form = AdminLoginForm()
    
     return render(request, 'adminpanel/admin_login.html', {'form': form})
  

@login_required(login_url='/404/')
def blog_list(request):
      blogs = Blog.objects.filter(author__is_active=True,status=Blog.PUBLISHED)
      return render(request, 'adminpanel/blog_list.html', {'blogs': blogs})

@login_required(login_url='/404/')   
def blog_view(request,blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.user.is_staff:
        comments = Comment.objects.filter(blog=blog)  # Admin sees all comments
   
    comment_count = comments.count()

    if request.method == 'POST':
        if 'hide_comment' in request.POST:
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(Comment, id=comment_id)
            if comment.blog == blog:
                comment.is_hidden = True
                comment.save()
                messages.success(request, 'Comment has been hidden.')
        elif 'show_comment' in request.POST:
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(Comment, id=comment_id)
            if comment.blog == blog:
                comment.is_hidden = False
                comment.save()
                messages.success(request, 'Comment is now visible.')
        

    return render(request, 'adminpanel/blog_view.html', {
        'blog': blog,
        
        'comments': comments,
        'comment_count': comment_count,
    })


@login_required(login_url='/404/')
def user_list(request):
    
    users = User.objects.filter(is_staff=False)
    user_data = []

    for user in users:
        # Count the blogs for the user
        blog_count = Blog.objects.filter(author=user).count()
        
        # Step 1: Check if the user has a profile
        profile_image = None  # Default to None in case no profile exists
        if hasattr(user, 'profile'):
            profile = user.profile

            # Step 2: Check if the profile has a profile image
            if profile.profile_image:
                profile_image = profile.profile_image.url

        # Append user data
        user_data.append({
            'user_id': user.id,
            'username': user.username,
            'profile_image': profile_image,
            'blog_count': blog_count,
            'is_active': user.is_active,
        })

    return render(request, 'adminpanel/user_list.html', {'user_data': user_data})
    # return render(request, 'adminpanel/user_list.html')

@login_required(login_url='/404/')
def active_deactive_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=user_id)
        user.is_active = not user.is_active
        user.save()

        # Trigger the appropriate email task
        if user.is_active:
            send_activate_email_task.delay(user.username, user.email)
        else:
            send_deactivate_email_task.delay(user.username, user.email)

        # Return a response (redirect or render a template)
        return redirect('userlist') 
       
    

@login_required(login_url='/404/')
def view_user(request,user_id):
    user = get_object_or_404(User, id=user_id)
    # Assuming the Blog model has a ForeignKey to User
    blogs = Blog.objects.filter(author=user)  
    return render(request, 'adminpanel/view_user.html', {'user': user, 'blogs': blogs})
    # return render(request, 'adminpanel/view_user.html')


@login_required(login_url='/404/')
def admin_notification(request):
      blog = Blog.objects.filter(author__is_active=True,status=Blog.PUBLISHED)
      return render(request, 'adminpanel/notification.html', {'blog': blog})
    

def adminreset_password(request):
    if request.method == 'POST':
        form = AdminResetPassForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data.get('old_password')
            new_password = form.cleaned_data.get('new_password')
            confirm_password = form.cleaned_data.get('confirm_password')

            user = request.user
            
            # Check if the old password is correct
            if not user.check_password(old_password):
                messages.error(request, "Old password is incorrect.")
            elif new_password != confirm_password:
                messages.error(request, "New passwords do not match.")
            else:
               
                user.save()
                # Log the user back in after changing the password
                login(request, user)
                messages.success(request, "Password has been updated Sucessfully .")
                return redirect('adminhome')
    else:
        form = AdminResetPassForm()

    return render(request, 'adminpanel/adreset_password.html', {'form': form})
    
@login_required(login_url='/404/')
def admin_logout(request):
    logout(request)
    return redirect('siteadmin')
