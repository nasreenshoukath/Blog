import random
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

def send_success_email(firstname,lastname, email):
    context = {
        'firstname': firstname,
        'lastname': lastname,
        'email': email,
       
        
    }

    email_subject = 'Thank you for the Registration'
    email_body = render_to_string('sitevisitor/succes_reg.html', context)

    my_email = EmailMessage(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL, [email, 'nasrimoluty@gmail.com'],
    )
    my_email.content_subtype = 'html'  # Ensure the email is sent as HTML
    return my_email.send(fail_silently=False)

def send_otp_email(email, otp):
    # Use the provided otp instead of generating it again
    # Context with the OTP
    context = {
        'otp': otp,
    }

    # Define email subject and body using the template
    email_subject = 'Your Blogster OTP Code'
    email_body = render_to_string('sitevisitor/send_otp.html', context)

    # Create and send the email
    my_email = EmailMessage(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL, [email],
    )
   
    my_email.content_subtype = 'html'  # Set the content type to HTML

    # Send the email
    my_email.send(fail_silently=False) 
   