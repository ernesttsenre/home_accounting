from django.contrib import admin
from money.models import Account, Category, Operation, Goal, Transfer, Param
import easy

admin.site.site_header = 'Управление счетами'


class AccountInline(admin.TabularInline):
    model = Account
    suit_classes = 'suit-tab suit-tab-cities'


class AccountAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general',),
            'fields': ('title',)
        }),
        ('Лимит пополнения', {
            'classes': ('suit-tab', 'suit-tab-limits',),
            'fields': ('debit_limit', 'debit_limit_period',)
        }),
        ('Лимит списания', {
            'classes': ('suit-tab', 'suit-tab-limits',),
            'fields': ('credit_limit', 'credit_limit_period',)
        })
    )
    list_display = ('title', 'balance', 'created_at')
    date_hierarchy = 'created_at'
    suit_form_tabs = (('general', 'Основное'), ('limits', 'Лимиты'))

    actions = ('recalculate_action',)

    @easy.action('Пересчитать баланс')
    def recalculate_action(self, request, queryset):
        for qs in queryset:
            qs.balance = qs.get_balance()
            qs.save()

        self.message_user(request, "Баланс пересчитан")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    date_hierarchy = 'created_at'


class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'percent', 'created_at')
    date_hierarchy = 'created_at'

    actions = ('recalculate_action',)

    @easy.action('Пересчитать процент')
    def recalculate_action(self, request, queryset):
        for qs in queryset:
            qs.percent = qs.get_percent()
            qs.save()

        self.message_user(request, "Процент пересчитан")


class OperationAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'user', 'get_category_title', 'account', 'is_transfer', 'created_at')
    list_filter = ('user', 'category', 'account', 'created_at')
    search_fields = ['comment']
    date_hierarchy = 'created_at'
    list_per_page = 100


class TransferAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'amount', 'created_at')
    date_hierarchy = 'created_at'


class ParamAdmin(admin.ModelAdmin):
    list_display = ('title', 'value')


admin.site.register(Account, AccountAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Operation, OperationAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(Transfer, TransferAdmin)
admin.site.register(Param, ParamAdmin)
