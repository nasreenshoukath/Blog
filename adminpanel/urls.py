
from django.urls import path


from .views import admin_home, admin_login, blog_list,blog_view,adminreset_password,user_list,view_user, active_deactive_user, admin_notification, admin_logout


urlpatterns = [
    path('',admin_login, name='siteadmin'),
    path('adminhome', admin_home, name='adminhome'),
    path('bloglist/', blog_list, name='blog_list'),
    path('blog_view/<int:blog_id>/', blog_view, name='blogview'),
    path('adresetpassword/', adminreset_password, name='adresetpassword'),
    path('userlist/', user_list, name='userlist'),
    path('Active_deactive_user/<int:user_id>/', active_deactive_user, name='Active_deactive_user'),
    path('view_user/<int:user_id>/', view_user, name='view_user'),
    path('adminnotification',admin_notification, name='adminnotification'),
    path('adminlogout',admin_logout, name='adminlogout'),
    

   
]
