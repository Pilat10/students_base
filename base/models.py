from django.db import models

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