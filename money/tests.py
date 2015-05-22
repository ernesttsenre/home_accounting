from django.test import TestCase
from money.models import Account, Operation, Transfer, Category
from django.contrib.auth.models import User

DEFAULT_CREDIT_ACCOUNT_AMOUNT = 10000
DEFAULT_DEBIT_ACCOUNT_AMOUNT = 0


class FixturesTest(TestCase):
    fixtures = ['django_project/fixtures/users.json', 'money/fixtures/money.json']

    def setUp(self):
        self.credit_account = Account.objects.get(pk=1)
        self.debit_account = Account.objects.get(pk=2)

    def test_is_fixtures_correct(self):
        self.assertEqual(self.credit_account.balance, DEFAULT_CREDIT_ACCOUNT_AMOUNT)
        self.assertEqual(self.debit_account.balance, DEFAULT_DEBIT_ACCOUNT_AMOUNT)


class BaseTest(TestCase):
    fixtures = ['django_project/fixtures/users.json', 'money/fixtures/money.json']

    def setUp(self):
        self.credit_account = Account.objects.get(pk=1)
        self.debit_account = Account.objects.get(pk=2)
        self.category = Category.objects.get(pk=1)
        self.user = User.objects.get(pk=1)

    def test_changes_account_balance_when_create_new_debit_operation(self):
        """
        Когда для счета создается транзакция пополнения, необходимо проверить баланс счета,
        т.к. он пересчитывается сигналами
        :return:
        """

        operation_amount = 1000
        Operation.objects.create(
            account=self.credit_account,
            category=self.category,
            user=self.user,
            type=Operation.DEBIT_OPERATION,
            amount=operation_amount
        )

        self.assertEqual(self.credit_account.balance, DEFAULT_CREDIT_ACCOUNT_AMOUNT + operation_amount)

    def test_changes_account_balance_when_create_new_credit_operation(self):
        """
        Когда для счета создается транзакция списания, необходимо проверить баланс счета,
        т.к. он пересчитывается сигналами
        :return:
        """

        operation_amount = 1000
        Operation.objects.create(
            account=self.credit_account,
            category=self.category,
            user=self.user,
            type=Operation.CREDIT_OPERATION,
            amount=operation_amount
        )

        self.assertEqual(self.credit_account.balance, DEFAULT_CREDIT_ACCOUNT_AMOUNT - operation_amount)

    def test_create_operations_for_accounts_when_transfer_created(self):
        """
        Когда создается перевод денег, он обязан создать операцию расхода на кредитном счету
        и операцию прихода, на туже сумму, на дебиторном счету
        :return:
        """

        transfer_amount = 1000
        transfer = Transfer.objects.create(
            account_from=self.credit_account,
            account_to=self.debit_account,
            amount=transfer_amount,
            user=self.user
        )

        self.assertEqual(self.credit_account.balance, DEFAULT_CREDIT_ACCOUNT_AMOUNT - transfer_amount)
        self.assertEqual(self.debit_account.balance, DEFAULT_DEBIT_ACCOUNT_AMOUNT + transfer_amount)
