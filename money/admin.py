from django.contrib import admin
from .models import Account, Category, Operation

admin.site.site_header = 'Управление счетами'

class AccountAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    date_hierarchy = 'created_at'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    date_hierarchy = 'created_at'


class OperationAdmin(admin.ModelAdmin):
    list_display = ('description', 'user', 'category', 'account', 'created_at')
    list_filter = ['user', 'category', 'account', 'created_at']
    search_fields = ['comment']
    date_hierarchy = 'created_at'
    list_per_page = 100


admin.site.register(Account, AccountAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Operation, OperationAdmin)
