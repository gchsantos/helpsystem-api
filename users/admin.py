from django.contrib import admin

from .models import CommonUser, Customer, Seller, Phone, Address


class CommonAdmin(admin.ModelAdmin):
    readonly_fields = ('common_id',)


admin.site.register(Customer, CommonAdmin)
admin.site.register(Seller, CommonAdmin)
admin.site.register(CommonUser, CommonAdmin)
admin.site.register([Phone, Address])
