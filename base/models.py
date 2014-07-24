from django.db import models

# Create your models here.


class Student(models.Model):
    """

    """
    fio = models.CharField(max_length=255)
    birthday = models.DateField()
    number_student_cart = models.ImageField()
    group = models.ForeignKey("Group")


class Group(models.Model):
    """

    """
    name = models.CharField(max_length=255)
    headman = models.ForeignKey("Student")