from django.contrib import admin
from .models import Account

# 목록에 보여줄 필드를 설정하는 클래스
class AccountAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user_id', 'account_number', 'balance')

# Account 모델을 AccountAdmin 설정과 함께 등록
admin.site.register(Account, AccountAdmin)