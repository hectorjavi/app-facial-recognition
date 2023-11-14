from django.contrib import admin

from . import models


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "created", "modified")
    list_per_page = 15
    search_fields = ["email", "username", "id"]
    ordering = ("-created", "-modified")
    date_hierarchy = "created"
    list_filter = ["gender"]
    filter_horizontal = ["groups", "user_permissions"]


admin.site.register(models.User, UserAdmin)
