from django.core.mail import EmailMessage
from web.models import Email_message
from urllib.parse import urljoin
from django.conf import settings
from django.template import loader

class Emails(object):
    def __init__(self, lang_code='pl'):
        self.lang_code = lang_code

    def render_to_string(self, template_name, context, **opts):
        context['base_url'] = urljoin(settings.BASE_DIR, self.lang_code)
        template_path = "emails/%s.html" % template_name
        return loader.render_to_string(template_path, context, **opts)

    @staticmethod
    def send(receiver, subject, message, attachment_filename=''):
        email = Email_message(receiver=receiver, subject=subject, message=message)
        email.save()

        msg = EmailMessage(subject, message, to=[receiver])
        msg.content_subtype = "html"
        if attachment_filename:
            msg.attach_file(attachment_filename)
        msg.send(fail_silently=True)

    def remind_password(self, receiver):
        args = {'receiver': receiver}
        message = self.render_to_string('remind_password', args)
        self.send(receiver=receiver,
                  subject="Rejestracja konta",
                  message=message)

    def register_me(self, receiver):
        self.send(receiver=receiver,
                  subject="Rejestracja konta",
                  message='')

    def account_registered(self, receiver):
        self.send(receiver=receiver,
                  subject="Twoje konto zostało zarejestrowane",
                  message='')

    def account_removed(self, receiver):
        self.send(receiver=receiver,
                  subject="Twoje konto zostało usunięte",
                  message='')


