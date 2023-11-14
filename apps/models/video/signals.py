from django.db import transaction
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from django.db.models import Max

from .models import Video


@receiver(pre_delete, sender=Video)
@transaction.atomic
def pre_delete_video(sender, instance, **kwargs):
    instance.video.delete()


@receiver(post_save, sender=Video)
@transaction.atomic
def post_save_video(sender, instance, created, **kwargs):
    if created:
        video_max_label = Video.objects.filter(
            work_environment=instance.work_environment
        ).exclude(id=instance.id).order_by("-label").first()
        if video_max_label:
            instance.label = video_max_label.label + 1
        else:
            instance.label = 0
        instance.save()
