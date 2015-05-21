from django.contrib import admin
from .models import Account, Category, Operation, Goal, Transfer
import easy

admin.site.site_header = 'Управление счетами'

class AccountAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'created_at')
    date_hierarchy = 'created_at'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    date_hierarchy = 'created_at'


class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'get_percent', 'created_at')
    date_hierarchy = 'created_at'


class OperationAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'user', 'get_category_title', 'account', 'is_transfer', 'created_at')
    list_filter = ('user', 'category', 'account', 'created_at')
    search_fields = ['comment']
    date_hierarchy = 'created_at'
    list_per_page = 100


class TransferAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'amount', 'created_at')
    date_hierarchy = 'created_at'

admin.site.register(Account, AccountAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Operation, OperationAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(Transfer, TransferAdmin)
