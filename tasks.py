import os
import requests
from dotenv import load_dotenv


load_dotenv()

DOMAIN = os.getenv('MAILGUN_DOMAIN')


def send_simple_message(to, subject, body):
    return requests.post(
       f"https://api.mailgun.net/v3/{DOMAIN}/messages",
       auth=("api", os.getenv('MAILGUN_API_KEY')),
       data={"from": f"Krzysztof Smykała <postmaster@{DOMAIN}>",
             "to": [to],
             "subject": subject,
             "text": body})


def send_user_registration_email(email, username):
    return send_simple_message(
        email,
        'Welcome to our service',
        f'Hi {username}. Thank you for registering!'
    )
