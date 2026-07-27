from django.db import models

# Create your models here.


class Department(models.Model):
    """

    """
    name_department = models.CharField(max_length=255)

    def __str__(self):
        return self.name_department


class Group(models.Model):
    """

    """
    name = models.CharField(max_length=255)
    department = models.ForeignKey("Department", on_delete=models.CASCADE)
    headman = models.OneToOneField(
        "Student", related_name='+', blank=True, null=True,
        on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Student(models.Model):
    """

    """
    fio = models.CharField(max_length=255)
    birthday = models.DateField()
    number_student_cart = models.IntegerField()
    group = models.ForeignKey("Group", on_delete=models.CASCADE)

    def __str__(self):
        return self.fio


class LogEntry(models.Model):
    """

    """
    ADD, CHANGE, DELETE = 1, 2, 3
    ACTION_STATUS = (
        (ADD, 'add'),
        (CHANGE, 'change'),
        (DELETE, 'delete'),
    )
    action_flag = models.PositiveSmallIntegerField(choices=ACTION_STATUS)
    action_time = models.DateTimeField(auto_now=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    object_descript = models.TextField(max_length=200)

    def __str__(self):
        return "{} '{}'".format(
            self.get_action_flag_display(), self.object_descript)
