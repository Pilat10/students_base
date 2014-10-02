from django.core.management.base import BaseCommand
from base.models import Group


class Command(BaseCommand):
    """

    """
    can_import_settings = True

    def handle(self, *args, **options):
        lines = []
        for group in Group.objects.all():
            lines.append(
                u'group name {}, headman {}'.format(group.name, group.headman))
            for stud in group.student_set.all():
                lines.append(u'   {}'.format(stud.fio))

        return u"\n".join(lines)