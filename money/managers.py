import datetime

from django.db import models
from django.db import connection

class OperationQuerySet(models.QuerySet):
    def debit_operations(self):
        return self.filter(
            type=1,
            transfer_id__isnull=True
        )

    def credit_operations(self):
        return self.filter(
            type=-1,
            transfer_id__isnull=True
        )

    def get_credit_report_by_week(self, year, month):
        cursor = connection.cursor()
        try:
            cursor.execute('''
                SELECT
                  extract(WEEK FROM money_operation.created_at) AS week,
                  sum(money_operation.amount)
                FROM money_operation
                  INNER JOIN money_category ON money_category.id = money_operation.category_id AND money_category.affected_limit = TRUE
                WHERE money_operation.type = -1 AND money_operation.transfer_id IS NULL AND
                      extract(MONTH FROM money_operation.created_at) = %s AND extract(YEAR FROM money_operation.created_at) = %s
                GROUP BY week
                ORDER BY week
            ''', [month, year])

            items = cursor.fetchall()

            categories = ['%s нед' % int(row[0]) for row in items]
            data = [float(row[1]) for row in items]

            return {
                'categories': categories,
                'data': data
            }
        finally:
            cursor.close()


class OperationManager(models.Manager):
    def get_queryset(self):
        return OperationQuerySet(self.model, using=self._db)

    def debits(self):
        return self.get_queryset().debit_operations()

    def credits(self):
        return self.get_queryset().credit_operations()

    def get_credit_week_report(self, year, month):
        return self.get_queryset().get_credit_report_by_week(year, month)
