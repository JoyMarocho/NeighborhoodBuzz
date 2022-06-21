from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_welcome_email(name, receiver):
    #create email subject and header
    subject = 'Welcome to the Neighbrhood Buzz'
    sender= 'joymarocho@gmail.com'
    
    # passing in the context variables
    text_content = render_to_string('email/buzzemail.txt',{"name": name})
    html_content = render_to_string('email/buzzemail.html',{"name": name})
    
    msg = EmailMultiAlternatives(subject, text_content, sender, [receiver])
    msg.attach_alternative(html_content, "text/html")
    msg.send()