import os
import requests
import jinja2

from dotenv import load_dotenv


load_dotenv()

DOMAIN = os.getenv('MAILGUN_DOMAIN')
template_loader = jinja2.FileSystemLoader(searchpath="./templates")
template_env = jinja2.Environment(loader=template_loader)


def render_template(template_filename, **context):
    template = template_env.get_template(template_filename)
    return template.render(**context)


def send_simple_message(to, subject, body, html):
    return requests.post(
       f"https://api.mailgun.net/v3/{DOMAIN}/messages",
       auth=("api", os.getenv('MAILGUN_API_KEY')),
       data={"from": f"Krzysztof Smykała <postmaster@{DOMAIN}>",
             "to": [to],
             "subject": subject,
             "text": body,
             "html": html})


def send_user_registration_email(email, username):
    return send_simple_message(
        email,
        'Welcome to our service',
        f'Hi {username}. Thank you for registering!',
        render_template('action.html', username=username)
    )
