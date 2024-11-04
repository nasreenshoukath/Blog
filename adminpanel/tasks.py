from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings

from .email import send_activate_email,send_deactivate_email
logger = get_task_logger(__name__)

@shared_task(name="send_activate_email_task", bind=True)
def send_activate_email_task(self, username ,email):
    logger.info("Sent account activated email")
    return send_activate_email(username=username, email=email)

@shared_task(name="send_deactivate_email_task", bind=True)
def send_deactivate_email_task(self, username ,email):
    logger.info("Sentaccount deactivated email")
    return send_deactivate_email(username=username, email=email)

