
from django.shortcuts import redirect, render
from django.contrib.auth import logout

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.contrib.auth import login 

from adminpanel.models import Blog, Comment, Profile, User
from .forms import BlogForm, CommentForm, EditProfileForm, EditRegistrationForm, ResetPassForm


from django.contrib import messages





# Create your views here.
@login_required(login_url='/404/')
def user_home(request):
     profile = get_object_or_404(Profile, user=request.user)
     context = {
        'logged_user': request.user,
        'profile': profile
    }
    
     return render(request, 'userpanel/user_home.html', context)


@login_required(login_url='/404/')
def add_blog(request):
      profile = get_object_or_404(Profile, user=request.user)
    
      if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            if blog.status == Blog.PUBLISHED:
                messages.success(request, 'Blog published successfully.')
            else:
                messages.success(request, 'Blog saved as draft.')
            return redirect('myblogs')
        else:
            print(form.errors)
      else:
        form = BlogForm()
    
      context = {
        'form': form,
        'profile': profile
      }
      return render(request, 'userpanel/add_blog.html', context)
    #   return render(request, 'userpanel/add_blog.html') 
   
@login_required(login_url='/404/')
def blog_list(request):
    #logged_user = request.user
    profile = get_object_or_404(Profile, user=request.user)
    
    # Filter blogs to exclude those from inactive users
    blogs = Blog.objects.filter(author__is_active=True,status=Blog.PUBLISHED)
    
    context = {
        'blogs': blogs,
        'profile': profile
    }
    return render(request, 'userpanel/blog_list.html', context)
  
@login_required(login_url='/404/')
def edit_blog(request,blog_id):
    logged_user = request.user
    profile = get_object_or_404(Profile, user=logged_user)
    
    # Retrieve the existing blog instance
    blog = get_object_or_404(Blog, id=blog_id)
    
    if request.method == "POST":
        blog_form = BlogForm(request.POST, request.FILES, instance=blog)
        if blog_form.is_valid():
            blog_form.save()
            messages.success(request, 'Successfully updated blog')
            return redirect('myblogs')
    else:
        blog_form = BlogForm(instance=blog)
    
    context = {
        'form': blog_form,
        'profile': profile
    }

    return render(request, 'userpanel/edit_blog.html', context)

@login_required(login_url='/404/')
def edit_profile(request):
    logged_user = request.user
    profile = get_object_or_404(Profile,user=logged_user)

    if request.method == 'POST':
        register_form = EditRegistrationForm(request.POST, instance=logged_user)
        profile_form = EditProfileForm(request.POST, request.FILES, instance=profile)

        if register_form.is_valid() and profile_form.is_valid():
            register_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('viewprofile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        register_form = EditRegistrationForm(instance=logged_user)
        profile_form = EditProfileForm(instance=profile)

    return render(request, 'userpanel/edit_profile.html', {
        'form': register_form,
        'form1': profile_form,
        'profile': profile,
        'logged_user': logged_user
    })

@login_required(login_url='/404/')
def view_profile(request, ):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    return render(request, 'userpanel/view_profile.html', {'profile': profile})

@login_required(login_url='/404/')
def my_blogs(request):
   profile = get_object_or_404(Profile, user=request.user)
   blogs = Blog.objects.filter(author=request.user, status=Blog.PUBLISHED)
    
   context = {
        'blogs': blogs,
        'profile': profile,
        'blog_status': 'published',
    }
   return render(request, 'userpanel/my_blogs.html', context)
  
@login_required(login_url='/404/')
def drafted_blogs(request):
    profile = get_object_or_404(Profile, user=request.user)
    blogs = Blog.objects.filter(author=request.user, status=Blog.DRAFT)
    
    context = {
        'blogs': blogs,
        'profile': profile,
        'view_type': 'drafted',
    }
    return render(request, 'userpanel/my_blogs.html', context)

@login_required(login_url='/404/')    
def reset_password(request):
    if request.method == 'POST':
        form = ResetPassForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data.get('old_password')
            new_password = form.cleaned_data.get('new_password')
            confirm_password = form.cleaned_data.get('confirm_password')

            user = request.user
            
            # Check if the old password is correct
            if  not user.check_password(old_password):
                messages.error(request, "Old password is incorrect.")
            elif new_password != confirm_password:
                messages.error(request, "New passwords do not match.")
            else:
                
                user.save()
                # Log the user back in after changing the password
                login(request, user)
                messages.success(request, "Password has been updated Sucessfully .")
                return redirect('userhome')
    else:
        form = ResetPassForm()

    return render(request, 'userpanel/reset_password.html', {'form': form})

@login_required(login_url='/404/')
def view_blog(request,blog_id):
        profile = get_object_or_404(Profile, user=request.user)
        blog = get_object_or_404(Blog, id=blog_id)
        comments = Comment.objects.filter(blog=blog, is_hidden=False)
        comment_count = comments.count()

        if request.method == 'POST':
                form = CommentForm(request.POST)
                if form.is_valid():
                    comment = form.save(commit=False)
                    comment.blog = blog
                    comment.author = request.user
                    comment.save()
                    messages.success(request, 'Your comment has been posted.')
                    return redirect('viewblog', blog_id=blog.id)
        else:
            form = CommentForm()

        return render(request, 'userpanel/view_blog.html', {
            'blog': blog,
            'form': form,
            'comments': comments,
            'comment_count': comment_count,
            'profile': profile
        })

@login_required(login_url='/404/')
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Ensure the logged-in user is the author of the comment
    if comment.author != request.user:
        messages.error(request, "You are not authorized to edit this comment.")
        return redirect('viewblog', blog_id=comment.blog.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Comment has been updated successfully.")
            return redirect('viewblog', blog_id=comment.blog.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'userpanel/edit_comment.html', {'form': form, 'comment': comment})


@login_required(login_url='/404/')
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Ensure the logged-in user is the author of the comment
    if comment.author != request.user:
        messages.error(request, "You are not authorized to delete this comment.")
        return redirect('viewblog', blog_id=comment.blog.id)

    if request.method == 'POST':
        blog_id = comment.blog.id 
        comment.delete()
        messages.success(request, "Comment has been deleted successfully.")
        return redirect('viewblog', blog_id=blog_id)

    return render(request, 'userpanel/view_blog.html', {'comment': comment})

@login_required(login_url='/404/')
def delete_blog(request,blog_id):   
    blog = get_object_or_404(Blog, id = blog_id)
    if request.method == "POST":
       
        blog.delete()
        return redirect('myblogs')
    return render(request,'userpanel/my_blogs.html',{'blog':blog})



@login_required(login_url='/404/')
def logout_view(request):
    logout(request)
    return redirect('coverpage')
