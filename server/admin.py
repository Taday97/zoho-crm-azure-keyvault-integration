from django.contrib import admin
from .models import ZohoToken, Lead

class DetailsAdmin(admin.ModelAdmin):
    pass

admin.site.register(ZohoToken, DetailsAdmin)
admin.site.register(Lead, DetailsAdmin)

# Register your models here.    