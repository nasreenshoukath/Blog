
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static



from .views import user_home, add_blog, blog_list, view_blog, view_profile, edit_blog, delete_blog, edit_profile, reset_password, my_blogs, logout_view, drafted_blogs,delete_comment, edit_comment
   
urlpatterns = [
    path('', user_home, name='userhome'),

    path('addblog/',add_blog, name='addblog'),

    path('bloglist/', blog_list, name='bloglist'),

    path('viewblog/<int:blog_id>/', view_blog, name='viewblog'),

    path('delete/<int:comment_id>/',delete_comment, name='delete_comment'),

    path('edit_comment/<int:comment_id>/',edit_comment, name='edit_comment'),

    path('deleteblog/<int:blog_id>/', delete_blog, name='deleteblog'),

     path('viewprofile/', view_profile, name='viewprofile'),

    path('editblog/<int:blog_id>/', edit_blog, name='editblog'),
    
    path('editprofile/', edit_profile, name='editprofile'),

    path('resetpassword/',reset_password, name='resetpassword'),

    path('logout/',logout_view, name='logout'),
    
    path('draftedblogs/', drafted_blogs, name='draftedblogs'),

    
    path('myblogs/', my_blogs, name='myblogs'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)