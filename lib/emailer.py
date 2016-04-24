# Import global context
from flask.ext.mail import Mail, Message

# Import core libraries
from lib.decorators import async_threaded


class Emailer(Mail):

    def __init__(self, app):
        super().__init__(app)
        self.sender = app.config['MAIL_USERNAME']

    @async_threaded
    def send_email(self, app, recipient, email, params):
        message = Message(email['subject'], sender=self.sender,
                          recipients=[recipient])
        message.body = email['text']
        message.html = email['html'][params['html']]
        message.html = message.html.format(mp=params['mp'],
                                           mp_url=params['mp_url'],
                                           role=params.get('role', ''))
        message.html += email['footer']

        with app.app_context():
            super().send(message)
