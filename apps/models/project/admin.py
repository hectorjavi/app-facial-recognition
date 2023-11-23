from django.contrib import admin

from . import models


# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "file", "ia_model", "created", "modified")
    list_per_page = 15
    ordering = ("-created", "-modified")
    date_hierarchy = "created"


admin.site.register(models.Project, ProjectAdmin)
