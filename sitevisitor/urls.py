from django.conf import settings
from django.conf.urls.static import static

from django.urls import path


from .views import coverpage, site_home, login_view, registration, reset_password, forgot_password, otp, unauthorized_access

urlpatterns = [
   
    path('', coverpage, name='coverpage'),
    path('sitehome/', site_home, name='sitehome'),
    path('signin/', login_view, name='signin'),
    path('signup/', registration, name='registration'),
    path('resetpassword/', reset_password, name='reset_password'),
    path('forgotpassword/', forgot_password, name='forgot_password'),
    path('otp/', otp, name='otp'),
    path('404/',unauthorized_access , name='404'),
    

   
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

   

