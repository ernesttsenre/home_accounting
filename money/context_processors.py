from money.models import Operation, Param


def global_vars(request):
    return {
        'week_credit': get_week_credit_amount()
    }


def get_week_credit_amount():
    credit_amount = Operation.get_credit_amount_by_week()
    credit_limit = Param.get_param('week_credit_amount_limit')

    credit_percent = 0
    if credit_limit and float(credit_limit) > 0:
        credit_percent = float(credit_amount) / float(credit_limit) * 100

    credit_color = 'success'
    if credit_percent >= 90:
        credit_color = 'danger'
    elif credit_percent >= 80:
        credit_color = 'warning'

    return {
        'amount': int(credit_amount),
        'limit': int(credit_limit),
        'percent': int(credit_percent),
        'color': credit_color,
        'is_danger': credit_percent > 100,
    }
