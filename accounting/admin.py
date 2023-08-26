from django.contrib import admin

from .models import Purchase, Expenses, Balance

admin.site.register(Purchase)
admin.site.register(Expenses)
admin.site.register(Balance)


