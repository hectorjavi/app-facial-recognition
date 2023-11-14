from django.contrib import admin

from . import models


# Register your models here.
class WorkEnvironmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created", "modified")
    list_per_page = 15
    ordering = ("-created", "-modified")
    date_hierarchy = "created"


admin.site.register(models.WorkEnvironment, WorkEnvironmentAdmin)
