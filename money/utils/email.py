from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.contrib.humanize.templatetags.humanize import intcomma

from money.models import Operation


class Email(object):
    @staticmethod
    def send_debit_email(user, operation):
        """
        :type user: User
        :type operation: Operation
        :return:
        """
        msg = EmailMessage(to=[user.email])
        msg.template_name = "debit"
        msg.global_merge_vars = {
            'TITLE': 'Домашний учет',
            'LINK': reverse('money:index'),
            'USERNAME': user.first_name,
            'OPERATION_USER': operation.user.first_name,
            'OPERATION_ACCOUNT': operation.account.title,
            'OPERATION_AMOUNT': intcomma(float(operation.amount)),
            'COPYRIGHT': '2015 &copy; Иванов Олег',
        }
        msg.send()
