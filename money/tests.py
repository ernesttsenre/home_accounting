from django.test import TestCase
from money.models import Account, Operation, Transfer, Category
from django.contrib.auth.models import User


class BaseTest(TestCase):
    def test_testing_system(self):
        return self.assertEqual(True, True)


class TransferTest(TestCase):
    def setUp(self):
        self.credit_amount = 10000
        self.debit_amount = 0

        self.user = User.objects.create(username='ernesttsenre', password='password', email='ernest.oleg.iv@gmail.com')
        self.category = Category.objects.create(title='Тесты')
        self.credit_account = Account.objects.create(title='Счет кредитор', balance=self.credit_amount)
        self.debit_account = Account.objects.create(title='Счет дебитор', balance=self.debit_amount)

        # создаю остаток на счете
        Operation.objects.create(
            account=self.credit_account,
            amount=self.credit_amount,
            user=self.user,
            category=self.category,
            type=Operation.DEBIT_OPERATION
        )

    def test_create_operations_for_accounts_when_transfer_created(self):
        """
        Когда создается перевод денег, он обязан создать операцию расхода на кредитном счету
        и операцию прихода, на туже сумму, на дебиторном счету
        :return:
        """

        self.assertEqual(self.credit_account.balance, self.credit_amount)
        self.assertEqual(self.debit_account.balance, self.debit_amount)

        transfer_amount = 1000
        transfer = Transfer.objects.create(
            account_from=self.credit_account,
            account_to=self.debit_account,
            amount=transfer_amount,
            user=self.user
        )

        self.assertEqual(self.credit_account.balance, self.credit_amount - transfer_amount)
        self.assertEqual(self.debit_account.balance, self.debit_amount + transfer_amount)
