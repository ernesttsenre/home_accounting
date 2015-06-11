import easy
import copy

from django.contrib import admin
from money.models import Account, Category, Operation, Goal, Transfer, Param, PlanItem
from djrill import DjrillAdminSite

admin.site.site_header = 'Управление счетами'

# Mandrill
# admin.site = DjrillAdminSite()
admin.autodiscover()

class AccountInline(admin.TabularInline):
    model = Account
    suit_classes = 'suit-tab suit-tab-cities'


class AccountAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            # 'classes': ('suit-tab', 'suit-tab-general',),
            'fields': ('title',)
        }),
    )
    list_display = ('title', 'balance', 'created_at')
    date_hierarchy = 'created_at'
    # suit_form_tabs = (('general', 'Основное'), ('limits', 'Лимиты'))

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


class PlanItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'account', 'amount', 'period', 'must_closed_at', 'is_closed')
    list_filter = ('account', 'state',)
    search_fields = ['title']
    date_hierarchy = 'must_closed_at'
    list_per_page = 100
    actions = ('close_action',)

    def changelist_view(self, request, extra_context=None):
        if 'state__exact' not in request.GET:
            query = request.GET.copy()
            query['state__exact'] = PlanItem.STATE_OPENED
            request.GET = query
            request.META['QUERY_STRING'] = request.GET.urlencode()
        return super(PlanItemAdmin, self).changelist_view(request, extra_context=extra_context)

    @easy.action('Выполнить')
    def close_action(self, request, queryset):
        for qs in queryset:
            if not qs.is_closed:
                archive_item = copy.copy(qs)

                archive_item.id = None
                archive_item.mark_closed()
                archive_item.save()

                qs.calc_must_closed(True)
                qs.save()

        self.message_user(request, "Задачи выполнены")


admin.site.register(Account, AccountAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Operation, OperationAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(Transfer, TransferAdmin)
admin.site.register(Param, ParamAdmin)
admin.site.register(PlanItem, PlanItemAdmin)
