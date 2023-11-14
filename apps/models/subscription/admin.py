from django.contrib import admin

from . import models


# Register your models here.
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "order", "created", "modified")
    list_per_page = 15
    ordering = ("-created", "-modified")
    date_hierarchy = "created"


admin.site.register(models.Subscription, SubscriptionAdmin)
