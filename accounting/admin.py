from django.contrib import admin
from . import models

@admin.register(models.FinancialEntity)
class FinancialEntityAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    readonly_fields = ('date_time_registered',)
    