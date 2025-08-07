from django.core.mail import send_mail
from django.conf.global_settings import EMAIL_HOST_USER
from . models import Profile

def SendMail(email):
    subject = "Welcome to Ultra application"
    message = f"""
                        Welcome {Profile.full_name}.
                        This is an onboarding message to show you that you are
                        now a registered user of the app
                """ 
    send_mail(
        subject,
        message,
        EMAIL_HOST_USER,
        [email],
        fail_silently=True)