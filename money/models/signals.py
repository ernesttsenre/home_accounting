from django.db.models.signals import post_save, post_delete

from money.models import Operation, Transfer, Goal


def create_operation(sender, instance, **kwargs):
    instance.account.balance = instance.account.get_balance()
    instance.account.save()

    goals = Goal.objects.filter(account_id=instance.account.id)
    for goal in goals:
        goal.percent = goal.get_percent()
        goal.save()


def delete_operation(sender, instance, **kwargs):
    instance.account.balance = instance.account.get_balance()
    instance.account.save()

    goals = Goal.objects.filter(account_id=instance.account.id)
    for goal in goals:
        goal.percent = goal.get_percent()
        goal.save()


def create_transfer_operations(sender, instance, **kwargs):
    Operation.objects.filter(transfer_id=instance.id).delete()

    credit_operation = Operation()
    credit_operation.account = instance.account_from
    credit_operation.transfer = instance
    credit_operation.user = instance.user
    credit_operation.amount = instance.amount
    credit_operation.type = Operation.CREDIT_OPERATION
    credit_operation.save()

    debit_operation = Operation()
    debit_operation.account = instance.account_to
    debit_operation.transfer = instance
    debit_operation.user = instance.user
    debit_operation.amount = instance.amount
    debit_operation.type = Operation.DEBIT_OPERATION
    debit_operation.save()


post_save.connect(create_transfer_operations, sender=Transfer)
post_save.connect(create_operation, sender=Operation)
post_delete.connect(create_operation, sender=Operation)