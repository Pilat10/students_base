from django.db import models
from django.db.models.signals import post_save, post_delete
from base.signals import obj_save, obj_delete

# Create your models here.


class Group(models.Model):
    """

    """
    name = models.CharField(max_length=255)
    headman = models.OneToOneField(
        "Student", related_name='+', blank=True, null=True,
        on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.name


class Student(models.Model):
    """

    """
    fio = models.CharField(max_length=255)
    birthday = models.DateField()
    number_student_cart = models.IntegerField()
    group = models.ForeignKey("Group")

    def __unicode__(self):
        return self.fio


post_save.connect(obj_save, sender=Group)
post_save.connect(obj_save, sender=Student)
post_delete.connect(obj_delete, sender=Group)
post_delete.connect(obj_delete, sender=Student)