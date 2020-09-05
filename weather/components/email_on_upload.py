from django.conf import settings
from django.core.mail import send_mail

def send_email_upload():
    subject = 'CSV Uploaded'
    message = 'A CSV file has been uploaded.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['testmail9920123@gmail.com']
    send_mail(subject, message, email_from, recipient_list)