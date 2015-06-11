from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse

class Command(BaseCommand):
    help = 'Sending emails'

    def handle(self, *args, **options):
        msg = EmailMessage(
            subject='Test',
            from_email='ernest.oleg.iv@gmail.com',
            to=['ernest.oleg.iv@gmail.com']
        )
        msg.template_name = "debit"
        msg.global_merge_vars = {
            'TITLE': 'Домашний учет',
            'LINK': reverse('money:index'),
            'USERNAME': 'Таня',
            'OPERATION_USER': 'Олег',
            'OPERATION_ACCOUNT': 'Личный (Олег)',
            'OPERATION_AMOUNT': 40000,
            'COPYRIGHT': '2015 &copy; Иванов Олег',
        }
        msg.send()
