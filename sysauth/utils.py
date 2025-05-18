from django.core.mail import EmailMessage
import os

class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject = data.get('subject'),
            from_email = os.environ.get('EMAIL_USER'),
            to = [data.get('to')],
            body = data.get('body')
        )
        email.send()