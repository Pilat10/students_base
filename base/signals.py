from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save

from base.models import LogEntry


@receiver(post_save, sender='base.Group', dispatch_uid='base.log_group_save')
@receiver(post_save, sender='base.Student',
          dispatch_uid='base.log_student_save')
def obj_save(sender, instance, created=False, **kwargs):
    LogEntry.objects.create(
        action_flag=LogEntry.ADD if created else LogEntry.CHANGE,
        object_id=instance.pk,
        object_descript=str(instance),
    )


@receiver(post_delete, sender='base.Group',
          dispatch_uid='base.log_group_delete')
@receiver(post_delete, sender='base.Student',
          dispatch_uid='base.log_student_delete')
def obj_delete(sender, instance, **kwargs):
    LogEntry.objects.create(
        action_flag=LogEntry.DELETE,
        object_id=instance.pk,
        object_descript=str(instance),
    )
