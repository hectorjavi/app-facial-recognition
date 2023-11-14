from django.contrib import admin

from . import models


# Register your models here.
class IAModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "model_file", "labels_model", "created", "modified")
    list_per_page = 15
    ordering = ("-created", "-modified")
    date_hierarchy = "created"


admin.site.register(models.IAModel, IAModelAdmin)
