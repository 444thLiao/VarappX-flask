from flask_mail import Mail
from varappx.handle_init import app
from flask_mail import Message
from varappx.handle_config import settings
mail = Mail(app)

email_TAGS = '[ VarX ]  '
def send_email(email_to, subject='No subject', text='', html='', tofile=None):
    """Call _send_email using the app's settings"""
    _send_email(settings.MAIL_USERNAME,email_to, subject=subject, text=text, html=html, tofile=tofile)

def _send_email(email_from,email_to, subject='No subject', text='', html='', tofile=None):
    """
    :param email_to: email of the receiver
    :param subject: head of the message
    :param text: plain text to send if HTML cannot be used
    :param html: message contend, in HTML format (has priority over *text*)
    :param tofile: file object, for testing purposes
    """
    msg = Message(email_TAGS+subject,sender=email_from,recipients=[email_to])
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred. If it is supported, only the HTML
    # message will be received.
    msg.bodt = text
    msg.html = html
    if tofile:
        tofile.write(msg.as_string())
    else:
        try:
            mail.send(msg)
        except ConnectionRefusedError:
            raise ConnectionRefusedError("No SMTP server was found at {}:{}".format(email_host, email_port))

