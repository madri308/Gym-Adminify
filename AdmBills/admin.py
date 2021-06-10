from django.contrib import admin

from .models import Bill, PayMethod

admin.site.register(Bill)
admin.site.register(PayMethod)
