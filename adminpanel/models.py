from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    id_proof = models.ImageField(upload_to='id_proofs/', blank=True, null=True)
    about_description = models.TextField(default='Your default description here')
    def __str__(self):
        return self.user.username
    
      
class Blog(models.Model):
        DRAFT = 'draft'
        PUBLISHED = 'published'
        STATUS_CHOICES = [
            ('draft', 'Draft'),
            ('published', 'Published'),
            
        ]
        title = models.CharField(max_length=200)
        content = models.TextField()
        blog_image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
        author = models.ForeignKey(User, on_delete=models.CASCADE)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        status = models.CharField(max_length=200,choices=STATUS_CHOICES, default=DRAFT)

        def __str__(self):
            return self.title

class Comment(models.Model):
    comment = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=200)
    is_hidden = models.BooleanField(default=False)
    

    def __str__(self):
        return self.comment

