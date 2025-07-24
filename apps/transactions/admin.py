from django.contrib import admin
from .models import Transaction

class AmountRangeFilter(admin.SimpleListFilter):
    title = "Amount Range"
    parameter_name = "amount"
    def lookups(self, request, model_admin):
        return (
        ('0~10000', '1만 -'),
        ('10000~100000', '1만 ~ 10만'),
        ('100000~1000000', '10만 ~ 100만'),
        ('1000000+', '100만 +')
        )

    def queryset(self, request, queryset):
        if self.value():
            if self.value() == '1000000+':
                return queryset.filter(amount__gte=1000000)
            else:
                min,max=map(int,self.value().split('~'))
                return queryset.filter(amount__gte=min, amount__lt=max)
        return queryset


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display=("id", "account_id", "amount", "io_type", "created_at")
    list_filter = ("io_type", AmountRangeFilter)