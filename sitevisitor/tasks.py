import random
from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings

from .email import send_otp_email, send_success_email
logger = get_task_logger(__name__)

@shared_task(name="send_success_email_task", bind=True)
def send_success_email_task(self, firstname, lastname ,email):
    logger.info("Sent Registration success email")
    return send_success_email(firstname=firstname,lastname=lastname, email=email)


@shared_task(name="send_otp_generation", bind=True)
def send_otp_generation(self,email):
    otp = random.randint(100000, 999999)  # Generate a 6-digit OTP
    logger.info("Sent OTP to your email")
    send_otp_email(email=email, otp=otp)
    return otp