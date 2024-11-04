
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

def send_activate_email(username,email):
    context = {
        'username': username,
        'email': email,
       
        
    }

    email_subject = 'Admin Activated Your Account'
    email_body = render_to_string('adminpanel/activate_user.html', context)

    my_email = EmailMessage(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL, [email, 'nasrimoluty@gmail.com'],
    )
    my_email.content_subtype = 'html'  # Ensure the email is sent as HTML
    return my_email.send(fail_silently=False)

def send_deactivate_email(username,email):
    context = {
        'username': username,
        'email': email,
       
        
    }

    email_subject = 'Admin DeActivated Your Account'
    email_body = render_to_string('adminpanel/deactivate_user.html', context)

    my_email = EmailMessage(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL, [email, 'nasrimoluty@gmail.com'],
    )
    my_email.content_subtype = 'html'  # Ensure the email is sent as HTML
    return my_email.send(fail_silently=False)


