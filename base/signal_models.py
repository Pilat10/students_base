from django.db import models

ADD = 1
CHANGE = 2
DELETE = 3


class LogEntry(models.Model):
    """

    """
    ACTION_STATUS = (
        (1, 'add'),
        (2, 'change'),
        (3, 'delete'),
    )
    action_flag = models.PositiveSmallIntegerField(choices=ACTION_STATUS)
    action_time = models.DateTimeField(auto_now=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    object_descript = models.TextField(max_length=200)

    def __unicode__(self):
        return self.get_action_flag_display() + " '{}'".format(
            self.object_descript)