
from django.contrib import admin
from .models import Country, Department, NDS, Group, Contact, BankCode, Contractor, Product, UnitOfMeasurement, \
    AccountingFeatures, EGAISCode, Warehouse, Project, Receipt, Remains, Сancellation, Purchase

admin.site.register(Country)
admin.site.register(Department)
admin.site.register(NDS)
admin.site.register(Group)
admin.site.register(Contact)
admin.site.register(BankCode)
admin.site.register(Contractor)
admin.site.register(Product)
admin.site.register(AccountingFeatures)
admin.site.register(EGAISCode)
admin.site.register(UnitOfMeasurement)
admin.site.register(Warehouse)
admin.site.register(Project)
admin.site.register(Receipt)
admin.site.register(Remains)
admin.site.register(Сancellation)

