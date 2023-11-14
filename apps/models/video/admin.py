from django.contrib import admin

from . import models


# Register your models here.
class VideoAdmin(admin.ModelAdmin):
    list_display = ("id", "label_name", "label", "created", "modified")
    list_per_page = 15
    ordering = ("-created", "-modified")
    date_hierarchy = "created"

    def delete_queryset(self, queryset):
        # En este ejemplo, simplemente lanzaremos una excepción cuando se intente eliminar múltiples instancias
        if queryset.count() > 1:
            raise Exception("La eliminación múltiple no está permitida en este modelo.")
        # Si solo se está eliminando una instancia, llamamos al método delete_queryset predeterminado
        super().delete_queryset(queryset)


admin.site.register(models.Video, VideoAdmin)
