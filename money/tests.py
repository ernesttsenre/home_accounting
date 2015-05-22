from django.test import TestCase
from money.models import Transfer


class BaseTest(TestCase):
    def test_testing_system(self):
        return self.assertEqual(True, True)


# class TransferTest(TestCase):
#     def test_create_operations_for_accounts_when_transfer_created(self):
#         """
#         Когда создается перевод денег, он обязан создать операцию расхода на кредитном счету
#         и операцию прихода, на туже сумму, на дебиторном счету
#         :return:
#         """
#
#         account =
#         transfer = Transfer()
