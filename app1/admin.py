from django.contrib import admin
from app1.models import Account, DailyFreeTicket, Coupon, CouponHistory, Math, Hand
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.


class AccountInline(admin.StackedInline):
    model = Account
    verbose_name_plural = 'Contas'
    verbose_name = 'Conta'
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (AccountInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(DailyFreeTicket)
admin.site.register(Coupon)
admin.site.register(CouponHistory)
admin.site.register(Math)
admin.site.register(Hand)
